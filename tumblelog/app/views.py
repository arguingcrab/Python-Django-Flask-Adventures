import re, os
from datetime import datetime
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from flask_login import login_user, logout_user, login_required, current_user
from mongoengine import ValidationError
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash
from app import app, db
from .auth import redirect_auth
from .forms import LoginForm, RegisterForm
from .models import Post, Comment, BlogPost, Video, Image, Quote, User, Session, LoginHistory

'''
views/functions that don't require login + login/register/logout
'''

posts = Blueprint('posts', __name__, template_folder='templates')

class ListView(MethodView):
    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)
        
        
class DetailView(MethodView):
    # modified to handle form
    form = model_form(Comment, exclude=['created_at', 'id'])
    
    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)
        
        context = {
            "post": post,
            "form": form,
        }
        
        return context
        
    # get default context
    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)
        
    # validates comment on post, post appends comment to post on valid
    # get default context
    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')
        
        if form.validate():
            comment = Comment()
            form.populate_obj(comment)
            comment.ip = request.remote_addr
            # comment.ip = request.environ['REMOTE_ADDR']
            post = context.get('post')
            post.comments.append(comment)
            try:
                post.save()
                return redirect(url_for('posts.detail', slug=slug))
            except ValidationError:
                flash(":(")
        return render_template('posts/detail.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
@redirect_auth
def login():
    cls = User
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = cls.objects.get(username__iexact=form.username.data)
        except:
            user=None
        if user and User.validate_login(user.password, form.password.data):
            user_obj = User(user.username)
            if user.active:
                try:
                    session = Session.objects.get(user=user)
                    session.update(set__session=os.urandom(32), set__last_login=datetime.now())
                except:
                    session = Session(user=user, ip=request.remote_addr,session=os.urandom(32), last_login=datetime.now())
                    # session = Session(user=user, ip=request.environ['REMOTE_ADDR'],session=os.urandom(32), last_login=datetime.now())
                    session.save()
                login_history = LoginHistory(user=user, ip=request.remote_addr, date_time=datetime.now())
                # login_history = LoginHistory(user=user, ip=request.environ['REMOTE_ADDR'], date_time=datetime.now())
                login_history.save()
                login_user(user_obj)
                flash("Logged in successfully", category='success')
                return redirect(request.args.get("next") or url_for("admin.index"))
        flash("Invalid username or password", category='error')
    return render_template('login.html', title='login', form=form)
    
    
@app.route('/logout/')
@login_required
def logout():
    user = User.objects.get(username=current_user.username)
    session = Session.objects.get(user=user)
    session.update(set__session='')
    logout_user()
    # flash("Logged out successfully")
    return redirect(url_for('login'))

    
@app.route('/register/', methods=['GET', 'POST'])
@redirect_auth
def register():
    cls = User
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User(re.sub('[^a-zA-Z0-9]', '_', form.username.data).rstrip('_').lstrip('_'), form.email.data, generate_password_hash(form.password.data), active=False)
            user.save()
            # if you want to auto-log them in after registering
            # user_obj = User(user.username)
            # login_user(user_obj)
            flash("Registered successfully", category='success')
            return redirect(request.args.get("next") or url_for("login"))
        except (DuplicateKeyError, NotUniqueError)as n:
            # pymongo exception / mongoengine exception
            unique = ['username', 'email']
            for field in unique:
                if field in str(n):
                    flash("Duplicate entry: %s already exists" % (field.title()))
    return render_template('register.html', title='register', form=form)


@app.route('/category/', defaults={'category': ''}, methods=['GET', 'POST'])
@app.route('/category/<category>', methods=['GET', 'POST'])
def list_category(category):
    if category.lower() in ('post', 'posts', 'blog', 'blog_post', 'blog_posts') :
        posts = Post.objects(class_check=True, _cls__in=['Post.BlogPost'])
    elif category.lower() in ('video', 'videos') :
        posts = Post.objects(class_check=True, _cls__in=['Post.Video'])
    elif category.lower() in ('image', 'images') :
        posts = Post.objects(class_check=True, _cls__in=['Post.Image'])
    elif category.lower() in ('quote', 'quotes') :
        posts = Post.objects(class_check=True, _cls__in=['Post.Quote'])
    else:
        posts = None
        
    return render_template('posts/list.html', posts=posts)


# register class urls (posts.list, posts.detail)
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
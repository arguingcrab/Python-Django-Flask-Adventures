from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from flask_login import login_user, logout_user, login_required
from mongoengine import ValidationError
from mongoengine.errors import NotUniqueError
from mongoengine.queryset.visitor import Q
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash
from app import app, db
from .auth import redirect_auth
from .forms import LoginForm, RegisterForm
from .models import Post, Comment, BlogPost, Video, Image, Quote, User

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
    form = model_form(Comment, exclude=['created_at'])
    
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
            user = cls.objects.get(username=form.username.data)
        except:
            user=None
        if user and User.validate_login(user.password, form.password.data):
            user_obj = User(user.username)
            if user.active:
                login_user(user_obj)
                flash("Logged in successfully", category='success')
                return redirect(request.args.get("next") or url_for("admin.index"))
        flash("Invalid username or password", category='error')
    return render_template('login.html', title='login', form=form)
    
    
@app.route('/logout/')
@login_required
def logout():
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
            user = User(form.username.data, form.email.data, generate_password_hash(form.password.data), active=False)
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
    print(category)
    if category.lower() in ('post', 'posts', 'blog') :
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


@app.route('/search/', methods=['GET', 'POST'])
def search_posts():
    data = request.form.get('search', '')
    print(request.form)
    print(request.referrer, data)
    try:
        if 'admin' in request.referrer and data:
            posts = Post.objects(Q(title__contains=data) | \
                Q(slug__contains=data) | Q(body__contains=data) | \
                Q(author__contains=data) | Q(post_author__contains=d))

            print(posts)
            return render_template('admin/search_results.html', posts=posts, data=data)
        else:
            # objects = Post.objects.search(data)
            # print(objects)
            return redirect(url_for('admin.index'))
    except:
        return redirect(url_for('admin.index'))

# register class urls (posts.list, posts.detail)
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
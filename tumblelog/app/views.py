from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from flask_login import login_user, logout_user
from mongoengine import ValidationError
from app import app, db
from .forms import LoginForm
from .models import Post, Comment, BlogPost, Video, Image, Quote, User

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
        return render_template('post/detail.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():  
    cls = User
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # print(db.users.find_one_or_404({'_id': form.username.data}))
        # print(User.objects.all())
        # print(form.username.data)
        # .where(User.username == form.username.data))
        try:
            user = cls.objects(username=form.username.data)
        except:
            user=None
        for u in user:
            pass
        #     print(u.__dict__)
        # print(">>",user.__dict__)
        # ?
        user_password = None
        user_username = None
        try:
            for x in user._result_cache:
                user_password = x['password']
                user_username = x['username']
                # print(x['password'])
            # print(user_password)
        except:
            pass
        # print(">>>",user_password)
        # print(">",user._result_cache)
        # print(user_password)
        # print(user._result_cache)
        # print(form.password.data)
        # user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user_password, form.password.data):
            # user_obj = User(user['_id'])
            user_obj = User(user_username)
            login_user(user_obj)
            flash("Logged in successfully", category='success')
            return redirect(request.args.get("next") or url_for("admin.index"))
        flash("Wrong username or password", category='error')
    return render_template('login.html', title='login', form=form)
    
@app.route('/logout/')
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('login'))


# register urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
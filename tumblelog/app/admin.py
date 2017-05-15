import os
from flask import Blueprint, request, redirect, render_template, url_for, flash, session
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from flask_login import login_required, current_user
from mongoengine import ValidationError
from mongoengine.errors import NotUniqueError
from mongoengine.queryset.visitor import Q
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app, login_manager
from .forms import UserForm
from .models import Post, Comment, BlogPost, Video, Image, Quote, User

'''
views/functions that do require login/authentication
'''

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [login_required]
    cls = Post
    
    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)      
        

class Detail(MethodView):
    decorators = [login_required]
    class_map = {
        'post': BlogPost,
        'video': Video,
        'image': Image,
        'quote': Quote,
    }
    
    def get_context(self, slug=None):
        if slug:
            post = Post.objects.get_or_404(slug=slug)
            # handle old posts also
            cls = post.__class__ if post.__class__ != Post else BlogPost
            form_cls = model_form(cls, exclude=('created_at', 'comments', 'archived_at', 'post_author'))
            if request.method == 'POST':
                form = form_cls(request.form, initial=post._data)
            else:
                form = form_cls(obj=post)
        else:
            cls = self.class_map.get(request.args.get('type', 'post'))
            post = cls()
            form_cls = model_form(cls, exclude=('created_at', 'comments', 'archived_at', 'post_author'))
            form = form_cls(request.form)
            
        context = {
            "post": post,
            "form": form,
            "create": slug is None,
        }
        
        return context
        
    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)
        
    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')
        
        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            try:
                post.save()
                if context.get('create'):
                    flash('Post created')
                    return redirect(url_for('admin.index'))
                flash('Post updated')
                return render_template('admin/detail.html', **context)
            except ValidationError as e:
                for v in reversed(sorted(e.errors.values())):
                    flash("%s" % (str(v[0])))
            except NotUniqueError as n:
                unique = ['slug', 'title']
                for word in unique:
                    if word in str(n):
                        flash("Duplicate entry: %s already exists" % (word.title()))
        return render_template('admin/detail.html', **context)

    
# nagivate with or without <user_name> param    
@app.route('/user/', defaults={'user_name': ''}, methods=['GET', 'POST'])
@app.route('/user/<user_name>', methods=['GET', 'POST'])
@login_required
def profile(user_name):
    cls = User
    if not user_name:
        user_name = current_user.username
    view_user_name = cls.objects.get(username=user_name)
    
    form = UserForm()
    # if request.method == 'POST' and form.validate_on_submit():
    if request.method == 'POST':
        if current_user.status == 'admin':
            active_status = form.active.data
        else:
            active_status = True
        new_password = view_user_name.password
        if current_user.username == view_user_name.username or current_user.status == 'admin':
            if User.validate_login(view_user_name.password, form.password.data) \
                    and form.password2.data \
                    and not User.validate_login(view_user_name.password, form.password2.data):
                new_password = generate_password_hash(form.password2.data)
            
            # update user obj with new data
            try:
                cls.objects.get(username=user_name).update(set__email=form.email.data,set__password=new_password, set__active=active_status)
                if not User.validate_login(view_user_name.password, form.password2.data) \
                        and form.password2.data:
                    flash("Profile successfully changed. Please relog.")
                    return redirect(url_for('logout'))
                else:
                    flash("Profile successfully changed")
                    return redirect(url_for('profile', user_name = view_user_name.username))
            except (DuplicateKeyError, NotUniqueError)as n:
                flash("Duplicate entry: Email already exists")
    return render_template('admin/edit_user.html', title='register', form=form, current_user=current_user, view_user_name=view_user_name)


@app.route('/users/', methods=['GET', 'POST'])
@login_required
def list_users():
        cls = User
        users = cls.objects.all()
        return render_template('admin/user-list.html', users=users)
        

@app.route('/admin/<edit_type>/<post_slug>/', methods=['GET', 'POST'])        
@login_required
def delete_archive_post(edit_type, post_slug):
    cls = Post
    if edit_type == 'archive':
        if cls.objects.get(slug=post_slug).archived_at:
            cls.objects.get(slug=post_slug).update(unset__archived_at="")
        else:
            cls.objects.get(slug=post_slug).update(set__archived_at=datetime.now)
    elif edit_type == 'delete':
        cls.objects.get(slug=post_slug).delete()
    
    flash("Post updated")
    return redirect(url_for('admin.index'))
    


@app.route('/admin/search/', methods=['GET', 'POST'])
@login_required
def admin_search_posts():
    data = request.form.get('search', '')
    if request.referrer and 'admin' in request.referrer and data:
        posts = Post.objects(Q(title__contains=data) | \
            Q(slug__contains=data) | Q(body__contains=data) | \
            Q(author__contains=data))

        return render_template('admin/search_results.html', posts=posts, data=data)
    else:
        return redirect(url_for('admin.index'))
        
@app.route('/admin/category/', defaults={'category': ''}, methods=['GET', 'POST'])
@app.route('/admin/category/<category>/', methods=['GET', 'POST'])
def admin_list_category(category):
    if category.lower() == 'blog_post' :
        posts = Post.objects(class_check=True, _cls__in=['Post.BlogPost'])
    elif category.lower() == 'video' :
        posts = Post.objects(class_check=True, _cls__in=['Post.Video'])
    elif category.lower() == 'image' :
        posts = Post.objects(class_check=True, _cls__in=['Post.Image'])
    elif category.lower() == 'quote' :
        posts = Post.objects(class_check=True, _cls__in=['Post.Quote'])
    else:
        posts = None
        
    return render_template('admin/list.html', posts=posts)
    
@app.route('/admin/comments/', defaults={'slug': ''}, methods=['GET', 'POST'])
@app.route('/admin/comments/<slug>/', methods=['GET', 'POST'])    
@login_required
def manage_comments(slug):
    cls = Post
    posts = cls.objects(slug=slug)
    return render_template('admin/comments.html', posts=posts)


@app.route('/admin/purge', methods=['GET', 'POST'])    
@login_required
def purge():
    app.secret_key = os.urandom(32)
    return redirect(url_for('admin.index'))

# register class urls (admin.index, admin.create, admin.edit)
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/post/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/post/<slug>/', view_func=Detail.as_view('edit'))
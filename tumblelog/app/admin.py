from flask import Blueprint, request, redirect, render_template, url_for, flash, g
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from flask_login import login_required, current_user
from mongoengine import ValidationError
from mongoengine.errors import NotUniqueError
from werkzeug.security import generate_password_hash
from app import app, login_manager
from .auth import requires_auth
from .forms import UserForm
from .models import Post, Comment, BlogPost, Video, Image, Quote, User

'''
views/functions that do require login
'''

admin = Blueprint('admin', __name__, template_folder='templates')

# @login_required
class List(MethodView):
    decorators = [requires_auth]
    cls = Post
    
    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)      
        

class Detail(MethodView):
    decorators = [requires_auth]
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
            form_cls = model_form(cls, exclude=('created_at', 'comments'))
            if request.method == 'POST':
                form = form_cls(request.form, initial=post._data)
            else:
                form = form_cls(obj=post)
        else:
            cls = self.class_map.get(request.args.get('type', 'post'))
            post = cls()
            form_cls = model_form(cls, exclude=('created_at', 'comments'))
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
                return redirect(url_for('admin.index'))
            except ValidationError as e:
                for v in reversed(sorted(e.errors.values())):
                    flash("%s" % (str(v[0])))
            except NotUniqueError as n:
                unique = ['slug', 'title']
                for word in unique:
                    if word in str(n):
                        flash("Duplicate entry: %s already exists" % (word.title()))
        return render_template('admin/detail.html', **context)

    
    
@app.route('/user/', defaults={'user_name': ''}, methods=['GET', 'POST'])
@app.route('/user/<user_name>', methods=['GET', 'POST'])
@requires_auth
def profile(user_name):
    cls = User
    # view_user_name = current_user
    if not user_name:
        user_name = current_user.username
    view_user_name = cls.objects.get(username=user_name)
    
    form = UserForm()
    # if request.method == 'POST' and form.validate_on_submit():
    if request.method == 'POST':
        if current_user.username == view_user_name.username or current_user.status == 'admin':
            if User.validate_login(view_user_name.password, form.password.data) \
                    and not User.validate_login(view_user_name.password, form.password2.data):
                view_user_name.password = generate_password_hash(form.password2.data)
            
            cls.objects(username=user_name).update_one(set__email=form.email.data,set__password=view_user_name.password, set__active=form.active.data)
            
            # , upsert=True
            # view_user_name.save()
            flash("Profile successfully changed")
            return redirect(url_for('profile', user_name = view_user_name.username))
    # current_user_info = {k:current_user for k in current_user}
    # print(current_user_info['username'])
    # for n in current_user:
    #     print(type(n))
        # if n.username:
        #     print(n)
        
        # current_username = n['username']
        # current_email = n['email']
    return render_template('admin/edit_user.html', title='register', form=form, current_user=current_user, view_user_name=view_user_name)


@app.route('/users/', methods=['GET', 'POST'])
@requires_auth
def list_users():
        cls = User
        users = cls.objects.all()
        return render_template('admin/user-list.html', users=users)  

# register urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
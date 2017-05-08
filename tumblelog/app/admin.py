from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from mongoengine import ValidationError
from mongoengine.errors import NotUniqueError
from .auth import requires_auth
from .models import Post, Comment, BlogPost, Video, Image, Quote

admin = Blueprint('admin', __name__, template_folder='templates')

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


# register urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
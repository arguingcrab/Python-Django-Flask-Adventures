from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_mongoengine.wtf import model_form
from mongoengine import ValidationError
from .models import Post, Comment, BlogPost, Video, Image, Quote

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
        

# register urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
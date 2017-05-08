import logging
import mmap
from datetime import datetime
from mongoengine import signals, ValidationError
from flask import url_for, render_template, flash
from app import db, app
from app.b import stops

def handler(e):
    def decorator(f):
        def apply(cls):
            e.connect(f, sender=cls)
            return cls
        f.apply = apply
        return f
    return decorator

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
   

class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__


    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        error = None
        for x in document.title.split():
            if x.lower() in stops:
                error = x.lower()
        return error
    
    def save(self, *args, **kwargs):
        error = Post.pre_save(self.__class__, document=self)
        if error is None:
            return super(Post, self).save(*args, **kwargs)
        else:
            raise ValidationError("ValidationError", errors=error)
            
    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }


class BlogPost(Post):
    body = db.StringField(required=True)
    
    
class Video(Post):
    embed_code = db.StringField(required=True)

    
class Image(Post):
    image_url = db.StringField(max_length=255, required=True)
    
    
class Quote(Post):
    body = db.StringField(required=True)
    author = db.StringField(verbose_name="Author Name", max_length=255, required=True)


signals.pre_save.connect(Post.pre_save, sender=Post)
import logging
import mmap
from datetime import datetime
from mongoengine import signals, ValidationError
from flask import url_for, render_template, flash
from flask_login import UserMixin
from cerberus import Validator
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, app, login_manager
from .b import stops
from .signals import post_pre_save
from .validators import MyValidator


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
   

class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True, unique=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
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
    
    # def __init__(self, settings):
    #     self.settings = settings[self.__class__]
    # def get_post_content(self):
    #     post_content = None
        
    def save(self, *args, **kwargs):
        # print(Post().post_type)
        # print(self.post_type)
        # def clean(self):
        schema = {
            'title': {'filter_words': self.title, 'anyof_type': ['string', 'integer']},
            'slug': {'filter_words': self.slug, 'anyof_type': ['string', 'integer']},
            'embed_code': {'anyof_type': ['string', 'integer'], 'empty': True},
            'image_url': {'anyof_type': ['string', 'integer'], 'empty': True},
        }
        
        document = {'title': self.title, 'slug': self.slug}
        if hasattr(self, 'body'):
            document['body'] = self.body
            schema['body'] = {'filter_words': self.body, 'anyof_type': ['string', 'integer'], 'empty': True}
        if hasattr(self, 'embed_code'):
            document['embed_code'] = self.embed_code
        if hasattr(self, 'image_url'):
            document['image_url'] = self.image_url
        if hasattr(self, 'author'):
            document['author'] = self.author
            schema['author'] = {'filter_words': self.author, 'anyof_type': ['string', 'integer'], 'empty': True}
            
        v = MyValidator(schema)
        if v.validate(document):
            return super(Post, self).save(*args, **kwargs)
        else:
            raise ValidationError("ValidationError", errors=v.errors)
            
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


# class User(UserMixin):
class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(max_length=255, required=True, unique=True)
    password = db.StringField(required=True)
    status = db.StringField(required=True, default='normal')
    active = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    
    # def __init__(self, username, email, active, *args, **kwargs):
    #     super(db.Document, self).__init__(*args, **kwargs)
    #     self.username = username
    #     self.email = email
        # self.email = username
        # self.password = username
        # self.active = username
        
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return self.active
        
    def is_anonymous(self):
        return False
        
    def get_status(self):
        return self.status
        
    def get_id(self):
        return self.username
        
    def __repr__(self):
        return self.username
        
    @staticmethod
    def validate_login(password_hash, password):
        # print(password_hash, password)
        # return password_hash == password
        return check_password_hash(password_hash, password)
        
# ? where do i put this...
@login_manager.user_loader
def load_user(username):
    # u = app.config['USERS_COLLECTION'].find_one({'_id': username})
    # u = DBUsers.query.get(username)
    u = User.objects.get(username=username)
    # print(">>>",u.username)
    # cls.objects(username=form.username.data)
    # if not u:
    #     return None
    # return User.get()
    return User(u.username, u.email, u.password, u.status, u.active)
    # return User(u.name,u.id,u.active)
    # return User(u['_id'])
        
signals.pre_save.connect(Post.pre_save, sender=Post)
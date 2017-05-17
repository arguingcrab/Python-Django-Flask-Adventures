import re, os
from bson import ObjectId
from datetime import datetime
from mongoengine import signals, ValidationError
from flask import url_for, render_template, flash, request, redirect
from flask_login import current_user, logout_user
from cerberus import Validator
from werkzeug.security import check_password_hash
from app import db, app, login_manager
from .bad_words import stops
from .validators import MyValidator
# from .views import logout


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(max_length=255, required=True, unique=True)
    password = db.StringField(required=True)
    status = db.StringField(required=True, default='normal')
    active = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    # session = db.BinaryField(nullable=True)
        
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
        
    def get_session(self):
        return self.session
        
    def __repr__(self):
        return self.username
        
    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
        
# ? where do i put this...
@login_manager.user_loader
def load_user(username):
    u = User.objects.get(username=username)
    try:
        session = Session.objects.get(user=u)
    except:
        session = Session(user=u, ip=request.remote_addr,session=os.urandom(32), last_login=datetime.now())
        # session = Session(user=u, ip=request.environ['REMOTE_ADDR'],session=os.urandom(32), last_login=datetime.now())
        session.save()
    delta = session.last_login - datetime.now()
    if delta.days <= -5:
        session.update(set__session='')
    if not session.session:
        return None
    # current_user will have these values (current_user.username etc)
    return User(u.username, u.email, u.password, u.status, u.active)


class Session(db.Document):
    user = db.ReferenceField(User, unique=True)
    ip = db.StringField(required=True)
    session = db.BinaryField(nullable=True)
    last_login = db.DateTimeField(default=datetime.now, required=True)


class LoginHistory(db.Document):
    user = db.ReferenceField(User)
    ip = db.StringField(required=True)
    date_time = db.DateTimeField(required=True)

class Comment(db.EmbeddedDocument):
    id = db.ObjectIdField(default=ObjectId)
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
    approved = db.BooleanField(default=0)
    ip = db.StringField(default="")
   

class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    title = db.StringField(max_length=255, required=True, unique=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    post_author = db.ReferenceField(User)
    archived_at = db.DateTimeField(required=False)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    # signal - send&connect or Post.pre_save
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        error = None
        for x in document.title.split():
            if x.lower() in stops:
                error = x.lower()
        return error
        
    def save(self, *args, **kwargs):
        #cerberus validation schema
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
            self.slug = re.sub('[^a-zA-Z0-9\-]', '-', self.slug)
            self.slug = re.sub(r'([\-])\1+', r'\1', self.slug).rstrip('-').lstrip('-')
            self.post_author = User.objects.get(username=current_user.username)
            # self.slug == z.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=_+"})
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
    
signals.pre_save.connect(Post.pre_save, sender=Post)
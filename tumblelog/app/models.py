import logging
import logging
import mmap
from datetime import datetime
from mongoengine import signals, ValidationError
# from flask.signals import Namespace
# from blinker import signal, Namespace
from flask import url_for, render_template
from app import db, app
from app.b import stops

# test = Namespace()
# post_test_signal = test.signal('_post_pre_save')

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
    # @handler(signals.pre_save)
    def pre_save(cls, sender, document, **kwargs):
        # signals.pre_save.send(self.__class__, document=self)
        error = None
        print("!")
        for x in document.title.split():
            if x.lower() not in stops:
                print(":)")
            else:
                error = ":( %s" % ( x.lower() )
                print(error)
                return render_template('admin/detail.html', error=error)
        return error
                
    
    # @classmethod
    # def attach_signals(cls):
    #     signals.pre_save.connect(cls.pre_save, sender=cls)            
    # # @signals.pre_save.connect_via(app)
    
    # def save(self, *args, **kwargs):
    #     # _post_pre_save.send(self.pre_save)
    #     # print(self)
    #     # self.pre_save(self, Post)
    #     print("?")
    #     return super(Post, self).save(*args, **kwargs)
    
    
    # @pre_save.apply
    # def clean(self):
    def save(self, *args, **kwargs):
        error = Post.pre_save(self.__class__, document=self)
        if error is None:
        # super(Post, self).pre_save(*args, **kwargs)
            print(Post.pre_save(self.__class__, document=self))
            print("clean")
            return super(Post, self).save(*args, **kwargs)
        else:
            print(">:|")
            # raise ValidationError(":|", error=error)
            
            
        # def pre_save(cls, sender, document, **kwargs):
        #     # signals.pre_save.send(self.__class__, document=self)
        #     print("!")
        #     for x in document.title.split():
        #         if x.lower() not in stops:
        #             print(":)")
        #         else:
        #             print(":( %s" % ( x.lower() ))
        #             raise Exception(":(")
        # pre_save(self.__class__, document=self, sender=Post) 
        
        # pre_save(self, sender=Post)                       
        # signals.pre_save.connect(self, sender=Post)
    #     # print(signals.pre_save.send(self, sender=Post))
    #     # test.send(app, sender=Post)
    #     post_test_signal.send(self, sender=Post)
    #     # test.send(self)
    #     # attach_signals(self)
            
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

# @classmethod
# def _pre_save(sender, *args, **kwargs):
#     # signals.pre_save.send(self.__class__, document=self)
#     print("!")
#     for x in document.title.split():
#         if x.lower() not in stops:
#             print(":)")
#         else:
#             print(":( %s" % ( x.lower() ))
#             raise Exception(":(")     

# signals.pre_save.connect(_post_pre_save, sender=Post)
signals.pre_save.connect(Post.pre_save, sender=Post)
# signals.pre_save.connect(Post, sender=Post)
# print("1")
# signals.pre_save.connect(_pre_save, sender=BlogPost)
# signals.post_save.connect(Post.post_save, sender=Post)
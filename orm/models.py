from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Connecting
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
# Creating a session ( db_session.add(x), db_session.commit(x) )
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Declare a Mapping # Base.metadata.create_all(engine)
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __repr__(self):
        return "<User(name= '%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password
        )
        
# Relationship
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User, 
        back_populates="addresses", 
        cascade='delete, all, delete-orphan',
        single_parent=True,
    )
    
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address
        
# Base.metadata.create_all(engine) and possibly restart        
User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

# Many to Many
post_keywords = Table(
    'post_keywords', 
    Base.metadata, 
    Column('post_id', ForeignKey('posts.id'), primary_key=True), 
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)

class BlogPost(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    
    # many to many BlogPost>-<Keyword
    keywords = relationship('Keyword', secondary=post_keywords, back_populates='posts')
    
    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body
        
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)
        
        
class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost', secondary=post_keywords, back_populates='keywords')
    
    def __init__(self, keyword):
        self.keyword = keyword
        

BlogPost.author = relationship(User, back_populates="posts")
User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
# For column level options
from sqlalchemy.orm import column_property
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Connecting
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
# Creating a session ( db_session.add(x), db_session.commit(x) )
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Declare a Mapping # Base.metadata.create_all(engine)
Base = declarative_base()
Base.query = db_session.query_property()


# Naming columns distinctly from attribute names
class User(Base):
    __tablename__ = 'users'
    id = Column('user_id', Integer, primary_key=True)
    name = column_property(Column('user_name', String(50)), active_history=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    fullname = column_property(firstname + " " + lastname)
    password = Column(String)
    
    # for existing table:
    # class User(Base):
    #     __table__ = user_table
    #     id = user_table.c.user_id
    # column_property also used to map single attr to multiple cols
    # class User(Base):
    #     __table__ = user.join(address)
    #     id = column_property(user_table.c.id, address_table.c.user_id)
    
    def __repr__(self):
        return "<User(name= '%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password
        )
        
    addresses = relationship("Address", backref="users", order_by="Address.id")
        
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
# User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

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
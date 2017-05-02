from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref, mapper
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

# Connecting
engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
# Creating a session ( db_session.add(x), db_session.commit(x) )
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Declare a Mapping # Base.metadata.create_all(engine)
Base = declarative_base()
Base.query = db_session.query_property()

# Classical Mappings http://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html
metadata = MetaData()

user = Table('user', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(50)),
        Column('fullname', String(50)),
        Column('password', String(12)),
    )
    
class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
        
# mapper(User, user)

class Address(object):
    def __init__(self, email_address, user_id):
        self.email_address = email_address
        self.user_id = user_id

# Relationship
address = Table('address', metadata, 
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('user.id')),
        Column('email_address', String(50)),
    )
    
mapper(User, user, properties={
    'addresses': relationship(Address, backref='user', order_by=address.c.id)
})

mapper(Address, address)


# Classical mapping to existing table
# mapper(User, user_table, properties={
#     'id': user_table.c.user_id, 
#     'name': user_table.c.user_name,
# })

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

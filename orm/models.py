from flask import Flask
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
# For column level options, and validation
from sqlalchemy.orm import column_property, validates
from sqlalchemy.ext.declarative import declarative_base
# SQL exp as mapped attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

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
    password = Column(String)
    
    ''' http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html#sqlalchemy.orm.validates
    include_removes = Operation is a removal
    validation() by default doesn't get emitted for collection events
    as typical expectation = value being discarded doesn't require validation
    
    include_backrefs=False where mutually dependent validators are linked
    via a backref
    '''
    addresses = relationship("Address")
    @validates('addresses', include_removes=True)
    def validate_address(self, key, address, is_remove):
        if is_remove:
            raise ValueError("Now allowed to remove items from the collection")
        else:
            assert '@' in address.email
            return address
    
    @hybrid_property
    def fullname(self):
        if self.firstname is not None:
            return self.firstname + " " + self.lastname
        else:
            return self.lastname
    
    # distinguishing between sql/python
    @fullname.expression
    def fullname(cls):
        return case([
            (cls.firstname != None, cls.firstname + " " + cls.lastname),
        ], else_ = cls.lastname)
        
    
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
        
# Relationship & Descriptors and Hybrids
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    _email_address = Column("email", String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User, 
        back_populates="addresses", 
        cascade='delete, all, delete-orphan',
        single_parent=True,
    )
    
    @hybrid_property
    def email_address(self):
        # class level Address.email_address attr doesn't have usual exp semantics with Query
        # hybrid allows behaviour change - when attr accessed instance lvl or class/expr lvl
        return self._email_address[:-12]
        
    @email_address.setter
    def email_address(self, email):
        self._email_address = email + "@example.com"
        
    @email_address.expression
    def email_address(cls):
        return func.substr(cls._email_address, 0, func.length(cls._email_address) - 12)
        
    # address = db_session.query(Address).filter(Address.email_address == 'address').one()
        
    @validates('email_address')
    def validate_email(self, key, address):
        assert '@' in address
        return address
        
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address
        
    '''
    from sqlalchemy.orm import Session
    session = Session()
    address = session.query(Address).\
                    filter(Address.email_address == 'address@exmaple.com').\
                    one()
                    
    address.email_address = 'otheraddr@example.com'
    session.commit()
    '''
        
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
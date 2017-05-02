from sqlalchemy import select, func, Column, Integer, String, ForeignKey
from sqlalchemy.orm import column_property
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('userid'))
    
    
class User(Base):
    __tablename__ = 'user'
    User.address_count = column_property(
        select([func.count(Address.id)]).\
            where(Address.user_id==User.id).\
            correlate_except(Address)
    )
    
'''
select where >correlate_except indicates each ele in FROM may be omitted from 
the FROM list except "Address" - prevents "Address" from  being inadvertently 
omitted in the case a long str of joins User>-<Address where select stmt against
Address are nested
'''

# for many-many use and_ to join fields of the association table to both tables
from sqlalchemy import and_

mapper(Author, authors, properties={
    'book_count': column_property(
        select([func.count(books.c.id)],
            and_(
                book_authors.c.author_id==authors.c.id,
                book_authors.c.book_id==books.c.id
            )
        )
    )
})

# Plain descriptor for when sql > column_property+hybrid_property
from sqlalchemy import select, func
from sqlalchemy.orm import object_session

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    
    @property
    def address_count(self):
        return object_session(self).\
            scalar(
                select([func.count(Address.id)]).\
                    where(Address.user_id==self.id)
            )
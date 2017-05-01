# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying
for instance in db_session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)
# x xx y

for name, fullname in db_session.query(User.name, User.fullname):
    print(name, fullname)
# x xx y
    
for row in db_session.query(User, User.name).all():
    print(row.User, row.name)
# <User(name='x', fullname='xx, y', password='z')> x

from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')
for row in db_session.query(user_alias, user_alias.name).all():
    print(row.user_alias)
# <User(name='x', fullname='xx, y', password='z')>

# Limit and Offset
for u in db_session.query(User).order_by(User.id)[1:3]:
    print(u)
    
# Filters
for user in db_session.query(User).\
            filter(User.name=='x').\
            filter(User.fullname=='xx'):
    print(user)
# <User(name='x', fullname='xx, y', password='z')>


# === Common Filter Operators === #
# EQUALS
query.filter(User.name == 'x')
# NOT EQUALS
query.filter(User.name != 'x')
# LIKE
query.filter(User.name.like('%x%'))
    ### INSENSITIVE
    query.filter(User.name.ilike('%x%'))
# IN
query.filter(User.name.in_(['x', 'y']))
# NOT IN
query.filter(~User.name.in_(['x', 'y']))
# NULL
query.filter(User.name == None) // query.filter(User.name.is_(None))
# NOTNULL
query.filter(User.name != None) // query.filter(User.name.isnot(None))
# AND -- Make sure its and_() and not and
from sqlalchemy import and_
query.filter(and_(User.name == 'x', User.fullname == 'xx'))
query.filter(User.name == 'x', User.fullname == 'xx')
query.filter(User.name == 'x').filter(User.fullname == 'xx')
# OR
from sqlalchemy import or_
query.filter(or_(User.name == 'x', User.name == 'y'))
# MATCH -- uses db-specific match/contains / varies by backend - sqlite etc
query.filter(User.name.match('x'))


# === Returning Lists and Scalars === #
# all() - returns list
# first() - applies limit, returns first as scalar
# one(), one_or_none(), scalar()


# === Querying with Joins === #
# jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
# jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]
# session.add(jack)
# session.commit()
for u, a in db_session.query(User, Address).\
            filter(User.id==Address.user_id).\
            filter(Address.email_address=='jack@google.com').\
            all():
    print(u)
    print(a)
    
db_session.query(User).join(Address).\
            filter(Address.email_address=='jack@google.com').\
            all()
            
query.join(Address, User.id==Address.user_id)   # explicit
query.join(User.addresses)  # specify from left to right
query.join(Address, User.addresses) # same with explicit target
query.join('addresses') # same with string
query.outerjoin(User.addresses) # left outer join

# Aliases and Joins
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-aliases
from sqlalchemy.orm import aliased
adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
        session.query(User.name, adalias1.email_address, adalias2.email_address).\
        join(adalias1, User.addresses).\
        join(adalias2, User.addresses).\
        filter(adalias1.email_address=='jack@google.com').\
        filter(adalias2.email_address=='j25@yahoo.com'):
    print(username, email1, email2)
# jack jack@google.com j25@yahoo.com

# Subqueries
from sqlalchemy.sql import func
stmt = db_session.query(Address.user_id, func.count('*').\
        label('address_count')).\
        group_by(Address.user_id).subquery()
        
for u, count in db_session.query(User, stmt.c.address_count).\
                outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
    print(u, count)
    
# Exists
from sqlalchemy.sql import exists
stmt = exists().qhere(Address.user_id==User.id)
for name, in db_session.query(User.name).filter(stmt):
    print(name)
    
    
# Common Relationship Operators
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-relationship-operators
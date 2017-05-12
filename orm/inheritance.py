''' Mapping Class Inheritance Hierarchies
SQLAlchemy supports
single table inheritance - several types of classes represented by a single table
concrete table inheritance - each type class represented by independent tables
joined table inheritance - class hierarchy is broken up among dependent tables
    each class represented by its own table that only includes those attr local to
    that class
    
when mappers are config'd in an inheritance relationship, SQLAlchemy can load
elements polymorphically = single query return multiple types
'''

# Joined Table Inheritance 
# http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#joined-table-inheritance
'''
each class along class' list of parents is represented by a unique table
total set of attr for an instance is represented as a join along all tables in
    its inheritance path
    
define class Employee() that contains pk and col for each attr represented by Employee
    =   name
mapped tbl also has type acting as a discriminator, stores val which indicates 
    type of obj represented within the row (datatype, str, int)
'''
class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_identity':'employee',
        'polymorphic_on':type,
        'with_polymorphic':'*',
    }
    
'''
discriminator col only needed if you want polymorphic loading

defined Engineer & Employee where each col that represent attr unique to 
    the subclass they represent
each tbl also must contain pk col(s), and in most cases a fk ref to the parent tbl

with_polymorphic('*')
'''

class Engineer(Employee):
    __tablename__ = 'engineer'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    engineer_name = Column(String(30))
    
    __mapper_args__ = {
        'polymorphic_identity':'engineer'
    }
    
    
class Manager(Employee):
    __tablename__ = 'manager'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    manager_name = Column(String(30))
    
    __mapper_args__ = {
        'polymorphic_identity':'manager'
    }
    
'''
orm.with_polymorphic() and Query.with_polymorphic() affects the specific tbl
    which the Quest selects from where orm is more flexible
    
db_session.query(Employee).all()
#    select x from employee;
    
from sqlalchemy.orm import with_polymorphic
eng_plus_manager = with_polymorphic(Employee, [Engineer, Manager])
query = db_session.query(eng_plus_manager)      or (query.all())

# orm.with_polymorphic() returns AliasedClass obj
query = db_session.query(eng_plus_manager).filter(
    or_(
        eng_plus_manager.Engineer.engineer_info=='x',
        eng_plus_manager.Manager.manager_data=='y'
    )
)
'''

# join to the engineer table
entity = with_polymorphic(Employee, Engineer)

# join to the engineer and manager tables
entity = with_polymorphic(Employee, [Engineer, Manager])

# join to all subclass tables
entity = with_polymorphic(Employee, '*')

# use the 'entity' with a Query obj
db_session.query(entity).all()

# custom selectable
employee = Employee.__table__
manager = Manager.__table__
engineer = Engineer.__table__
entity = with_polymorphic(
    Employee,
    [Engineer, Manager],
    employee.outerjoin(manager).outerjoin(engineer)
)

# use entity with query
db_session.query(entity).all()

db_session.query(Employee).with_polymorphic([Engineer, Manager]).\
    filter(or_(Engineer.engineer_info=='w', Manager.manager_data=='q'))
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MyClass(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    job_status = Column(String(50))
    
    status = synonym("job_status")
    
# .job_status and .status will behave as one attr at the expression level
print(MyClass.job_status == 'some_status')
print(MyClass.status == 'some_status')
my_table.job_status = :job_status_1

# .job_status and .status at the instance level
m1 = MyClass(status='x')
m1.status, m1.job_status
# ('x', 'x')

m1.job_status = 'y'
m1.status, m1.job_status
# ('y', 'y')

'''
synonym() can be used for any kind of mapped attr that subclasses MapperProperty
including mapped cols, relationships, and synonyms
'''

# synonym() can ref user-defined descriptor
class MyClass(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    
    @property
    def job_status(self):
        return "Status:" + self.status
        
    job_status = synonym("status", descriptor=job_status)
    
# when using Declarative
    from sqlalchemy.ext.declarative import synonym_for
    #...
    @synonym_for("status")
    @property
    def job_status(self):
        return "Status: " + self.status
        
        
'''
synonym() = good for simple mirroring
the use case of augmenting attr behaviour with descriptors is better handled with hybrid

http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html#operator-customization
column_property, relationship, composite -> PropComparator -> comparator_factory
'''
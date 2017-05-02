''' Composite Column Types
sets of cols can be associated with a single user-defined datatype
ORM provices a single attr which represents the group of cols using the class you provide
'''

''' Pairs of cols as Point obj - represents pair as .x .y
-   accepts x, y
-   provides method __composite_values__() returns< 
        state of obj as list/tuple
        in order of col-based attr
-   should also supply adequate __eq__() and __ne__() which test equality of 2 instances
'''
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __composite_values__(self):
        return self.x, self.y
        
    def __repr__(self):
        return "Point(x=%r, y=%r)" % (self.x, self.y)
        
    def __eq__(self, other):
        return isinstance(other, Point) and \
            other.x == self.x and \
            other.y == self.y
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
        
'''
Create mapping to tbl_vertices which represents x1/y1 & x2/y2
created with Column(), then composite() assigns new attr that represents 
    sets of cols via class Point()
'''        
from sqlalchemy import *
from sqlalchemy.orm import composite, mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.properties import CompositeProperty

Base = declarative_base()

'''
equals by default produces AND and can be changed with composite(comparator_factory)
where we specify a custom class CompositeProperty.Comparator() to define existing/new operations
# below: greater than operator, implementing the same expr. that the base greater than does
'''
class PointComparator(CompositeProperty.Comparator):
    def __gt__(self, other):
        # redefine the > operation
        return sql.and_(*[a>b for a, b in zip(
            self.__clause_element__().clauses,
            other.__composite_values__()
        )])
    
    
class Vertex(Base):
    __tablename__ = 'vertices'
    id = Column(Integer, primary_key=True)
    x1 = Column(Integer)
    y1 = Column(Integer)
    x2 = Column(Integer)
    y2 = Column(Integer)
    
    # original > start = composite(Point, x1, y1) / end = composite(Point, x2, y2)
    # comparator_factory
    start = composite(Point, x1, y1, comparator_factory=PointComparator)
    end = composite(Point, x2, y2, comparator_factory=PointComparator)
    
    
# classical mapping above would define each composite() against existing tbl
mapper(Vertex, vertices_table, properties={
    'start':composite(Point, vertices_table.c.x1, vertices_table.c.y1),
    'end':composite(Point, vertices_table.c.x2, vertices_table.c.y2),
})
'''
v = Vertex(start=Point(3,4), end=Point(5, 6))
db_session.add(v)
q = db_session.query(Vertex).filter(Vertex.start == Point(3,4))
print(q.first().start)

# Point(x=3, y=4)
'''
    
'''
inplace changes to existing composite are not tracked automatically and needs
to provide events to its parent obj explicitly

Automated by MutableComposite (later)
'''
# Automating column naming schemes from reflected tables
@event.listens_for(Table, "column_reflect")
def column_reflect(inspector, table, column_info):
    # If we want to qualify out event to only react to the specific MetaData
    if table.metadata is Base.metadata:
        # set column.key = "attr_<lower case name>"
        column_info['key'] = "attr_%s" % column_info['name'].lower()
    

# Reflection of column obj will be intercepted with the event that adds a new .key    
class MyClass(Base):
    __table__ = Table("some_table", Base.metadata, autoload=True, autoload_with=some_engine)
    
    
# Naming all cols with a prefix
class User(Base):
    __table__ = user_table
    __mapper_args__ = {'column_prefix': '_'}
    
    
# Mapping a subset of table col - will only include id and name
# can accurately describe cols even with joins
class User(Base):
    __table__ = user_table.join(addresses_table)
    __mapper_args__ = {
        'exclude_properties': [address_table.c.id],
        # 'include_properties': ['user_id', 'user_name'],
        'primary_key': [user_table.c.id]
    }
    

# will map all cols except the exclude_properties
class Address(Base):
    __table__ = address_table
    __mapper_args__ = {
        'exclude_properties': ['street', 'city', 'state', 'zip']
    }
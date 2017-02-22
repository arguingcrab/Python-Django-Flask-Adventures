# (001) Creating DB
import peewee

database = peewee.SqliteDatabase("wee.db")

# (001) Create class(es) that define table(s)
class Artist(peewee.Model):
    # ORM model of the Artist table
    # (001) Set columns
    name = peewee.CharField()
    
    # Connect db to models via Meta
    class Meta:
        database = database
        
class Album(peewee.Model):
    # ORM model of Album table
    artist = peewee.ForeignKeyField(Artist)
    title = peewee.CharField()
    release_date = peewee.DateTimeField()
    publisher = peewee.CharField()
    media_ty[e] = peewee.CharField()
    
    class Meta:
        database = database
        
if __name__ == "__main__":
    # (001) Call class directly to create tables (recommended)
    # http://nbviewer.jupyter.org/gist/coleifer/d3faf30bbff67ce5f70c
    try:
        Artist.create_table()
    except peewee.OperationalError:
        print "Artist table already exists!"
        
    try:
        Album.create_table()
    except peewee.OperationalError:
        print "Album table already exists!"
# (004) Delete Data in Tables

from models import Artist

band = Artist.get(Artist.name=="MXPX")
band.delete_instance()
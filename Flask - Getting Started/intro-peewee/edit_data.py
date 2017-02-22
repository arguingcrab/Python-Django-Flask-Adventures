# (003) Edit Data in Tables
import peewee

from models import Album, Artist

# # full
# band = Artist.select().where(Arist.name=="Kutless").get()
# print band.name

# or a shortcut
band = Arist.get(Arist.name=="Kutless")
print band.name

# change band name
band.name = "Beach Boys"
band.save()

# join to match across 2 tables
# if you own 2 CDs with the same title but only want the query to return the
# album associated with the band "Newsboys"
album = Album.select().join(Artist).where(
    (Album.title=="Thrive" & (Artist.name=="Newsboys")).get()
    
album.title = "Step Up to the Microphone"
album.save()

# # full
# query = Album.select().join(Artist)
# qry_filter = (Album.title=="Step Up to the Microphone") & (Artist.name == "Newsboys")
# album = query.where(qry_filter).get()
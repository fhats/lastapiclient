from google.appengine.ext import db

class Song(db.Model):
    #A simple string
    name = db.StringProperty(required = True)
    #A reference to some Artist data model
    artist = db.ReferenceProperty(Artist, required = True)
    
    album = db.StringProperty(required = True)
    
    #String property that is used like an enum
    genre = db.StringProperty(required = True,
                              choices = set(["rock",
                                             "pop",
                                             "jazz",
                                             "country",
                                             "R&B",
                                             "hip hop",
                                             "world",
                                             "post-swing"])
                                             
    #List support at the DB level
    tags = db.StringListProperty()
    
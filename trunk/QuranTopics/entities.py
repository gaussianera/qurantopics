from google.appengine.ext import db

class Sura(db.Model):
    number = db.IntegerProperty()
    name = db.StringProperty()
    number_of_ayat = db.IntegerProperty()
  
class Aya(db.Model):
    sura = db.ReferenceProperty(Sura) 
    number = db.IntegerProperty()
    content = db.TextProperty()
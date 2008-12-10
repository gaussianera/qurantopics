from google.appengine.ext import db

class Sura(db.Model):
    number = db.IntegerProperty()
    name = db.StringProperty()
    number_of_ayat = db.IntegerProperty()
    
    @staticmethod
    def get_by_number(sura_number):
        return Sura.gql("WHERE number = :number ", number = sura_number).fetch(1)[0]
    
    def get_ayat_query_in_range(self, from_aya, to_aya):
        ayat = self.aya_set
        ayat.filter('number >=', from_aya)
        ayat.filter('number <=', to_aya)
        ayat.order('number')
        return ayat

    def get_aya_by_number(self, aya_number):
        ayat = self.aya_set
        ayat.filter('number =', aya_number)
        return ayat.fetch(1)[0]

  
class Aya(db.Model):
    sura = db.ReferenceProperty(Sura) 
    number = db.IntegerProperty()
    content = db.TextProperty()
    
    @staticmethod
    def get_by_sura_and_aya_number(sura_number, aya_number):
        sura = Sura.get_by_number(sura_number)
        return sura.get_aya_by_number(aya_number)
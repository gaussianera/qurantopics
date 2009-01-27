from google.appengine.ext import db
from google.appengine.ext import search

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


class Topic(search.SearchableModel):

    topic_id = db.IntegerProperty()
    title = db.StringProperty()
    ayat_keys = db.ListProperty(db.Key)
    created_by = db.UserProperty()

    
    @staticmethod
    def get_by_id(topic_id):
        return Topic.gql("WHERE topic_id = :id ", id = topic_id).fetch(1)[0]

    
    @staticmethod
    def remove_by_id(topic_id):
        topic = Topic.get_by_id(topic_id)
        Topic.delete(topic)


    @staticmethod
    def delete(topic):
        db.delete(topic)
    
    
    def get_ayat(self):
        return db.get(self.ayat_keys)


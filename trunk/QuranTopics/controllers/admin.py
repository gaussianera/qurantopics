# coding: utf8

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from controllers.entities import Sura, Aya, Topic
from controllers.page_controller import PageController



class RemoveSura(webapp.RequestHandler):

    def get(self):
        sura_number = int(self.request.get('sura'))
        sura = Sura.gql("WHERE number = :number ", number = sura_number).fetch(1)[0]
        db.delete(sura.aya_set)


class ReputSura(webapp.RequestHandler):

    def get(self):
        sura_number = int(self.request.get('sura'))
        sura = Sura.gql("WHERE number = :number ", number = sura_number).fetch(1)[0]
        ayat = Aya.gql("where sura = :sura", sura = sura).fetch(1000)
        for aya in ayat:
            db.put(aya)
        self.response.out.write ("reput num of ayat: " + str(len(ayat)))
        

class EditAya(PageController):

    def perform_get(self):
        sura_number = int(self.request.get('sura'))
        aya_number = int(self.request.get('aya'))
        
        return self.display_page(sura_number, aya_number)
        
        
    def display_page(self, sura_number, aya_number):
        
        sura = Sura.get_by_number(sura_number)
        ayat = sura.aya_set
        ayat.filter('number =', aya_number)
        ayat = ayat.fetch(1000)

        aya_topics = []
        for aya in ayat:
            aya_topics.append("مفتاح = " + str(aya.key()));
            topics = self.get_topics_for_aya(aya)
            for topic in topics:
                aya_topics.append("موضوع = " + str(topic.topic_id))
        
        
        self.template_values['aya'] = ayat[0]
        self.template_values['aya_topics'] = aya_topics
        self.template_values['ayat'] = ayat
        self.template_values['show_delete'] = len(ayat) > 1
 
        return 'edit_aya.html'
    
        
    def perform_post(self):
        if (self.request.get('edit')):
            aya_key = self.request.get('aya_key')
            aya = db.get(aya_key)
            aya.content = self.request.get('aya_content')
            db.put(aya)
            return self.display_page(aya.sura.number, aya.number)
        
        elif (self.request.get('delete')):
            aya_key = self.request.get('aya_key')
            aya = db.get(aya_key)
            topics = self.get_topics_for_aya(aya)
            if len(topics) == 0:
                db.delete(aya)
            return self.display_page(aya.sura.number, aya.number)
        
        
    def get_topics_for_aya(self, aya):
        return Topic.gql("WHERE ayat_keys = :aya_key ", aya_key = aya.key()).fetch(1000)



application = webapp.WSGIApplication(
                                     [('/admin/remove_sura', RemoveSura),
                                      ('/admin/reput_sura', ReputSura),
                                      ('/admin/edit_aya', EditAya)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()
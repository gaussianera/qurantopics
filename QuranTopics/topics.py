import cgi

import os
import logging
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from view_objects import TopicEditView, TopicAya
from entities import Sura, Aya

class CreateNewTopic(webapp.RequestHandler):
    def get(self):
    
        template_values = {
          }
    
        path = os.path.join(os.path.dirname(__file__), 'edit_topic.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

        topics_edit_view = self.populate_view()
        selected_ayat = topics_edit_view.ayat_display
        logging.debug("after populaing")    

        if (self.request.get('add')):
            logging.debug("in add")    
            sura = Sura.get_by_number(topics_edit_view.sura)
            ayat = sura.get_ayat_query_in_range(topics_edit_view.from_aya, topics_edit_view.to_aya)
            added_ayat = self.make_ayat_display_from_ayat(ayat)
            self.merge_added_ayat_to_topic_ayat(selected_ayat, added_ayat)
        else:
            logging.info("not in add")

        ayat = self.make_ayat_from_ayat_display(selected_ayat)
        
        template_values = {
           'ayat': ayat
          }
    
        path = os.path.join(os.path.dirname(__file__), 'edit_topic.html')
        self.response.out.write(template.render(path, template_values))
        
    def populate_view(self):
        topics_edit_view = TopicEditView()
        topics_edit_view.title = self.request.get('title')
        topics_edit_view.sura = int(self.request.get('sura'))
        topics_edit_view.from_aya = int(self.request.get('from_aya'))
        topics_edit_view.to_aya = int(self.request.get('to_aya'))
        self.populate_ayat(topics_edit_view)
        return topics_edit_view

    def populate_ayat(self, topics_edit_view):
        count = 0
        ayat_display = []
        while (self.request.get("sura_" + str(count))):
            topic_aya = TopicAya()
            topic_aya.sura_number = self.get_sura(count)
            topic_aya.aya_number = self.get_aya(count)
            ayat_display.append(topic_aya)
            count = count + 1
        
        logging.debug("populated ayat display with " + str(len(ayat_display)) + " items")    
        topics_edit_view.ayat_display = ayat_display
        
    
    def make_ayat_display_from_ayat(self, ayat):
        ayat_display = []
        for aya in ayat:
            aya_display = TopicAya()
            aya_display.sura_number = aya.sura.number
            aya_display.aya_number = aya.number
            ayat_display.append(aya_display)
        return ayat_display

            
    def make_ayat_from_ayat_display(self, ayat_display):
        logging.debug("start: make_ayat_from_ayat_display")    
        ayat = []
        for aya_display in ayat_display:
            aya = Aya.get_by_sura_and_aya_number(aya_display.sura_number, aya_display.aya_number)
            ayat.append(aya)
        logging.debug("end: make_ayat_from_ayat_display")    
        return ayat
            
    
    def merge_added_ayat_to_topic_ayat(self, topic_ayat, added_ayat):
        ayat_to_add = []
        for aya_display in added_ayat:
            if not self.list_contains_aya(topic_ayat, aya_display):
                ayat_to_add.append(aya_display)
        topic_ayat.extend(ayat_to_add)
    
    
    def list_contains_aya(self, ayat_display, aya_display):
        for list_aya in ayat_display:
            if self.same_aya(list_aya, aya_display):
                return True
        return False
    
    
    def same_aya(self, aya1, aya2):
        return aya1.sura_number == aya2.sura_number and aya1.aya_number == aya2.aya_number    
    
    def get_sura(self, order):
        return int(self.request.get("sura_" + str(order)))
    

    def get_aya(self, order):
        return int(self.request.get("aya_" + str(order)))



application = webapp.WSGIApplication(
                                     [('/topics/add_edit', CreateNewTopic)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()
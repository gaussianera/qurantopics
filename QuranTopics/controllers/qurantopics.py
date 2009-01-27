import cgi
import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from controllers.entities import Sura, Topic
from controllers.page_controller import PageController




class MainPage(PageController):
    def perform_get(self):
        topics = Topic.all()
        self.template_values['topics'] = topics
        return 'index.html'


class SurasListPage(PageController):
    def perform_get(self):
        suras = Sura.gql("order by number").fetch(114)
        self.template_values['suras'] = suras
        return 'suras_list.html'


class SurasDisplayPage(PageController):
    def perform_get(self):
        leading_length = len('/display_sura/')
        sura_number = int(self.request.path[leading_length:])
        sura = Sura.gql("WHERE number = :number ", number = int(sura_number)).fetch(1)[0]
        ayat = sura.aya_set
        ayat.order('number')

        self.template_values['sura'] = sura
        self.template_values['ayat'] = ayat
        
        return 'sura_display.html'


class SearchTopics(PageController):
    def perform_get(self):
        return "/"

    def perform_post(self):
        search_for = self.request.get('search_for')
        topics = Topic.all().search(search_for)

        self.template_values['topics'] = topics
        
        return 'search_results.html'


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/list_suras', SurasListPage),
                                      ('/display_sura/.*', SurasDisplayPage),
                                      ('/search', SearchTopics)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()
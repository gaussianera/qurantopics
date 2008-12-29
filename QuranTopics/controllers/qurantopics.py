import cgi

import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from controllers.entities import Sura, Topic
from controllers.page_controller import PageController




class MainPage(PageController):
    def get(self):
        topics = Topic.all()
        
        template_values = {
           'topics' : topics
         }

        path = self.get_view_path('index.html')
        self.response.out.write(template.render(path, template_values))


class SurasListPage(PageController):
  def get(self):

    suras = Sura.gql("order by number").fetch(114)

    template_values = {
      'suras': suras
      }

    path = self.get_view_path('suras_list.html')
    self.response.out.write(template.render(path, template_values))


class SurasDisplayPage(PageController):
  def get(self):

    sura_number = self.request.get('sura')
    sura = Sura.gql("WHERE number = :number ", number = int(sura_number)).fetch(1)[0]
    ayat = sura.aya_set
    ayat.order('number')

    template_values = {
      'sura': sura,
      'ayat': ayat
      }

    path = self.get_view_path('sura_display.html')
    self.response.out.write(template.render(path, template_values))




application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/list_suras', SurasListPage),
                                      ('/display_sura', SurasDisplayPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
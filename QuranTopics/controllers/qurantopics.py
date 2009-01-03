import cgi

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
        sura_number = self.request.get('sura')
        sura = Sura.gql("WHERE number = :number ", number = int(sura_number)).fetch(1)[0]
        ayat = sura.aya_set
        ayat.order('number')

        self.template_values['sura'] = sura
        self.template_values['ayat'] = ayat

        return 'sura_display.html'


class Login(PageController):
    def get(self):
        user = users.get_current_user()
        self.redirect(users.create_login_url(self.request.uri))


class Logout(PageController):
    def get(self):
        user = users.get_current_user()
        self.redirect(users.create_logout_url('/'))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/list_suras', SurasListPage),
                                      ('/display_sura', SurasDisplayPage),
                                      ('/login', Login),
                                      ('/logout', Logout)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
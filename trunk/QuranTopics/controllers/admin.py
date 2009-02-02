import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from controllers.entities import Sura, Aya


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
        


application = webapp.WSGIApplication(
                                     [('/admin/remove_sura', RemoveSura),
                                      ('/admin/reput_sura', ReputSura)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()
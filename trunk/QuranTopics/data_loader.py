import cgi
import csv
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from entities import Sura, Aya

class SurasLoader(webapp.RequestHandler):
  def get(self):
      if database_has_suras():
          print "Suras are already loaded. Not performing load."
          return

      reader = csv.reader(open("./docs/data/suras_info_utf8.csv", "rb"))
      for row in reader:
          sura = Sura()
          sura.number = int(row[0])
          sura.name = unicode(row[1], 'utf-8')
          sura.number_of_ayat = int(row[2])
          sura.put()
    
      print "done loading suras" 

def database_has_suras():
    return len(Sura.all().fetch(1)) == 1

def database_has_ayat():
    return len(Aya.all().fetch(1)) == 1

class AyatLoader(webapp.RequestHandler):
  def get(self):
      if database_has_ayat():
          print "Ayat are already loaded. Not performing load."
          return

      for i in range(1, 115):
          sura = Sura.gql("WHERE number = :number ", number = i).fetch(1)[0]
          file_name = "./docs/data/" + str(i) + ".txt"
          reader = csv.reader(open(file_name, "rb"))
          logging.info("processing sura #" + str(i))
          count = 1
          for row in reader:
              aya = Aya()
              aya.sura = sura
              aya.number = count
              aya.content = unicode(row[0], 'utf-8')
              aya.put()
              count = count + 1
      
      print "done loading ayat" 



application = webapp.WSGIApplication(
                                     [('/load/suras', SurasLoader),
                                      ('/load/ayat', AyatLoader)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
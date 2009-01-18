import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from controllers.create_or_edit_topic import CreateOrEditTopic
from controllers.view_topic import ViewTopic

        
application = webapp.WSGIApplication(
                                     [('/topics/add_edit', CreateOrEditTopic),
                                      ('/topics/view/.*', ViewTopic)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()
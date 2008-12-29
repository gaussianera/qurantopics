import os
from google.appengine.ext import webapp

class PageController(webapp.RequestHandler):
    
    def get_int(self, name):
        value = self.request.get(name)
        if (value): return int(value)
        return None
    
    def get_view_path(self, page_name):
        return os.path.join(os.path.dirname(__file__) + "/../views/", page_name)
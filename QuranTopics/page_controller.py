from google.appengine.ext import webapp

class PageController(webapp.RequestHandler):
    
    def get_int(self, name):
        value = self.request.get(name)
        if (value): return int(value)
        return None

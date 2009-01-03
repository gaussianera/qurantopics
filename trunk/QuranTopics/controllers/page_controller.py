import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

class PageController(webapp.RequestHandler):
    
    template_values = {}
    
    def get(self):
        self.template_values = {}
        self.set_user()
        view = self.perform_get()
        self.display_view(view)
        
        
    def post(self):
        self.template_values = {}
        self.set_user()
        view = self.perform_post()
        self.display_view(view)
        

    def set_user(self):
        user = users.get_current_user()
        if user:
            self.template_values['user_nickname'] = user.nickname()
            user_link = users.create_logout_url('/')
        else:
            user_link = users.create_login_url(self.request.uri)

        self.template_values['user_link'] = user_link
            
    
    def display_view(self, view):
        path = self.get_view_path(view)
        self.response.out.write(template.render(path, self.template_values))
    

    def get_view_path(self, page_name):
        return os.path.join(os.path.dirname(__file__) + "/../views/", page_name)
    
    
    def get_int(self, name):
        value = self.request.get(name)
        if (value): return int(value)
        return None
    

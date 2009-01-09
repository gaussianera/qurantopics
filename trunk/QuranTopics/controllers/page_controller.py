import os
import logging
import traceback
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from controllers.exceptions import *

class PageController(webapp.RequestHandler):
    
    template_values = {}
    user = None
    
    def get(self):
        self.perform_action(self.perform_get)
        
        
    def post(self):
        self.perform_action(self.perform_post)

    
    def perform_action(self, action):
        self.template_values = {}
        self.set_user()
        try:
            view = action()
            self.display_view(view)
        except UserAuthException, message:
            logging.debug("User authorization error: " + str(message))
        

    def set_user(self):
        user = users.get_current_user()
        if user:
            self.user = user
            self.template_values['user'] = user.nickname()
            user_link = users.create_logout_url('/')
        else:
            user_link = users.create_login_url(self.request.uri)

        self.template_values['user_link'] = user_link
            
    
    def display_view(self, view):
        path = self.get_view_path(view)
        self.response.out.write(template.render(path, self.template_values))
    

    def get_view_path(self, page_name):
        return os.path.join(os.path.dirname(__file__) + "/../views/", page_name)
    
    
    def require_login(self):
        if not self.user:
            self.redirect(users.create_login_url(self.request.uri))
            raise NoUserLoggedIn
    
    def require_user(self, user):
        if not users.is_current_user_admin() and self.user != user:
            self.redirect('/')
            raise UserNotPermittedToPerformOperation, self.user.email()
                         

    def get_int(self, name):
        value = self.request.get(name)
        if value.isdigit() and len(value) < 5 and len(value) > 0:
            return int(value)
        return None
    

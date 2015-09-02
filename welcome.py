import webapp2
import cgi
from head import fold

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        username = cgi.escape(username, quote = True) 
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(fold('Hello, %s!'%username))

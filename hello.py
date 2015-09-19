import webapp2
from head import adr
from head import fold

title = "Hello World"
page = 'Hello, World!'
class HelloPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(fold(page,title))

from head import debug
app = webapp2.WSGIApplication([    
    (adr['hello'], HelloPage),
], debug=debug)

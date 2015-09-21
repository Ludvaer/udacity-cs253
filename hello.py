import webapp2
import head

title = "Hello World"
page = 'Hello, World!'
class HelloPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(head.fold(page,title))

from head import debug
app = webapp2.WSGIApplication([    
    (head.adr['hello'], HelloPage),
], debug=head.debug)

import webapp2
from head import backLinkString
from head import helloAdr

class HelloPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Hello, World!' + backLinkString)


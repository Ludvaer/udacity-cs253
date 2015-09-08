import webapp2
from head import adr

from main import MainPage
from hello import HelloPage
from rot13 import Rot13Page
from signUp import SignUpPage
from welcome import WelcomePage
from blog import BlogPage

app = webapp2.WSGIApplication([    
    (adr['hello'], HelloPage),
    (adr['rot13'], Rot13Page),
    (adr['signUp'], SignUpPage),
    (adr['welcome'], WelcomePage),
    (adr['blog'], BlogPage),
], debug=True)

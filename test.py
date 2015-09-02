import webapp2
from head import helloAdr
from head import rot13adr
from head import signUpAdr
from head import welcomeAdr

from indexPage import MainPage
from helloWorld import HelloPage
from rot13 import Rot13Page
from signUp import SignUpPage
from welcome import WelcomePage

app = webapp2.WSGIApplication([
    ('/', MainPage),
    (helloAdr, HelloPage),
    (rot13adr, Rot13Page),
    (signUpAdr, SignUpPage),
    (welcomeAdr, WelcomePage),
], debug=True)

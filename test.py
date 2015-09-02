import webapp2
from head import helloadr
from head import rot13adr
from mainPage import MainPage
from helloWorld import HelloPage
from rot13 import Rot13Page

app = webapp2.WSGIApplication([
    ('/', MainPage),
    (helloadr, HelloPage),
    (rot13adr, Rot13Page),
], debug=True)

import webapp2
from google.appengine.api import app_identity

helloAdr = "/hello"
rot13adr = "/rot13"
signUpAdr = "/signup"
welcomeAdr = "/welcome"

backLinkString ='<br> <a href="http://%s">home</a>'%app_identity.get_default_version_hostname()

def fold(s):
    return s+backLinkString;

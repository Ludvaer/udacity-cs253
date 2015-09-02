import webapp2
from google.appengine.api import app_identity

helloadr = "/hello"
rot13adr = "/rot13"

backlinkstring ='<br> <a href="http://%s">back</a>'%app_identity.get_default_version_hostname()

import webapp2
import cgi
import crypto
from google.appengine.ext import db
from head import adr
from head import fold
from signUp import getNewUser

title = "welcome"

def getPepper(username):
    #attempt to avoid reading from database befor wrighting completed
    newUser = getNewUser()
    if(newUser and newUser.name == username):
        return newUser.pepper
    users = db.GqlQuery("SELECT * FROM User WHERE name = '%s'"%username)
    for user in users:
        return str(user.pepper)
    return None


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        username = cgi.escape(username, quote = True) 
        userCookie = self.request.cookies.get('user', None)
        usernamec = crypto.unbake(userCookie,getPepper)
        self.response.headers['Content-Type'] = 'text/html'      
        if(usernamec):
            self.response.write(fold('Hello, %s!'%usernamec,title))
        else:
            self.redirect(adr['signup']);

app = webapp2.WSGIApplication([    
    (adr['welcome'], WelcomePage),
], debug=True)

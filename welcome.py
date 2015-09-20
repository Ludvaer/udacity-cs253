import webapp2
import user
from head import adr
from head import fold


title = "welcome"


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        #username = self.request.get("username")
        #username = cgi.escape(username, quote = True) 
        userCookie = self.request.cookies.get('user', None)
        username = user.unbake(userCookie)
        #username = crypto.unbake(userCookie,getPepper)
        self.response.headers['Content-Type'] = 'text/html'      
        if(username):
            self.response.write(fold('Hello, %s!'%username,title))
        else:
            self.redirect(adr['signup']);

app = webapp2.WSGIApplication([    
    (adr['welcome'], WelcomePage),
], debug=True)

import webapp2
import user
import head

title = "welcome"


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        userCookie = self.request.cookies.get('user', None)
        username = user.unbake(userCookie)
        self.response.headers['Content-Type'] = 'text/html'      
        if(username):
            self.response.write(head.fold('Hello, %s!'%username,title))
        else:
            self.redirect(head.adr['signup']);

app = webapp2.WSGIApplication([    
    (head.adr['welcome'], WelcomePage),
], debug = head.debug)

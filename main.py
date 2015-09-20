import webapp2
from head import adr
from head import fold
from head import projectName

mainpaige = """
<ul>
<li><a href="%(hello)s">Hello, World</a></li>
<li><a href="%(rot13)s">Rot 13</a></li>
<li><a href="%(signup)s">Sign Up</a></li>
<li><a href="%(signin)s">Log In</a></li>
<li><a href="%(signout)s">Log Out</a></li>
<li><a href="%(blog)s">Blog</a></li>
</ul>
"""%adr


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(fold(mainpaige,noHomeLink = True))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

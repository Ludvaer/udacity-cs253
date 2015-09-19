import webapp2
from head import adr
from head import fold
from head import projectName

mainpaige = """
<ul>
<li><a href="%(hello)s">Hello, World</a> <br></li>
<li><a href="%(rot13)s">Rot 13</a> <br></li>
<li><a href="%(signUp)s">Sign Up</a> <br></li>
<li><a href="%(blog)s">Blog</a> <br></li>
</ul>
"""%adr


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(fold(mainpaige,noHomeLink = True))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

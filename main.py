import webapp2
import head

mainpaige = """
<nav>
<h6>Udacity related pages:</h6>
<ul>
<li><a href="%(hello)s">Hello, World</a></li>
<li><a href="%(rot13)s">Rot 13</a></li>
<li><a href="%(signup)s">Sign Up</a></li>
<li><a href="%(signin)s">Log In</a></li>
<li><a href="%(signout)s">Log Out</a></li>
<li><a href="%(blog)s">Blog</a></li>
</ul>
<h6>Experimental:</h6>
<ul>
<li><a href="%(timer)s">Timer</a></li>
</ul>
</nav>
"""%head.adr


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(head.fold(mainpaige,noHomeLink = True))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=head.debug)
 
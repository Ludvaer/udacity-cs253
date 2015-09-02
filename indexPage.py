import webapp2
from head import helloAdr
from head import rot13adr
from head import signUpAdr



mainpaige = """
<a href="%(hello)s">Hello, World</a> <br>
<a href="%(rot13)s">Rot 13</a> <br>
<a href="%(signup)s">Sign Up</a> <br>
"""%{"hello":helloAdr, "rot13":rot13adr, "signup":signUpAdr}


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(mainpaige)


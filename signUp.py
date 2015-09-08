import webapp2
import cgi
import re
from welcome import WelcomePage
from head import fold
from head import adr
from head import projectName

title = "Sign Up stub page "

form = """
<form method="post">
 <label><h>Sign Up</h></label>
 <input type=input name="username" value="%(name)s">
 <label class="error">%(nameerr)s</label><br>

 <label>Password</label>
 <input type=password name="password" >
 <label class="error">%(pswerr)s</label><br>

 <label>Verify password</label>
 <input type=password name="verify" >
 <label class="error">%(vererr)s</label><br>

 <label>E mail</label>
 <input type=input name="email" value="%(mail)s">
 <label class="error">%(mailerr)s</label><br>

 <input type=submit value="Sign Up">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PSW_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


class SignUpPage(webapp2.RequestHandler):
    def validUsername(self, username):
        return USER_RE.match(username)
    def validPsw(self, psw):
        return PSW_RE.match(psw)
    def validMail(self, mail):
        return MAIL_RE.match(mail)
    def write_form(self,name = "", mail="", nameerr="", pswerr="", vererr="", mailerr="",):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(fold(form%{"name":name, "mail":mail, "nameerr":nameerr, "pswerr":pswerr, "vererr":vererr, "mailerr":mailerr},title))
    def get(self):
        self.write_form()
    def post(self):
        username = self.request.get("username")
        email = self.request.get("email")
        psw =  self.request.get("password")   
        psw2 =  self.request.get("verify")
        if(self.validUsername(username)):
            nameerr = ""
        else:
            nameerr = "Invalid username."
        if(self.validPsw(psw)):
            pswerr = ""
            if(psw==psw2):
                vererr = ""
            else:
                vererr = "Passwords do not match."
        else:
            vererr = ""
            pswerr = "Invalid password."
        if(self.validMail(email)):
            mailerr = ""
        else:
            mailerr = "Invalid mail."
        
        if(nameerr == "" and pswerr=="" and vererr=="" and mailerr==""):
            self.redirect(adr['welcome'] + "?username=" + username)
        else:
            username = cgi.escape(username, quote = True)            
            email = cgi.escape(email, quote = True)
            self.write_form(username,email,nameerr,pswerr,vererr,mailerr)


app = webapp2.WSGIApplication([    
    (adr['signUp'], SignUpPage),
    (adr['welcome'], WelcomePage),
], debug=True)

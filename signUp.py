import webapp2
import jinja2
import re
import head
import user
from jinja2 import Template


title = "Sign Up "

page = """
 <label><h1>{% if isSignup %}Sign Up{% else %}Sign In{% endif %}</h1></label>
 <form method="post">
   <label>Name</label>
   <input type=input name="username" value="{{name|e}}">
   <label class="error">{{nameerr}}</label>
 
   <label>Password</label>
   <input type=password name="password" >
   <label class="error">{{pswerr}}</label>
 
   {% if isSignup %}

   <label>Verify password</label>
   <input type=password name="verify" >
   <label class="error">{{vererr}}</label>
 
   <label>E mail (now optional)</label>
   <input type=input name="email" value="{{mail|e}}">
   <label class="error">{{mailerr}}</label>

   {% endif %}

   <input type=submit value="{% if isSignup %}Sign Up{% else %}Sign In{% endif %}">
</form>
"""
template = Template(page);

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PSW_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class SignPage(webapp2.RequestHandler):
    def write(self,**params):
        self.response.headers['Content-Type'] = 'text/html'
        c = template.render(params)
        self.response.write(head.fold(c,title))
    def write_form(self,name = "", mail="", nameerr="", pswerr="", vererr="", mailerr="",):
        self.write(name = name, mail = mail, nameerr = nameerr, pswerr = pswerr, vererr = vererr, mailerr = mailerr)
    def validUsername(self, username):
        return USER_RE.match(username)
    def validPsw(self, psw):
        return PSW_RE.match(psw)
    def validMail(self, mail):
        if(mail):
            return MAIL_RE.match(mail)
        else:
            return True
    def get(self):
        self.write()

class SignUpPage(SignPage):
    def write(self,**kw):
        super(SignUpPage,self).write(isSignup = True,**kw)
    def post(self):
        username = self.request.get("username")
        email = self.request.get("email")
        psw =  self.request.get("password")   
        psw2 =  self.request.get("verify")
        if(self.validUsername(username)):
            if user.exists(username):
                nameerr = "Username already exists."
            else:
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
            userCookie = user.bake(username, psw)      
            self.response.headers.add_header('Set-Cookie', str('user=%s; Path=/'%userCookie)) 
            self.redirect(head.adr['welcome']);   
        else:
            self.write_form(username,email,nameerr,pswerr,vererr,mailerr)

class SignInPage(SignPage):
    def write(self,**kw):
        super(SignInPage,self).write(isSignup = False,**kw)
    def post(self):
        username = self.request.get("username")
        password =  self.request.get("password")
        u =  user.getUser(username)
        nameerr =""
        pswerr=""
        if (u):
            if u.check(password):
                userCookie = u.bake()
                self.response.headers.add_header('Set-Cookie', str('user=%s; Path=/'%userCookie)) 
                self.redirect(head.adr['welcome']);   
            else:
                self.write(name = username, nameerr = "Incorrect password.")
        else:
            self.write(name = username, nameerr = "User not found.")


class ClearPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(head.fold('<form method="post"><input type=submit value="Clear"></form>',title))
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user.cleanUsers()    
        self.response.write(head.fold("Clean!",title))


from welcome import WelcomePage
app = webapp2.WSGIApplication([    
    (head.adr['signup'], SignUpPage),
    (head.adr['signin'], SignInPage),
    (head.adr['welcome'], WelcomePage),
    (head.adr['signup']+'/cleaneveryuser', ClearPage),
], debug = head.debug)

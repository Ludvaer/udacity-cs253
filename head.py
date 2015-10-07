import os
import webapp2
import jinja2
from google.appengine.api import app_identity
from jinja2 import Template

debug = True

templateDir = os.path.join(os.path.dirname(__file__), 'templates');
jinja_environment = jinja2.Environment(autoescape=False,
    loader=jinja2.FileSystemLoader(templateDir))

projectName = "Lurr CS-253 Project"

adr = {
          'hello': '/hello',
          'rot13': '/rot13',
          'signup' : '/blog/signup',
          'signin' : '/blog/login',
          'signout' : '/blog/logout',
          'welcome' : '/blog/welcome',
          'blog' : '/blog',
          'blogpost' : '/blog/newpost',
          'timer' : '/timer',
      }

homeLinkString ='<div><a href="http://%s">home</a></div>'%app_identity.get_default_version_hostname()

page = """
<!DOCTYPE html>
<html>
  <head>
      <title>{{title|e}}</title>
      <link rel="stylesheet" type="text/css" href="/css/main.css">
  </head>
  <body>
  <div class="main">
    {{content}} 
    {{homeLink}}
  </div>
  </body>
</html>
"""

# template = jinja_environment.get_template('index.html');
template = Template(page);
def fold(content,title = "", noHomeLink = False):
    return template.render({"content":content, "title":title +" | "+ projectName, "homeLink": "" if noHomeLink else homeLinkString})

class HeadPage(webapp2.RequestHandler):
  page = ""
  title = "Empty"
  template = None
  noHomeLink = False
  def render(self,**params):
    if not self.template:
        self.template = Template(self.page);
    c = self.template.render(params)
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write(fold(c,self.title,noHomeLink = self.noHomeLink))

    

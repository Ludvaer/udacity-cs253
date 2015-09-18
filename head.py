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
            'signUp' : '/signup',
            'welcome' : '/signup/welcome',
            'blog' : '/blog',
            'blogpost' : '/blog/newpost',
        }

homeLinkString ='<br><a href="http://%s">home</a>'%app_identity.get_default_version_hostname()

page = """
<!DOCTYPE html>
<html>
  <head>
      <title>{{title|e}}</title>
      <style type="text/css">
    body {
        font-family: Helvetica, Arial, sans-serif;
        width: 800px;
        margin: 0 auto;
        padding: 10px;
    }
    .error {
        color: red;
    }
    label {
        display: block; font-size: 20px;
    }
    label + label {
        margin-top: 20px;
    }
    input[type=text] {
        width: 500px; font-size: 20px; padding: 2px; font-family: monospace;
    }
    textarea {
        width: 500px; height: 200px; font-size: 17px; font-family: monospace;
    }
    input[type=submit] {
        font-size: 24px;
    }
    
    .main-title {
color: #111;
display: block;
font-size: 40px;
font-weight: bold;
text-align: center;
margin-bottom: 30px;
border-bottom: 2px solid #eee;
text-decoration: none;
    }


    .post {
        margin-bottom: 20px;
        width:100%;        
    }
    .post-header {
        position:relative;
        border-bottom: 1px dotted #ccc;
    }
    .post-subject {
        font-weight: bold;
        font-size: 20px; 
        text-decoration: none;
    }
    .post-date {
        position: absolute;
        right: 0px;
        bottom: 0px;
        font-size: 15px;
        color: #aaa;
    }
    .post-content {
        word-wrap: break-word;
        margin: 0; 
        font-size: 17px; 
    }
      </style>
  <head>
  <body>
    {{content}}
  </body>
  {{homeLink}}
</html>
"""

# template = jinja_environment.get_template('index.html');
template = Template(page);
def fold(content,title = "", noHomeLink = False):
    return template.render({"content":content, "title":title +" "+ projectName, "homeLink": "" if noHomeLink else homeLinkString})
    

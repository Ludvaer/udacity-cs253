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
            'signup' : '/signup',
            'welcome' : '/signup/welcome',
            'blog' : '/blog',
            'blogpost' : '/blog/newpost',
        }

homeLinkString ='<div><a href="http://%s">home</a></div>'%app_identity.get_default_version_hostname()

page = """
<!DOCTYPE html>
<html>
  <head>
      <title>{{title|e}}</title>
      <style type="text/css">
    body {
        background: #ddd;
        font-family: Helvetica, Arial, sans-serif;
        max-width: 50em;
        padding: 2%;
        margin: auto;
        font-size: 20px;
    }
    h1 {
        color: #111;
        display: block;
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 2px solid #ccc;
    }

    label {
        display: block; font-size: 20px;
    }
    label + label {
        margin-top: 20px;
    }
    form { 
        margin:auto;
        max-width:30em;
        padding: 2%;
        box-sizing: border-box;
    }
    input {
        font-size: 17px;
        padding: 0.3em;
        font-family: monospace;
        width:100%;
        box-sizing: border-box;
    }
    textarea {
        font-size: 17px;
        padding: 0.3em;
        height: 30em;
        font-family: monospace;
        width:100%;
        box-sizing: border-box;
    }
    input[type=submit] {
        width:auto;
        font-size: 24px;
        font-family: Helvetica, Arial, sans-serif;
        padding: 0.3em;
    }
    li {
        margin: 1em
    }

    .error {
        color: red;
    }
    
    .main-title {
        color: #111;
        display: block;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin: auto;
        margin-bottom: 1em;
        border-bottom: 2px solid #ccc;
        text-decoration: none;
    }


    .post {        
        margin: 1em;
        background: #eee;
        width: auto; 
        border: 1px solid #ccc       
    }
    .post-header {
        position:relative;
        border-bottom: 1px dotted #ccc;
        background: #f7f7f7;
        padding: 1em;
        padding-bottom: 0.5em;
    }
    .post-subject {
        color: #222;
        font-weight: bold;
        font-size: 20px; 
        text-decoration: none;
    }
    .post-date {
        position: absolute;
        right: 1em;
        bottom: 0.75em;
        font-size: 15px;
        color: #aaa;
    }
    .post-content {        
        white-space: pre-wrap;
        word-wrap: break-word;
        font-size: 17px; 
        padding: 1em;
        padding-top: 0.5em;
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
    

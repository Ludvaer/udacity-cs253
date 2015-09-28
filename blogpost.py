import os
import webapp2
import jinja2
from google.appengine.ext import db
from jinja2 import Template
from head import adr
from head import templateDir
from blog import bfold
from blog import Post

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templateDir), autoescape=False)

title = "New Post"

page = """
<form method="post">
    <div>
        <label>subject</label>
        <input type="text" name="subject" {% if subject %}value ="{{subject|e}}"{% endif %}>
        <div class="error"> {{errors}} </div>
    </div>
    
    <div>
        <label>content</label>
        <textarea name="content">{{content|e}}</textarea> 
        <div class="error"> {{errorc}} </div>
    </div>
    <input type="submit" value = "submit">
</form>
"""

template = Template(page);

class PostPage(webapp2.RequestHandler):
    def render(self, **kw):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(bfold(template.render(kw),title))
    def get(self):
        self.render();
    def post(self):
        subject = self.request.get("subject") 
        content = self.request.get("content")
        if subject and content:
            p = Post(subject = subject, content = content)
            p.put()
            self.redirect(adr['blog']+"/"+str(p.key().id()))
            return
        args = {"subject":subject,"content":content}
        if not subject:
            args["errors"] = "No subject detected - submission rejected."             
        if not content:
            args["errorc"] = "No content - no entry!"
        self.render(**args)



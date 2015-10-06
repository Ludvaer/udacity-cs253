import os
import webapp2
import jinja2
import post
import head
from google.appengine.ext import db
from jinja2 import Template
from blog import bfold

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(head.templateDir), autoescape=False)

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
            key = post.add(subject,content)
            self.redirect(head.adr['blog']+"/"+str(key))
            return
        args = {"subject":subject,"content":content}
        if not subject:
            args["errors"] = "No subject detected - submission rejected."             
        if not content:
            args["errorc"] = "No content - no entry!"
        self.render(**args)


app = webapp2.WSGIApplication([
    (head.adr['blogpost'], PostPage)
], debug=head.debug)
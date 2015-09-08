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
    <label>
        <div>subject</div><input type="text" name="subject" value ="{{subject|e}}">
    </label>
    <label>
        <div>content</div><textarea name="content">{{content|e}}</textarea>
    </label>
    <div class="error"> {{error}} </div>
    <input type="submit">
</form>

"""



template = Template(page);

class PostPage(webapp2.RequestHandler):
    #def write(self, *a, **kw):
    #    self.response.out.write(*a, **kw)
    #def render_str(self, template, **params):
    #    t = jinja_env.get_template(template)
    #    return t.render(params)
    #def render(self, template, **kw):
    #    self.write(self.render_str(template, **kw))
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
        elif subject:
            error = "No content - no entry!"
        elif content:
            error = "No subject detected - submission rejected." 
        else:
            error = "I would like a subject and some content." 
        self.render(error = error,subject = subject,content =content )



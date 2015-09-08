import os
import webapp2
import jinja2
from google.appengine.ext import db
from jinja2 import Template
from head import fold
from head import adr
from head import templateDir

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templateDir), autoescape=False)

btitle = "Blog"

bhomeLinkString = '<br> <a href="%s">Blog home page</a> <br>'%adr['blog']

bpage = """
<h1>Lurr CS 253 Blog</h1><br>
{{content}}
{{bhomeLink}}
"""

btemplate = Template(bpage)

def bfold(content, title = "", noHomeLink = False):
    return fold(btemplate.render({"content":content, "bhomeLink": "" if noHomeLink else bhomeLinkString}), title + " " + btitle)


page = """
<a href=" {{blogpost}} ">[add post]</a> <br>
<br>
    {{test}}
    <div>
    {% for post in posts %}
    <div class="post">
        <div class="post-subject"><a href = "{{blog}}/{{post.key().id()}}">{{post.subject|e}}</a></div>
        <pre class="post-content">{{post.content|e}}</pre>
    </div>
    </div>
    {% endfor %}
"""
template = Template(page);

class Post(db.Model):
     
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class BlogPage(webapp2.RequestHandler):
    #def write(self, *a, **kw):
    #    self.response.out.write(*a, **kw)
    #def render_str(self, template, **params):
    #    return template.render(params)
    #def render(self, template, **kw):
    #    self.write(self.render_str(template, **kw))

    def write(self,**params):
        self.response.headers['Content-Type'] = 'text/html'
        c = template.render(params)
        self.response.write(bfold(c,noHomeLink = True))
    def render(self, **params):
        self.write(blogpost = adr['blogpost'],blog = adr['blog'],**params)
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 13")     
        self.render(posts = posts);

class BlogPostPage(BlogPage):
    def write(self,**params):
        self.response.headers['Content-Type'] = 'text/html'
        c = template.render(params)
        self.response.write(bfold(c,noHomeLink = False))
    def get(self):
        pid = self.request.path.split('/')[-1] 

        posts = db.GqlQuery("SELECT * FROM Post WHERE __key__ = KEY('Post',%s)"%pid)     
        self.render(test = posts,posts = posts );    
        

from blogpost import PostPage
app = webapp2.WSGIApplication([
    (adr['blog'], BlogPage),
    (adr['blogpost'], PostPage),
    (adr['blog']+'/.*', BlogPostPage)
], debug=True)

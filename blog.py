import os
import webapp2
import jinja2
import head
import json
from google.appengine.ext import db
from jinja2 import Template

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(head.templateDir), autoescape=False)

btitle = "Blog"

bhomeLinkString = '<a href="%s">Blog home page</a>'%head.adr['blog']

bpage = """
<a href="%(blog)s" class="main-title">Lurr CS 253 Blog</a>
{{content}}
{{bhomeLink}}
"""%head.adr

btemplate = Template(bpage)

def bfold(content, title = "", noHomeLink = False):
    return head.fold(btemplate.render({"content":content, "bhomeLink": "" if noHomeLink else bhomeLinkString}), title + " " + btitle)


page = """
<a href=" {{blogpost}} ">[add post]</a>
    <div>
    {% for post in posts %}
    <div class="post">
        <div class="post-header" onclick="fclick{{post.key().id()}}()" >
            <a href = "{{blog}}/{{post.key().id()}}" class="post-subject"> {{post.subject|e}} </a>
            <span class="post-date">{{post.created.strftime("%d %b %Y")|e}}</span>
        </div>
        <script>
            function fclick{{post.key().id()}}() {
                window.location.href = "{{blog}}/{{post.key().id()}}";
            }
        </script>
        <div class="post-content">{{post.content|e}}</div>
    </div>
    {% endfor %}
    </div>
"""
template = Template(page);

class Post(db.Model):     
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    def toDict(self):
        return {"content" : self.content.encode('utf-8'), "created" : (self.created.isoformat()), "last_modified" : (self.created.isoformat()), "subject" : self.subject.encode('utf-8')}

class BlogPage(webapp2.RequestHandler):
    def write(self,c):
        self.response.write(bfold(c,noHomeLink = True))        
    def render(self, **params):
        params["blogpost"] = head.adr['blogpost'];
        params["blog"] = head.adr['blog'];
        self.response.headers['Content-Type'] = 'text/html'
        c = template.render(params)
        self.write(c)
    def renderJson(self, **params):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        list = [post.toDict() for post in params["posts"]]
        self.response.write(json.dumps(list))
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 13")     
        self.render(posts = posts);

class BlogSinglePage(BlogPage):
    def write(self,c):
        self.response.write(bfold(c,noHomeLink = False))  
    def get(self):
        adr = self.request.path.split('/')[-1].split('.')
        pid = adr[0]
        posts = db.GqlQuery("SELECT * FROM Post WHERE __key__ = KEY('Post',%s)"%pid)     
        if(adr[-1] == "json"):
            self.renderJson(posts = posts)
        else:
            self.render(posts = posts); 

class BlogPageJson(BlogPage):
    def render(self, **params):
        self.renderJson(**params)

class BlogSinglePageJson(BlogSinglePage):
    def render(self, **params):
        self.renderJson(**params)

   

from blogpost import PostPage
from signUp import SignUpPage
from signUp import SignOutPage
from signUp import SignInPage
from welcome import WelcomePage
app = webapp2.WSGIApplication([
    (head.adr['blog'], BlogPage),
    (head.adr['blog']+".json", BlogPageJson),
    (head.adr['blog']+"/.json", BlogPageJson),
    (head.adr['blog']+"/signup", SignUpPage),
    (head.adr['blog']+"/login", SignInPage),
    (head.adr['blog']+"/logout", SignOutPage),
    (head.adr['blog']+"/welcome", WelcomePage),
    (head.adr['blogpost'], PostPage),
    (head.adr['blogpost']+".json", BlogSinglePageJson),
    (head.adr['blog']+'/.*', BlogSinglePage)
], debug=head.debug)

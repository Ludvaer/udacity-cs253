from google.appengine.ext import db
from datetime import datetime

cachetop = []
last = None
COUNT = 10
time = None

class Post(db.Model):     
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    def toDict(self):
        return {"content" : self.content.encode('utf-8'), "created" : (self.created.isoformat()), "last_modified" : (self.created.isoformat()), "subject" : self.subject.encode('utf-8')}
    def id(self):
      	return self.key().id()


def add(subject,content):
	global cachetop
	global last
	global time
	p = Post(subject = subject, content = content)
	p.put()
	last = p
	posts = top()
	c = []
	c.append(p)
	for post in posts:
		if post.id() != p.id():
			c.append(post)
		if len(c) == COUNT:
			break
	cachetop = c
	time = datetime.now()
	return p.id()

def top():
	global time
	global cachetop
	if len(cachetop) == 0:
		posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT %i"%COUNT)
		time = datetime.now()
		c = []
		for post in posts:
			c.append(post)
		cachetop = c
	return cachetop


def get(pid):
	global time
	global last
	if last and str(last.id()) == pid:
		return [last]
	time = datetime.now()
	posts =  db.GqlQuery("SELECT * FROM Post WHERE __key__ = KEY('Post',%s)"%pid)
	for post in posts:
		last = post
	if last:
		return [last]
	else:
		return []


def delete(pid):
	global time
	global last
	global cachetop
	posts = get(pid)
	for post in posts:
	    post.delete()
	del cachetop[:]
	last = None
	time = datetime.now()


def seconds():
	if not time:
		return 0
	return (datetime.now() - time).seconds

def flush():
	global time
	global last
	global cachetop
	cachetop = []
	last = None
	time = None





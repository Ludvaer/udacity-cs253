from google.appengine.ext import db
import crypto


userCache = None


class User(db.Model):     
    name = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    salt = db.StringProperty(required = True)
    pepper = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    def put(self):
        global userCache
        userCache = self
        super(User,self).put()
    def check(self,password):
        return crypto.check(password, self.salt, self.password)
    def bake(self):
        (userCookie,pepper) = crypto.bake(self.name)
        self.pepper = pepper
        self.put()
        return userCookie


def getFirst(users):
    for user in users:
        return user
    return None

#return oldest user with given uname and kills others
#knida smart way to keep names unique even if to users somehow registered simulltaniusly
def getUser(username):
    user = userCache
    if (user and user.name == username):
        return user
    users = db.GqlQuery("SELECT * FROM User WHERE name='%s' ORDER BY created ASC"%username)
    user = getFirst(users)
    if user:
        uid = user.key().id()
        for u in users:
            if u.key().id() != uid:
                u.delete()
        return user
    return None



def cleanUsers():
    userCache = None
    users = User.all()
    for u in users:
        u.delete()  


def exists(username):
    user = getUser(username)
    if (user):
        return True     

def bake(username, password):
    """Return the cookie foe newly baked user, error if exists."""
    #I want to chek for existance here, but I also wont to check for existance before get here
    #if exists(username):
    #    return  None  
    #in current scenario user added without check will be removed later
    (hmacPsw,salt) = crypto.make(password);            
    (userCookie,pepper) = crypto.bake(username);
    user = User(name = username, password = hmacPsw, salt = salt, pepper = pepper)
    user.put()
    return userCookie;


def getPepper(username):
    """Return pepper from user by username."""
    #attempt to avoid reading from database before wrighting completed 
    #it happens only on localhost as far as I tried by I prefer to be safe
    #so I'm trying to hash last created user and ceck it befor quering db
    user = getUser(username)
    if(user):
        return user.pepper
    return None

def unbake(userCookie):
    """Return the name retrieved from cookie."""
    return crypto.unbake(userCookie,getPepper)



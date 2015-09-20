from google.appengine.ext import db
import crypto


newUser = None


class User(db.Model):     
    name = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    salt = db.StringProperty(required = True)
    pepper = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


def getFirst(users):
    for user in users:
        return user
    return None
#return oldest user with given uname and kills others
#knida smart way to keep names unique even if to users somehow registered simulltaniusly
def getUser(username):
    users = db.GqlQuery("SELECT * FROM User WHERE name='%s' ORDER BY created ASC"%username)
    user = getFirst(users)
    if user:
        uid = user.key().id()
        for u in users:
            if u.key().id() != uid:
                u.delete()
        return user
    user = newUser
    if (user and user.name == username):
        return user
    return None

def exists(username):
    user = getUser(username)
    if (user):
        return True     

def bake(username,psw):
    """Return the cookie foe newly baked user, error if exists."""
    #I want to chek for existance here, but I also wont to check for existance before get here
    #if exists(username):
    #    return  None  
    (hmacPsw,salt) = crypto.make(psw);            
    (userCookie,pepper) = crypto.bake(username);
    u = User(name = username, password = hmacPsw, salt = salt, pepper = pepper)
    global newUser
    newUser = u
    u.put() #put from local variable incase smth happens to global (is it possible?)
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

def cleanUsers():
    users = User.all()
    for u in users:
        u.delete()  


import hmac
import hashlib
import string
import random

symbols = string.lowercase + string.uppercase + string.digits
def randomword(length):
   return ''.join(random.choice(symbols) for i in range(length))


def hmake(s, salt):
    return hmac.new(str(salt),s,hashlib.sha256).hexdigest()
def make(s):
    salt = randomword(10)
    hmacs = hmake(s,salt)
    return (hmacs,salt)
def bake(s):   
    (hmacs,salt) = make(s)
    return ("%s|%s"%(s,hmacs),salt)
def unbake(cookie, getSalt):
    if(cookie):
        (s,separator,hmacs) = cookie.rpartition('|')
    else:
        return None
    if hasattr(getSalt, '__call__'):
        salt = getSalt(s);
    else:
        salt = getSalt
    if (salt and (hmacs == hmake(s,salt))):
        return s
    else:
        return None

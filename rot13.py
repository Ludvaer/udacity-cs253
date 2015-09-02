import webapp2
import cgi
import re
from head import backLinkString


form = """
<form method="post">
<textarea name="text">%s</textarea><br>
<input type=submit value="rotate">
</form>
"""

alpha = "abcdefghijklmnopqrstuvwxyz" 
alphA = alpha.upper()
rep = {alpha[i]:alpha[(i+13)%26] for i in xrange(26)}
rep.update({alphA[i]:alphA[(i+13)%26] for i in xrange(26)})
rep = dict((re.escape(k), v) for k, v in rep.iteritems())
pattern = re.compile("|".join(rep.keys()))

class Rot13Page(webapp2.RequestHandler):
    def escape13(self,s):
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], s) 
    def write_form(self,s):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write((form%s) + (backLinkString))
    def get(self):
        self.write_form("")
    def post(self):
        text = self.request.get("text");        
        text = self.escape13(text)
        text = cgi.escape(text, quote = True);
        self.write_form(text)

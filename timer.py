import webapp2
import head

title = "Timer"

page = """
<h1 id = "countdown">10</h1>
 <audio id="audio" src="/static/beep-07.mp3" autostart="false" ></audio>
<script>
var startTime = 60;
var sound = document.getElementById("audio");
var countdown = document.getElementById("countdown");
setInterval(f, 1000);
var c = startTime;
countdown.innerHTML = c;


function f() {
  c -= 1;  
  if (c <= 0) { 
    var audioContext = new AudioContext();
    var oscillator = audioContext.createOscillator();
    oscillator.frequency.value = 666; 
    oscillator.connect(audioContext.destination); 
    oscillator.start(0);
    oscillator.stop(0.3);  
    c = startTime;
  } 
  countdown.innerHTML = c;
}
function stop() {
  
}

</script>
"""


class TimerPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(head.fold(page,title,noHomeLink = True))

from head import debug
app = webapp2.WSGIApplication([    
    (head.adr['timer'], TimerPage),
], debug=head.debug)
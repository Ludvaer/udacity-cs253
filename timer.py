import webapp2
import head


title = "Timer"

page = """
<h1 id = "countdown"></h1>
<form method="get">
 <input type="button" value="reset" onclick="rset()">
 <label>Set period (sec)</label>
 <input type="number" name="s" id = "startTime" value="">
 <input type="button" value="set" onclick="set()">
 <input type="button" value="set+reset" onclick="forceset()">
 <input type="submit" value="go">
</form>

<script>
var sec = 1000
var soundlong = 0.333
var soundfreq = 666
var startTime = {{start}};
var sound = document.getElementById("audio");
var countdown = document.getElementById("countdown");
var startTimeInput = document.getElementById("startTime");
var interval =  null;
var audioContext = null; 
rset();


function f() {
  c -= 1; 
  if (audioContext != undefined) {
      audioContext.close()
      audioContext = null
  }
  
  if (c <= 0) {
    audioContext = new AudioContext();
    var oscillator = audioContext.createOscillator();
    oscillator.frequency.value = soundfreq; 
    oscillator.connect(audioContext.destination); 
    oscillator.start(0);
    oscillator.stop(soundlong);  
    c = startTime;    
  } 
  countdown.innerHTML = c;
}
function set() {
  startTime = parseInt(startTimeInput.value);
}
function rset() {
  c = startTime;
  countdown.innerHTML = c;
  startTimeInput.setAttribute("value",c);
  if (interval != undefined) {
    clearInterval(interval);
  }
  interval = setInterval(f, sec);
}
function forceset() {
  set();
  rset();
}

</script>
"""


class TimerPage(head.HeadPage):
    page = page
    noHomeLink = True
    title = "Timer"
    def get(self):                
        start = self.request.get("s")
        if not start:
          start = "5";
        self.render(start = start)


from head import debug
app = webapp2.WSGIApplication([    
    (head.adr['timer'], TimerPage),
], debug=head.debug)
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from highscore import get_high_scores_html
from html import write_header, write_footer

class MainPage(webapp.RequestHandler):
  def get(self):
      user = users.get_current_user()

      if user:
        write_header(self)
        self.response.out.write("""
	<h1 style="color: #AA4422; margin:10px 0"><b>Color Quest</b></h1>
	<h2 style="font: bold 18px Arial; margin-top:5px"><i>A simple bargaining game.</i></h2>

        <p><b><u>The Game</u></b>:
        <ul>
          <li>There is a path made of colored squares.</li>
          <li>Crossng a square costs a chip with the same color as the square.</li>
          <li>You wll not start with all the chips you need.</li>
          <li>Each turn you will be <i>offered a choice</i> between two trades.</li>
          <li>Be quick: after the first few rounds, the trail will begin to burn. If the fire catches up to you, GAME OVER!!</li>
          <li><b>Goal</b>: Get the high score!</li>
        </ul></p>

	<p><b><u>Scoring</u></b>:
        <ul>
          <li><b>Only your first game</b> will considered for the Hall of Fame - do your best!</li>
	  <li><i>+5</i> points for each square crossed</li>
          <li><b><u>If you finish the game</u></b>, you also get:
          <ul>
            <li><i>+5</i> points for every non-black chip you have left</li>
            <li><i>+1</i> point for every black chip you have left</li>
            <li><i>+50</i> points for reaching the end of the trail</li>
          </ul>
        </ul>
        </p>

        <center>
	<FORM METHOD="LINK" ACTION="/gameplay_start.html">
	<button onclick="this.disabled=true;" style="height:50px; width:400px; font:bold 24px Arial;">Play now!</button>
	</FORM>""")

        self.response.out.write(get_high_scores_html())

        self.response.out.write("""
	<p style="font: 10px Arial; text-align: center;">By continuing to use this application, you acknowledge that gameplay data will be stored for research purposes.</p>
        </center>
	""")
        write_footer(self)

      else:
        self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

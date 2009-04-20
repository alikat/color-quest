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

        <p><b><u>The Game</u></b>: <blockquote><i>Try to reach the goal and accumulate as
many points as possible along the way!  Each square in the path has a different
color.  In order to cross a square, you must give up a chip of the same color as
the square. You will probably not have all the chips you need to reach the goal,
so to get them you must <u>choose among the proposals offered by the your
computer opponent</u>.  Be quick, however, because after the first few rounds,
the trail will begin to burn.  If the fire catches up to you, GAME OVER!!</i></blockquote>
</p>

	<p><b><u>Scoring</u></b>:
        <ul>
          <li><b>Only your first game</b> will considered for the Hall of Fame - do your best!</li>
	  <li><i>+5</i> points for each square crossed</li>
          <li><b><u>If you finish the game</u></b>, you also get:
          <ul>
            <li><i>+5</i> points for every non-black chip you have left</li>
            <li><i>+1</i> point for every black chip you have left - there will be no blacks in your trail.</li>
            <li><i>+50</i> points for reaching the end of the trail</li>
          </ul>
        </ul>
        </p>

        <center>
	<FORM METHOD="LINK" ACTION="/gameplay_start.html">
	<button style="height:50px; width:400px; font:bold 24px Arial;">Play now!</button>
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

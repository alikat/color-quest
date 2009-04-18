from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
  def get(self):
      user = users.get_current_user()

      if user:
        self.response.out.write("""<html><head><TITLE> Color Quest </TITLE></head><BODY>""")
        self.response.out.write("""
	<h1> <font color="#AA4422"><b>Color Quest Game</b></font></h1>
	<h2> A simple bargaining game in which each player has a number of chips of different colors and a path of coloured squares to the goal.</h2>
	<p> <font color="#445566"> <i> Try to reach the goal and accumulate as many points as possible along the way!  Each square in the path has a different color.  In order to cross a square, you must give up a chip of the same color as the square. You will probably not have all the chips you need to reach the goal, so to get them you must <u>choose among the proposals offered by the your computer opponent</u>.  Be quick, however, because after the first few rounds, the trail will begin to burn.  If the fire catches up to you, GAME OVER!!</i> </p>

	<p> <b> Scoring: </b> <p>
	<p> &nbsp; &nbsp; 5 points for each square crossed </p>
	<p> &nbsp; &nbsp; 50 points for reaching the end of the trail </p>
	<p> &nbsp; &nbsp; 1 point for every chip left over after reaching the end of the trail.  (If you do not finish, you get no points for leftover chips!) </p>
        <p> &nbsp; &nbsp; Black chips at the end of the game are only worth 1/5th of a point each; black will never appear as a color on your trail.  </p> <br><br>

""")

        self.response.out.write("""<center>
	<FORM METHOD="LINK" ACTION="/gameplay_start.html">
	<INPUT TYPE="submit" VALUE="Continue">
	</FORM></center>""")

        self.response.out.write("""
	<p style="text-align: center;"> <font size="-2"> By continuing to use this application, you acknowledge that your gameplay data will be stored for research purposes. </font> </p>
	""")

      else:
        self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

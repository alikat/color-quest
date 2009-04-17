import cgi
import random
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Gamestate(db.Model):
  player = db.UserProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  trail = db.ListProperty(long)
  chips = db.ListProperty(long)
  iteration = db.IntegerProperty()
  round1_choices = db.IntegerProperty()
  round1_rational = db.IntegerProperty()
  round2_choices = db.IntegerProperty()
  round2_rational = db.IntegerProperty()
  chips_to_finish = db.BooleanProperty()
  include = db.BooleanProperty()
  location = db.IntegerProperty()
  game_over = db.BooleanProperty()
  score = db.FloatProperty()


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    
    user = users.get_current_user()
    if user:
      #q = db.GqlQuery("SELECT * FROM Gamestate WHERE user = :1", user)
      #games = q.fetch(1)
      query = Gamestate.all()
      #query.filter('player = ', user)
      query.order('-date')
      games = query.fetch(1)

      game = games[0]
      if (game.game_over):
        self.redirect('/endgame.html')
      else:
        chips = game.chips
      
      # Print out the table displaying the game state data
        self.response.out.write("""
	<table border="7" bordercolordark="#5599CC" bordercolorlight="#CCEEDF">
	      <tr>
	      <td height="37" colspan="4" bgcolor="#ECF2F8"><div align=center><font color="#550000" size=+1><b>Trail</b></font></div></td>
	      </tr>
	      <tr>
	      <td height="38" colspan="4" bordercolor="#FFFFFF"><p>
              <table><tr>
          """)
      # Print out the trail, colour in the trail as appropriate
        for i in (range(31)):
          if (i == game.location + 1):
            self.response.out.write(""" <td width="30" height="30"> <img width="30" height="30" src="/images/Stick_sm_016.png">&nbsp;</td>""")
          else:
            if (i <= game.iteration - 5):
              self.response.out.write(""" <td width="30" height="30"> <img width="30" height="30" src="/images/flammes-38.gif">&nbsp;</td>""")
            else:
              if (game.trail[i-1] == -1):
                self.response.out.write(""" <td width="30" height="30">&nbsp;</td>""")
              if (game.trail[i-1] == 0):
                self.response.out.write(""" <td bgcolor="red" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 1):
                self.response.out.write(""" <td bgcolor="green" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 2):
                self.response.out.write(""" <td bgcolor="orange" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 3):
                self.response.out.write(""" <td bgcolor="blue" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 4):
                self.response.out.write(""" <td bgcolor="yellow" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 5):
                self.response.out.write(""" <td bgcolor="violet" width="30" height="30">&nbsp;</td> """)

            #Output the chip counts of each colour
        self.response.out.write("""  </tr></table>
              </p></td></tr> <tr>
	      <td bordercolor="#334477" bgcolor="#FFDDAA"><div align="center"><b>Your Chips</b></font></div></td>
	      <td colspan="3" bordercolor="#334477"><p>  
                    <table><tr height="50"> <td bgcolor="red"> Red </td> <td>&nbsp; &nbsp; """)
        self.response.out.write('<b>%s</b>' % chips[0])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="green"> Green </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[1])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="orange"> Orange </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[2])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="blue"> Blue </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[3])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="yellow"> Yellow </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[4])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="violet"> Violet </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[5])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor=black><font color="white"> Black</font></td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[6])
        self.response.out.write(""" </td> </tr> </table> </td> </tr>&nbsp; &nbsp;  """)

      #Print out the two choices
        self.response.out.write("""
            <tr>
	    <td bordercolor="#334477" bgcolor="#FFDDAA"><div align="center"><b>Trade Choices</b></div></td>
            <td>
            <table><tr height="50"> <td bgcolor="red"> Red </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="green"> Green </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="orange"> Orange </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="blue"> Blue </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="yellow"> Yellow </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="violet"> Violet </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="black"><font color="white"> Black</font> </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> </table> <br>
                            <FORM METHOD="LINK" ACTION="/gameplay">
                            <INPUT type="submit" name="Choice 1" value="Select"></FORM></td> """)
        self.response.out.write(""" <td> <table> <tr height = "50"> <td bgcolor="red"> Red </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="green"> Green </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="orange"> Orange </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="blue"> Blue </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="yellow"> Yellow </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="violet"> Violet </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="black"><font color="white"> Black</font></td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>0</b>')
        self.response.out.write(""" </td> </tr></table><br>
                            <FORM METHOD="LINK" ACTION="/gameplay">
                            <INPUT type="submit" name="Choice 2" value="Select"></FORM></td></tr>
                            </table>  """)

        game.iteration = game.iteration + 1
        next_color = game.trail[game.location + 1]
        if (chips[next_color] > 0):
          chips[next_color] = chips[next_color] - 1
          game.location = game.location + 1
          
        if (game.location == len(game.trail)):
          game.game_over = true

        if (game.location + 1 == game.iteration - 5):
          game.game_over = True

        game.chips = chips
        game.put()


application = webapp.WSGIApplication(
                                     [('/gameplay', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

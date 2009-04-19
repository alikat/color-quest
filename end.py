import cgi
import random
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import Gamestate

class EndGame(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      q = db.GqlQuery(""" SELECT * FROM Gamestate
                        WHERE player = :1
                        ORDER BY date DESC
                        LIMIT 1 """, user)

      games = q.fetch(1)
      
      # redirect to the main page if we didn't find any games for this user
      if (len(games) == 0):
        self.redirect('/')
        return

      game = games[0]
      finish = False

      if (game.location + 1 >= len(game.trail)):
        finish = True
        

      excess_chips = 0
      for i in range(0,6):
        excess_chips = excess_chips + game.chips[i]


      score = 5*game.location
      if finish:
        score = score + 50
        score = score + excess_chips + game.chips[6]
        self.response.out.write("""
              <center>
               <h1> <font color="#AA4422"><b>You Made it!!</b></font></h1>""")
      else:
        self.response.out.write("""
               <center>
               <h1> <font color="#AA4422"><b>GAME OVER</b></font></h1>""")

      game.score = score
      game.put()

      self.response.out.write("""
               
               <h2> <font color="#445566"> Your Final Score is: %s </font></h2></center>""" % game.score)
      

application = webapp.WSGIApplication(
                                     [('/endgame\.html', EndGame)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

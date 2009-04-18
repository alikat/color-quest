import cgi
import random
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import Gamestate

class Initialize(webapp.RequestHandler):
  def get(self):

    user = users.get_current_user()

    # get the most recent game the user has been playing
    q = db.GqlQuery(""" SELECT * FROM Gamestate
                          WHERE player = :1
                          ORDER BY date DESC
                          LIMIT 1""", user)
    games = q.fetch(1)

    # redirect to the main page if we didn't find any games for this user
    if ((len(games) > 0) and (games[0].game_over == False)):
      self.redirect('/gameplay')
    else:
      game = Gamestate()

      if user:
        game.player = user

        trail = []
        chips_start = []
        trail_length = 30
        num_chips = 20
        for i in range(trail_length):
          trail.append(random.randint(0,5))

        for i in range(num_chips):
          chips_start.append(random.randint(0,5))

        red = 0
        green = 0
        orange = 0
        blue = 0
        yellow = 0
        violet = 0
        black = 0

        for i in chips_start:
          if (i == 0):
            red = red + 1
          if (i == 1):
            green = green + 1
          if (i == 2):
            orange = orange + 1
          if (i == 3):
            blue = blue + 1
          if (i == 4):
            yellow = yellow + 1
          if (i == 5):
            violet = violet + 1
        

        game.trail = trail
        game.chips = [red, green, orange, blue, yellow, violet, black]
        game.iteration = 0
        game.location = -1
        game.score = 0.0
        game.game_over = False
        game.trade1 = [0,0,0,0,0,0,0]
        game.trade2 = [0,0,0,0,0,0,0]

        game.put()

      self.redirect('/gameplay')

application = webapp.WSGIApplication(
                                     [('/gameplay_start\.html', Initialize)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

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
    if not user:
      self.redirect('/')
      return

    # get the most recent game the user has been playing
    q = db.GqlQuery(""" SELECT * FROM Gamestate
                          WHERE player = :1
                          ORDER BY date DESC
                          LIMIT 1""", user)
    games = q.fetch(1)

    # redirect to the main page if we didn't find any games for this user
    if len(games)==0 or games[0].game_over:
      game = Gamestate()
      game.player = user

      trail_length = 30
      trail = [random.randint(0,5) for _ in range(trail_length)]

      num_colors = 7
      chips = num_colors * [0]
      num_chips = 20
      for i in range(num_chips):
        chips[random.randint(0,5)] += 1

      game.trail = trail
      game.chips = chips
      game.iteration = 0
      game.location = -1
      game.score = 0
      game.game_over = False
      game.trade1 = num_colors * [0]
      game.trade2 = num_colors * [0]
      game.round1_choices = 0
      game.round1_rational = 0
      game.round2_choices = 0
      game.round2_rational = 0
      game.chips_to_finish = False
      game.finalized = False

      game.put()

    self.redirect('/gameplay')

application = webapp.WSGIApplication(
                                     [('/gameplay_start\.html', Initialize)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

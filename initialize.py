import cgi
from random import choice
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import Gamestate, put_safe

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
      num_chips = 20

      # generate all the random numbers at once using choice() for efficiency
      choices = [0, 1, 2, 3, 4, 5]
      nums = [choice(choices) for _ in range(trail_length + num_chips)]

      # make the trail from the first set of numbers
      trail = nums[:trail_length]

      # the remaining numbers identify chips
      num_colors = 7
      chips = num_colors * [0]
      for i in nums[trail_length:]:
        chips[i] += 1

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

      put_safe(game)

    self.redirect('/gameplay')

application = webapp.WSGIApplication(
                                     [('/gameplay_start\.html', Initialize)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

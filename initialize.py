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


class Initialize(webapp.RequestHandler):
  def get(self):
    game = Gamestate()

    if users.get_current_user():
      game.player = users.get_current_user()

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

    game.put()

    self.redirect('/gameplay')

application = webapp.WSGIApplication(
                                     [('/gameplay_start\.html', Initialize)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

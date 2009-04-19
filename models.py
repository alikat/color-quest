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
  score = db.IntegerProperty()
  trade1 = db.ListProperty(long)
  trade2 = db.ListProperty(long)

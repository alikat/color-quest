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

  # float from [0.0, 1.0] which represents the probability durng the "round 2"
  # trades that the trade will actually be fulfilled if accepted.
  trade_honesty = db.FloatProperty()

  # boolean which describes whether or not the last trade was honoured
  trade_honoured = db.BooleanProperty()

  # true once the game is finalized by end.py - prevents end.py from being run
  # more than once for a given game
  finalized = db.BooleanProperty()

class HighScore(db.Model):
  name = db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  score = db.IntegerProperty()

def put_safe(obj):
  """Puts obj into the datastore and retries up to three times if a failure occurs."""
  count = 0
  while True:
    try:
      return obj.put()
    except db.Timeout:
      count += 1
      if count == 3:
        raise

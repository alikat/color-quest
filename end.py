import cgi
import random
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import Gamestate

class EndGame(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <h1> <font color="#AA4422"><b>GAME OVER</b></font></h1> """)

application = webapp.WSGIApplication(
                                     [('/endgame\.html', EndGame)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

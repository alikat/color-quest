import cgi
import datetime
import time

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import Gamestate, fetch_safe

class Dump(webapp.RequestHandler):
    def get(self):
        # only let admins access this page
        user = users.get_current_user()
        if not user or not users.is_current_user_admin():
            self.redirect('/')
            return

        q = db.GqlQuery("""SELECT * FROM Gamestate ORDER BY date ASC""")
        games = fetch_safe(q, 1000)

        # the header
        write = self.response.out.write
        write('#\tPlayer\tDate\tIteration\tLocation\tR1C\tR1R\tR2C\tR2R\tGame Over\tScore\tTrail\n')

        fmt = '%u\t%s\t%u\t%u\t%u\t%u\t%u\t%u\t%u\t%s\t%u\t%s\n'
        i = 0
        for game in games:
            ts = int(time.mktime(game.date.timetuple()))

            # fmt_date = '%B %d %Y %H:%M'
            # when = (datetime.datetime.fromtimestamp(int(ts)) + datetime.timedelta(hours=-4)).strftime(fmt_date)

            i += 1
            write(fmt % (i, str(game.player), ts, game.iteration, game.location,
                         game.round1_choices, game.round1_rational, game.round2_choices, game.round2_rational,
                         str(game.game_over), game.score, str(game.trail)))


application = webapp.WSGIApplication(
                                     [('/dump', Dump)],
                                     debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

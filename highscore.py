import datetime

from google.appengine.ext import db

from models import HighScore, put_safe

# number of high scores to track
NUM_HIGH_SCORES = 10

# query to get all the high scores in order
GQL_HIGH_SCORES = """SELECT *
                     FROM HighScore
                     ORDER BY score DESC, date ASC"""


def check_completed_game_for_high_score(game):
    """Checks a completed game to see if it is a high-score.  The appropriate
    update is made if so.

    @param game  the game to check

    @return  HTML about whether it was a high scoring game
    """
    # make sure this is the user' first time playing
    q = db.GqlQuery("""SELECT *
                       FROM Gamestate
                       WHERE player = :1""", game.player)
    num = q.count(2)
    if num != 1:
        return 'Thanks for playing again!  <a href="/">Are you up for another try?</a>'

    # see if this is a high score
    hscores = get_high_scores()
    if hscores[-1].score < game.score:
        add_high_score(game)
        return 'Congratulations, you are a high scorer!  <a href="/">Go view the list!</a>'
    else:
        return 'Thanks for playing!  <a href="/">Try again?</a>'

def add_high_score(game):
    """Adds this game to the list of high scoring games and bumps the lowest
    game from the high score list."""
    # add the new high score
    newhs = HighScore()
    newhs.name = str(game.player)
    newhs.score = game.score
    put_safe(newhs)

    # remove the lowest score
    q = db.GqlQuery(GQL_HIGH_SCORES)
    hscores = q.fetch(1, NUM_HIGH_SCORES)
    if len(hscores) > 0:
        db.delete(hscores)

def get_high_scores():
    """Returns an array of the top NUM_HIGH_SCORES high scores."""
    # make sure this is the user' first time playing
    q = db.GqlQuery(GQL_HIGH_SCORES)
    hscores = q.fetch(NUM_HIGH_SCORES)

    # pad out the list with junk if we don't have the min # of high scores yet
    num_missing = NUM_HIGH_SCORES - len(hscores)
    if num_missing > 0:
        junk_entry = HighScore()
        junk_entry.name = '???'
        junk_entry.date = None
        junk_entry.score = 0
        hscores += (num_missing * [junk_entry])

    return hscores

def get_high_scores_html():
    """Returns an HTML table with the high scores."""
    hscores = get_high_scores()
    table_body = ''.join([get_high_scores_row_html(hs) for hs in hscores])
    return """
<span id="hof"><table>
  <tr><th colspan="2" style="text-align:center;"><h2>Hall of Fame</h2></th></tr>
  <tr><th>Who</th><th>Score</th></tr>
""" + table_body + '</table></span>'

def get_high_scores_row_html(hs):
    """Returns the HTML representation of a high score row."""
    if hs.date is None:
        when = 'n/a'
    else:
        edt = hs.date + datetime.timedelta(hours=-4) # UTC to EDT
        hr = str(int(edt.strftime('%I'))) # remove leading 0
        when = edt.strftime('%B %d at ' + hr + ':%M') + edt.strftime('%p').lower()
    return '<tr><td>%s</td><td>%u<!-- %s --></td></tr>' % (hs.name, hs.score, when)

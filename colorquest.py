import cgi
import random
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from html import write_header, write_footer
from models import Gamestate, put_safe

COLORS = ['red', 'green', 'orange', 'blue', 'yellow', 'violet', 'black']
HTML_COLORS    = ['#FF0000', '#00FF00', '#FFAA00', '#0000FF', '#FFFF00', '#DD00DD', '#000000']
HTML_COLORS_FG = ['#000000', '#000000', '#000000', '#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF']
NUM_COLORS = len(COLORS)
HIDE_UNNEEDED_TRADE_CELLS = True
VALUE_INDEX = NUM_COLORS  # last value in the trade list in the value of the trade
HALFWAY_POINT = 15

DEBUG_SHOW_VALUES = True

class MainPage(webapp.RequestHandler):
  def post(self):
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
      chips = game.chips

      # update the number of choices made
      is_round1 = (game.iteration <= HALFWAY_POINT)
      if is_round1:
        game.round1_choices = game.round1_choices + 1
      else:
        game.round2_choices = game.round2_choices + 1

      # get which trade was taken
      choiceh = self.request.get("choiceh", '')
      if choiceh == '':
        # only works if javascript is off (which is when choiceh fails)
        took_trade1 = (self.request.get("Choice_1", '') != '')
      else:
        took_trade1 = (choiceh == 'Accept Trade 1')

      # get the trade objects
      if took_trade1:
        trade_taken = game.trade1
        trade_not_taken = game.trade2
      else:
        trade_taken = game.trade2
        trade_not_taken = game.trade1

      # determine whether it was rational
      rational = (trade_taken[VALUE_INDEX] >= trade_not_taken[VALUE_INDEX])
      if rational:
        if is_round1:
          game.round1_rational = game.round1_rational + 1
        else:
          game.round2_rational = game.round2_rational + 1

      # apply the trade?
      values_differ = (trade_taken[VALUE_INDEX] != trade_not_taken[VALUE_INDEX])
      game.trade_honoured = (is_round1 or not values_differ or random.random() <= game.trade_honesty)
      if game.trade_honoured:
        for i in range(len(chips)):
          chips[i] = chips[i] + trade_taken[i]

      game.iteration = game.iteration + 1

      #If the player is not in the last spot, update their position
      if (game.location < (len(game.trail) - 1 )):
        next_color = game.trail[game.location + 1]
        if (chips[next_color] > 0):
          chips[next_color] = chips[next_color] - 1
          game.location = game.location + 1

      game.chips = chips

      #Generate a list of chip-requirements for the trail
      trail_reqs = [0, 0, 0, 0, 0, 0]
      for i in range(game.location+1, len(game.trail)):
        trail_reqs[game.trail[i]] = trail_reqs[game.trail[i]] + 1

      #Subtract current chips from trail requirements
        #Assume player has all the chips they need - if a positive number appears in need, set flag to false
      needs = [trail_reqs - chips for trail_reqs, chips in zip(trail_reqs, chips)]
      game.chips_to_finish = True
      for x in needs:
        if (x > 0):
          game.chips_to_finish = False


      redir_to = '/gameplay'
      if (game.location == len(game.trail)-1):
        game.game_over = True
        redir_to = '/endgame.html'

      if (game.location + 1 == game.iteration - 7):
        game.game_over = True
        redir_to = '/endgame.html'

      # this put() occasionally times out, so retry it a few times on failure
      put_safe(game)
      self.redirect(redir_to)


  def get(self):
    write_header(self, 0, 0)

    user = users.get_current_user()
    if user:
      # get the most recent game the user has been playing
      q = db.GqlQuery(""" SELECT * FROM Gamestate
                          WHERE player = :1
                          ORDER BY date DESC
                          LIMIT 1""", user)
      games = q.fetch(1)

      # redirect to the main page if we didn't find any games for this user
      if (len(games) == 0):
        self.redirect('/')
        return

      game = games[0]

      # choose a unique, deterministc random seed for each iteration so the
      # randomness isn't affected by simply reloading the page!
      random.seed(hash(str(game.key())) + game.iteration)

      if (game.game_over):
        self.redirect('/endgame.html')
      else:
        chips = game.chips

        trade1 = [0,0,0,0,0,0,0,0]
        trade2 = [0,0,0,0,0,0,0,0]

        #Generate Trades if they don't have the chips they need to finish
        if (not game.chips_to_finish):
          trail_temp = []

        #Only send remaining trail
          for i in range(game.location+1, len(game.trail)):
            c = game.trail[i]
            trail_temp.append(COLORS[c])

          order_var = random.random()

        #Testing base rationality - See if they can identify fair vs. unfair, good vs. bad trades
          if (game.iteration <= 15):
            if (order_var < 0.5):
            #Good trade on Left
              trade1 = createProposal(chips, trail_temp, False, 1) #Good
              trade2 = createProposal(chips, trail_temp, False, -1) #Unfair/Bad
            else:
            #Good trade on Right
              trade1 = createProposal(chips, trail_temp, False, -1)#Unfair
              trade2 = createProposal(chips, trail_temp, False, 1) #Fair

          else:
            if (order_var < 0.5):
            #Good trade on Left
              trade1 = createProposal(chips, trail_temp, False, 1) #Good trade!
              trade2 = createProposal(chips, trail_temp, True, -1) #zero phenomena
            else:
            #Good trade on Right
              trade1 = createProposal(chips, trail_temp, True, -1) #zero phenomena
              trade2 = createProposal(chips, trail_temp, False, 1) #Good trade!


        #Save trade in data structure
        game.trade1 = trade1
        game.trade2 = trade2

        put_safe(game)

        # Print out the table displaying the game state data
        write = self.response.out.write
        write('<div id="game">')
        write('<div id="pathname"><h2>The Path</h2></div>')

        # Print out the trail, colour in the trail as appropriate
        write('<div id="trail"><table><tr>')
        for i in (range(31)):
          if i == game.location + 1:
            idf = 'id="player"'
          elif i <= game.iteration - 7:
            idf = 'id="fire"'
          else:
            idf = ''

          color_num = game.trail[i-1]
          color = '#FFFFFF' if color_num == -1 else HTML_COLORS[color_num]
          self.response.out.write("""<td %s bgcolor="%s">&nbsp;</td>""" % (idf, color))
        write('</tr></table></div>')

        #Output the chip counts of each colour
        write('<div id="chips"><table width="100%"><tr>')
        write('<td style="background-color:#FFDDAA; font: bold 24px Arial; width:200px">Your Chips</td>');
        for i in range(NUM_COLORS):
          write('<td style="background-color:%s; color:%s;">%u</td>' % (HTML_COLORS[i], HTML_COLORS_FG[i], chips[i]))
        write('</tr></table></div>')

        # Let the user know if the last trade failed (fraud!)
        if not game.trade_honoured:
          write('<div id="scam">You were scammed!  The trade you tried to accept was fraudulent -- better luck next time.</div>')

        #Print out the two choices
        write('<div id="chips">')
        write('<div style="padding-bottom:10px;"><h2>Choose between these two trades:</h2></div>')
        write('<table width="100%">')
        trade_row_start = '''<tr>
<td style="width:200px">
  <FORM METHOD="POST" ACTION="/gameplay" style=" padding:0; margin:0">
    <input type="hidden" id="choiceh" name="choiceh" value="nil"/>
    <INPUT type="submit" id="Choice_%u" name="Choice_%u" value="Accept Trade %u" style="height:%upx"
           onclick="document.getElementById('choiceh').value = this.value;
                    document.getElementById('Choice_1').disabled=true;
                    document.getElementById('Choice_2').disabled=true;">%s
  </FORM>
</td>'''
        warning = '''
<div id="warning">
  WARNING: There is a <u>%.0f%%</u> chance this
  offer is a <u>fraud</u> and won\'t have any impact!
</div>'''
        for t in range(1, 3):
          if t == 2:
            write('<tr style="height:20px"><td colspan="%u" style="background-color:#444444;"></td></tr>' % (NUM_COLORS+1))
          trade = trade1 if t == 1 else trade2

          # show a warning about a dishonest trader in the second half for the rational choice
          rh = 100
          extra = ''
          if game.iteration > HALFWAY_POINT and game.trade_honesty < 1.0:
            other_trade = trade1 if t != 1 else trade2
            if trade[VALUE_INDEX] > other_trade[VALUE_INDEX]:
              rh = 50
              extra =  warning % (100.0 - 100.0*game.trade_honesty)

          write(trade_row_start % (t, t, t, rh, extra))
          for i in range(NUM_COLORS):
            if HIDE_UNNEEDED_TRADE_CELLS and trade[i]==0:
              write('<td style="background-color:#CCCCCC"></td>')
            else:
              write('<td style="background-color:%s; color:%s;">%u</td>' % (HTML_COLORS[i], HTML_COLORS_FG[i], trade[i]))
          write('</tr>')
        write('</table></div>')

        if DEBUG_SHOW_VALUES:
          write('Trade 1 = %u<br/>Trade 2 = %u' % (trade1[VALUE_INDEX], trade2[VALUE_INDEX]))

        # all done
        write_footer(self)

        #Save all changes in the datastore
        put_safe(game)

application = webapp.WSGIApplication(
                                     [('/gameplay', MainPage)],
                                     debug=True)



def getPlayerChipNeeds(chips,trail):
  color_order = ['red','green','orange','blue','yellow','violet','black'];
  chip_needs = [];
  for color in color_order:
    index = color_order.index(color);
    chip_needs.append(chips[index] - trail.count(color));
  return chip_needs;

def getChipValue(color,chips,trail):
  if color == ('black' or 6):
    return 1.0;
	
  color_order = ['red','green','orange','blue','yellow','violet','black'];
  chip_value = 0.0;
  total_left_in_trail = 0;
  chip_needs = getPlayerChipNeeds(chips,trail);
  for c in color_order:
    index = color_order.index(c);
    if chip_needs[index] < 0:
      total_left_in_trail = total_left_in_trail + abs(chip_needs[index]);
  total_in_trail = trail.count(color);	
  index = color_order.index(color);
  diff = total_in_trail - chips[index];
  if diff > 0:
    chip_value = 50.0/float(total_left_in_trail);
  elif diff <= 0:
    chip_value = 5.0;

  distance = len(trail);	
  for trail_color in trail:
    index = color_order.index(trail_color);
    if trail_color == color and chip_needs[index] < 0:
      chip_value = chip_value + distance;
      return chip_value;
    else:
      distance = distance - 1;

  return chip_value;

def getAllChipValues(chips,trail):
  color_order = ['red','green','orange','blue','yellow','violet','black'];
  chip_values = [];
  for color in color_order:
    chip_values.append(getChipValue(color,chips,trail));
  return chip_values;

def getMaxChipColor(color_order,chip_values):
  max_index = 0;	
  for i in range(len(chip_values)):
    if chip_values[max_index] < chip_values[i]:
      max_index = i;
  return color_order[max_index];

def getMinChipColor(color_order,chip_values):
  min_index = 0;	
  current_index = 0;
  for value in chip_values:
    if chip_values[min_index] > value and color_order[current_index] != ('black' or 6):
      min_index = current_index;
    current_index = current_index + 1;
  return color_order[min_index];


def evaluateProposal(proposal,chip_values):
  current_index = 0;
  proposal_value = 0;
  for value in chip_values:
    proposal_value = proposal_value + proposal[current_index]*value;
    current_index = current_index + 1;
  return proposal_value;
		
def closeToZeroProposal(proposal,opp_chips,opp_path):	
  color_order = ['red','green','orange','blue','yellow','violet','black'];
  color_order_copy = ['red','green','orange','blue','yellow','violet','black'];
  chip_values = getAllChipValues(opp_chips, opp_path);
  chip_values_p = getAllChipValues(opp_chips, opp_path);
  max_chip = getMaxChipColor(color_order_copy,chip_values);
  max_chip_index = color_order.index(max_chip);
  while opp_chips[max_chip_index] <= 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
    del chip_values[color_order_copy.index(max_chip)];
    del color_order_copy[color_order_copy.index(max_chip)];
    if len(color_order_copy) > 0 and len(chip_values) > 0:
      max_chip = getMaxChipColor(color_order_copy,chip_values);
      max_chip_index = color_order.index(max_chip);
  if opp_chips[max_chip_index] > 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
    proposal[max_chip_index] = -1;
    chip_values = getAllChipValues(opp_chips, opp_path);
    color_order_copy = ['red','green','orange','blue','yellow','violet','black'];
    proposal_value = evaluateProposal(proposal,chip_values_p);
    while proposal_value < 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
      max_chip = getMaxChipColor(color_order_copy,chip_values);
      max_chip_index = color_order.index(max_chip);
      if proposal[max_chip_index] < 0:
        del chip_values[color_order_copy.index(max_chip)];
        del color_order_copy[color_order_copy.index(max_chip)];
      else:
        if proposal_value + chip_values_p[max_chip_index] < 0:
          proposal[max_chip_index] = proposal[max_chip_index] + 1;
        else:
          del chip_values[color_order_copy.index(max_chip)];
          del color_order_copy[color_order_copy.index(max_chip)];
      proposal_value = evaluateProposal(proposal,chip_values_p);
		
  return proposal;

def createProposal(opp_chips,opp_path, bonus_enabled, agent_generosity):
  color_order = ['red','green','orange','blue','yellow','violet','black'];
  color_order_copy = ['red','green','orange','blue','yellow','violet','black'];
  chip_needs = getPlayerChipNeeds(opp_chips,opp_path);
  proposal = [];
  for color in color_order:
    proposal.append(0);

  if bonus_enabled:
    #chip_values = getAllChipValues(opp_chips, opp_path);
    #min_chip = getMinChipColor(color_order,chip_values);
    #min_chip_index = color_order.index(min_chip);
    #proposal[min_chip_index] = 1;
    proposal[len(color_order)-1] = random.randint(1,4);
  elif agent_generosity > 0:
    chip_values = getAllChipValues(opp_chips, opp_path);
    min_chip = getMinChipColor(color_order,chip_values);
    min_chip_index = color_order.index(min_chip);
    proposal[min_chip_index] = 1;
    max_chip = getMaxChipColor(color_order_copy,chip_values);
    max_chip_index = color_order.index(max_chip);
    proposal[max_chip_index] = 1;
    del chip_values[color_order_copy.index(max_chip)];
    del color_order_copy[color_order_copy.index(max_chip)];
    if len(color_order_copy) > 0 and len(chip_values) > 0:
      max_chip = getMaxChipColor(color_order_copy,chip_values);
      max_chip_index = color_order.index(max_chip);
    while opp_chips[max_chip_index] <= 0 and len(color_order_copy) > 0 and len(chip_values) > 0 and chip_needs[max_chip_index] <= 0:
      del chip_values[color_order_copy.index(max_chip)];
      del color_order_copy[color_order_copy.index(max_chip)];
      if len(color_order_copy) > 0 and len(chip_values) > 0:
        max_chip = getMaxChipColor(color_order_copy,chip_values);
        max_chip_index = color_order.index(max_chip);
    if opp_chips[max_chip_index] > 0 and len(color_order_copy) > 0 and len(chip_values) > 0 and chip_needs[max_chip_index] <= 0:
      proposal[max_chip_index] = -1;
    else:
      chip_values = getAllChipValues(opp_chips, opp_path);
      color_order_copy = ['red','green','orange','blue','yellow','violet','black'];
      min_chip = getMinChipColor(color_order,chip_values);
      min_chip_index = color_order.index(min_chip);
      while opp_chips[min_chip_index] <= 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
        del chip_values[color_order_copy.index(min_chip)];
        del color_order_copy[color_order_copy.index(min_chip)];
        if len(color_order_copy) > 0 and len(chip_values) > 0:
          min_chip = getMinChipColor(color_order_copy,chip_values);
          min_chip_index = color_order.index(min_chip);
      if opp_chips[min_chip_index] > 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
        proposal[min_chip_index] = -1;
    if random.randint(1,2) == 1 and proposal.count(1) > 1:
      chip_values = getAllChipValues(opp_chips, opp_path);
      min_chip = getMinChipColor(color_order,chip_values);
      min_chip_index = color_order.index(min_chip);
      if proposal[min_chip_index] == 1:
        proposal[min_chip_index] = 0;
  elif agent_generosity < 0:
    chip_values = getAllChipValues(opp_chips, opp_path);
    #print chip_values;
    max_chip = getMaxChipColor(color_order_copy,chip_values);
    max_chip_index = color_order.index(max_chip);
    #print chip_values;
    #print color_order_copy;
    while opp_chips[max_chip_index] <= 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
      del chip_values[color_order_copy.index(max_chip)];
      del color_order_copy[color_order_copy.index(max_chip)];
      if len(color_order_copy) > 0 and len(chip_values) > 0:
        max_chip = getMaxChipColor(color_order_copy,chip_values);
        max_chip_index = color_order.index(max_chip);
    if opp_chips[max_chip_index] > 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
      proposal[max_chip_index] = -1;
      #print proposal;
      del chip_values[color_order_copy.index(max_chip)];
      del color_order_copy[color_order_copy.index(max_chip)];
      if len(color_order_copy) > 0 and len(chip_values) > 0:
        max_chip = getMaxChipColor(color_order_copy,chip_values);
        max_chip_index = color_order.index(max_chip);
      while opp_chips[max_chip_index] <= 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
        del chip_values[color_order_copy.index(max_chip)];
        del color_order_copy[color_order_copy.index(max_chip)];
        if len(color_order_copy) > 0 and len(chip_values) > 0:
          max_chip = getMaxChipColor(color_order_copy,chip_values);
          max_chip_index = color_order.index(max_chip);
      if opp_chips[max_chip_index] > 0 and len(color_order_copy) > 0 and len(chip_values) > 0:
        proposal[max_chip_index] = 1;
  elif agent_generosity == 0:
    proposal = closeToZeroProposal(proposal,opp_chips,opp_path);	
	
  chip_values = getAllChipValues(opp_chips, opp_path);
  proposal_value = evaluateProposal(proposal,chip_values);	
  proposal.append(int(proposal_value));

  return proposal;

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

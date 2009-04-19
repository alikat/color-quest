import cgi
import random
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import Gamestate

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

      name = self.request.get("Choice_1", '')

      # if received trade agreement, update chip counts, location, etc.

    #Actions if they chose Trade 1
      if (name != ''):
        if (game.iteration <= 15):
          game.round1_choices = game.round1_choices + 1
        else:
          game.round2_choices = game.round2_choices + 1
        for i in range(len(chips)):
          chips[i] = chips[i] + game.trade1[i]
        
        if (game.trade1[7] >= game.trade2[7]):
          if (game.iteration <=15):
            game.round1_rational = game.round1_rational + 1
          else:
            game.round2_rational = game.round2_rational + 1

     #Actions if they chose Trade 2
      name = self.request.get("Choice_2", '')
      
      if (name != ''):
        if (game.iteration <= 15):
          game.round1_choices = game.round1_choices + 1
        else:
          game.round2_choices = game.round2_choices + 1

        for i in range(len(chips)):
          chips[i] = chips[i] + game.trade2[i]

        if (game.trade2[7] >= game.trade2[7]):
          if (game.iteration <=15):
            game.round1_rational = game.round1_rational + 1
          else:
            game.round2_rational = game.round2_rational + 1
      
    
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
          
    
      if (game.location == len(game.trail)-1):
        game.game_over = True
        game.put()
        self.redirect('/endgame')

      if (game.location + 1 == game.iteration - 5):
        game.game_over = True
        game.put()
        self.redirect('/endgame')
      
      game.put()
      self.redirect('/gameplay')


  def get(self):
    self.response.out.write('<html><body>')
    
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
            if c==0:
              trail_temp.append('red')
            if c==1:
              trail_temp.append('green')
            if c==2:
              trail_temp.append('orange')
            if c==3:
              trail_temp.append('blue')
            if c==4:
              trail_temp.append('yellow')
            if c==5:
              trail_temp.append('violet')
            if c==6:
              trail_temp.append('black')

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
        
        game.put()
      
      # Print out the table displaying the game state data
        self.response.out.write("""
	<table border="7" bordercolordark="#5599CC" bordercolorlight="#CCEEDF">
	      <tr>
	      <td height="37" colspan="4" bgcolor="#ECF2F8"><div align=center>
              <font color="#550000" size=+1><b>Trail</b></font></div></td>
	      </tr>
	      <tr>
	      <td height="38" colspan="4" bordercolor="#FFFFFF"><p>
              <table><tr>
          """)
      # Print out the trail, colour in the trail as appropriate
        for i in (range(31)):
          if (i == game.location + 1):
            self.response.out.write(""" <td width="30" height="30"> <img width="30" height="30" src="/images/Stick_sm_016.png">&nbsp;</td>""")
          else:
            if (i <= game.iteration - 7):
              self.response.out.write(""" <td width="30" height="30"> <img width="30" height="30" src="/images/flammes-38.gif">&nbsp;</td>""")
            else:
              if (game.trail[i-1] == -1):
                self.response.out.write(""" <td bgcolor="white" width="30" height="30">&nbsp;</td>""")
              if (game.trail[i-1] == 0):
                self.response.out.write(""" <td bgcolor="red" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 1):
                self.response.out.write(""" <td bgcolor="green" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 2):
                self.response.out.write(""" <td bgcolor="orange" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 3):
                self.response.out.write(""" <td bgcolor="blue" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 4):
                self.response.out.write(""" <td bgcolor="yellow" width="30" height="30">&nbsp;</td> """)
              if (game.trail[i-1] == 5):
                self.response.out.write(""" <td bgcolor="violet" width="30" height="30">&nbsp;</td> """)

            #Output the chip counts of each colour
        self.response.out.write("""  </tr></table>
              </p></td></tr> <tr>
	      <td bordercolor="#334477" bgcolor="#FFDDAA"><div align="center"><b>Your Chips</b></font></div></td>
	      <td colspan="3" bordercolor="#334477"><p>  
                    <table><tr height="50"> <td bgcolor="red"> Red </td> <td>&nbsp; &nbsp; """)
        self.response.out.write('<b>%s</b>' % chips[0])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="green"> Green </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[1])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="orange"> Orange </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[2])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="blue"> Blue </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[3])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="yellow"> Yellow </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[4])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="violet"> Violet </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[5])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor=black><font color="white"> Black</font></td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % chips[6])
        self.response.out.write(""" </td> </tr> </table> </td> </tr>&nbsp; &nbsp;  """)

      #Print out the two choices
        self.response.out.write("""
            <tr>
	    <td bordercolor="#334477" bgcolor="#FFDDAA"><div align="center"><b>Trade Choices</b></div></td>
            <td>
            <table><tr height="50"> <td bgcolor="red"> Red </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[0])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="green"> Green </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[1])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="orange"> Orange </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[2])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="blue"> Blue </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[3])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="yellow"> Yellow </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[4])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="violet"> Violet </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[5])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="black"><font color="white"> Black</font> </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade1[6])
        self.response.out.write(""" </td> </tr> </table> <br>
                            <FORM METHOD="POST" ACTION="/gameplay">
                            <INPUT type="submit" name="Choice_1" value="Accept Trade 1" title = %s ></FORM></td> """ % trade1[7])
        self.response.out.write(""" <td> <table> <tr height = "50"> <td bgcolor="red"> Red </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[0])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="green"> Green </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[1])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="orange"> Orange </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[2])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="blue"> Blue </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[3])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="yellow"> Yellow </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[4])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="violet"> Violet </td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[5])
        self.response.out.write(""" </td> </tr> """)
        self.response.out.write(""" <tr height="50"> <td bgcolor="black"><font color="white"> Black</font></td> <td>&nbsp; &nbsp;  """)
        self.response.out.write('<b>%s</b>' % trade2[6])
        self.response.out.write(""" </td> </tr></table><br>
                            <FORM METHOD="POST" ACTION="/gameplay">
                            <INPUT type="submit" name="Choice_2" value="Accept Trade 2" title = %s ></FORM></td></tr>
                            </table>  """ % trade2[7])


        #Save all changes in the datastore
        game.put()

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
      max_chip = getMaxChipColor(color_order_copy,chip_values);
      max_chip_index = color_order.index(max_chip);
    if opp_chips[max_chip_index] > 0 and len(color_order_copy) > 0 and len(chip_values) > 0 and chip_needs[max_chip_index] <= 0:
      proposal[max_chip_index] = -1;
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

def createProposal2(opp_chips,opp_path, bonus_enabled, agent_generosity):
  color_order = ['red','green','orange','blue','yellow','violet','black'];
  proposal = [];
  for color in color_order:
    proposal.append(0);
  index = color_order.index( opp_path[0] );
  proposal[index] = 1;

  return proposal;



def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

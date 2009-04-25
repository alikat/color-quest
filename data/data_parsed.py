import datetime

# this module creates global variables with several subsets of the data:
#     data_all - every result
#     data_first_only - first result from every player
#     data_first_and_fin - first result from every player who also finished

# you can also build some data on the fly with functions:
#     get_rational_data - gets data which are rational some % of the time and
#                         which has a certain # of choices made in round 2
#                         EX: get_rational_data(data_first_and_fin, .8, 5) => 80% rational in round 1, 5 round 2 data points

class Data:
    def __init__(self, id, player, timestamp, iteration, location, r1c, r1r, r2c, r2r, game_over, score, trail):
        self.id = id
        self.player = player
        self.date = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(hours=-4) # EDT time zone
        self.date_str = self.date.strftime('%B %d %Y %H:%M:%S') # date a string
        self.iteration = iteration
        self.location = location
        self.num_choices = [0, r1c, r2c]    # index 1 = round 1, index 2 = round 2
        self.num_rational = [0, r1r, r2r]
        self.game_over = game_over
        self.score = score
        self.trail = trail

    def rationality(self, round_num):
        if self.num_choices[round_num] > 0:
            return self.num_rational[round_num] / float(self.num_choices[round_num])
        else:
            return 0

    def __str__(self):
        # same order as GAE
        #fmt = '%u\t%s\t%s\t%u\t%u\t%u\t%u\t%u\t%u\t%s\t%u'  # condensed version
        fmt = 'id=%u who=%s when=%s iter=%u locn=%u choices=%s rational=%s finished=%s score=%u'
        return fmt % (self.id, self.player, self.date_str, self.iteration, self.location, str(self.num_choices),
                      str(self.num_rational), self.game_over, self.score)

def print_seq(seq):
    """pretty-print an array"""
    print '[\n' + ',\n'.join([str(elt) for elt in seq]) + ']'

# put all of the data into one giant array
data_all = [
    Data(1,"AngerRobot",1240299268,0,-1,0,0,0,0,False,0,[3L, 0L, 1L, 0L, 0L, 5L, 5L, 4L, 1L, 0L, 0L, 2L, 1L, 0L, 1L, 4L, 4L, 3L, 1L, 2L, 2L, 3L, 2L, 5L, 2L, 3L, 5L, 2L, 0L, 1L]),
    Data(2,"thenilly",1240299371,32,29,13,9,13,13,True,203,[2L, 3L, 3L, 2L, 5L, 0L, 2L, 0L, 4L, 5L, 5L, 3L, 1L, 3L, 3L, 0L, 3L, 5L, 2L, 5L, 1L, 3L, 4L, 5L, 5L, 2L, 5L, 2L, 5L, 1L]),
    Data(3,"mikio.hr",1240299372,21,13,13,5,8,5,True,65,[1L, 1L, 4L, 5L, 3L, 1L, 4L, 2L, 1L, 5L, 3L, 5L, 5L, 4L, 5L, 3L, 0L, 0L, 4L, 5L, 4L, 1L, 1L, 3L, 2L, 4L, 3L, 2L, 4L, 1L]),
    Data(4,"bjoyal",1240299400,31,29,13,11,9,6,True,210,[0L, 2L, 1L, 1L, 5L, 3L, 1L, 4L, 5L, 3L, 3L, 1L, 1L, 3L, 3L, 0L, 3L, 0L, 2L, 0L, 0L, 0L, 3L, 3L, 5L, 5L, 1L, 3L, 2L, 1L]),
    Data(5,"masayoshi.k",1240299439,32,29,13,13,6,6,True,201,[3L, 2L, 2L, 3L, 0L, 1L, 4L, 5L, 0L, 1L, 0L, 4L, 4L, 5L, 2L, 0L, 4L, 1L, 4L, 4L, 3L, 5L, 5L, 1L, 3L, 4L, 5L, 1L, 1L, 1L]),
    Data(6,"spasemunki",1240300524,31,29,13,12,17,12,True,221,[5L, 3L, 4L, 0L, 5L, 0L, 1L, 0L, 4L, 0L, 1L, 0L, 1L, 3L, 3L, 2L, 3L, 1L, 2L, 3L, 4L, 0L, 5L, 1L, 3L, 4L, 2L, 2L, 1L, 5L]),
    Data(7,"danielrh",1240301309,30,29,13,13,4,1,True,206,[0L, 1L, 3L, 3L, 1L, 4L, 3L, 4L, 5L, 0L, 0L, 3L, 1L, 1L, 3L, 0L, 3L, 4L, 2L, 3L, 4L, 2L, 1L, 4L, 5L, 4L, 4L, 3L, 0L, 4L]),
    Data(8,"peyman.kazemian",1240301613,29,21,13,8,16,9,True,105,[4L, 1L, 5L, 1L, 3L, 3L, 5L, 2L, 2L, 0L, 3L, 4L, 1L, 0L, 1L, 4L, 0L, 3L, 1L, 2L, 1L, 2L, 0L, 3L, 0L, 1L, 4L, 1L, 3L, 0L]),
    Data(9,"peyman.kazemian",1240301917,34,29,13,9,17,10,True,225,[4L, 3L, 4L, 3L, 3L, 0L, 0L, 1L, 0L, 5L, 5L, 1L, 5L, 2L, 1L, 3L, 4L, 1L, 1L, 0L, 3L, 0L, 4L, 5L, 0L, 2L, 4L, 2L, 2L, 5L]),
    Data(10,"glen.gibb",1240302101,31,29,13,9,9,7,True,207,[2L, 1L, 2L, 4L, 2L, 4L, 1L, 5L, 0L, 1L, 5L, 1L, 2L, 2L, 4L, 5L, 2L, 0L, 3L, 4L, 4L, 3L, 2L, 4L, 0L, 5L, 0L, 0L, 2L, 0L]),
    Data(11,"arj.1985",1240305061,31,29,13,10,6,4,True,204,[1L, 2L, 1L, 3L, 2L, 2L, 3L, 2L, 5L, 1L, 4L, 0L, 5L, 0L, 3L, 0L, 5L, 5L, 4L, 5L, 5L, 1L, 0L, 1L, 0L, 3L, 2L, 3L, 3L, 4L]),
    Data(12,"huangty",1240306499,0,-1,0,0,0,0,False,0,[4L, 4L, 0L, 0L, 3L, 0L, 5L, 5L, 4L, 1L, 1L, 3L, 2L, 3L, 1L, 2L, 4L, 5L, 1L, 4L, 5L, 0L, 1L, 0L, 5L, 2L, 2L, 0L, 3L, 2L]),
    Data(13,"aschulm",1240310942,30,29,13,13,13,12,True,210,[5L, 1L, 2L, 2L, 4L, 5L, 2L, 1L, 0L, 0L, 3L, 4L, 1L, 2L, 5L, 3L, 2L, 1L, 0L, 5L, 0L, 5L, 1L, 1L, 5L, 0L, 5L, 3L, 5L, 2L]),
    Data(14,"7thheavenfan@optonline.net",1240312050,36,29,13,5,16,16,True,198,[4L, 0L, 5L, 2L, 4L, 1L, 1L, 1L, 5L, 0L, 5L, 4L, 2L, 3L, 2L, 4L, 1L, 4L, 1L, 5L, 0L, 3L, 0L, 5L, 5L, 3L, 4L, 5L, 2L, 1L]),
    Data(15,"scubafuchs",1240313102,31,29,13,13,7,3,True,211,[3L, 5L, 1L, 1L, 1L, 1L, 4L, 5L, 3L, 0L, 5L, 2L, 1L, 4L, 4L, 1L, 4L, 3L, 5L, 4L, 2L, 3L, 5L, 1L, 4L, 0L, 5L, 4L, 5L, 1L]),
    Data(16,"WstCoaster07",1240316628,31,29,13,10,7,5,True,203,[2L, 4L, 5L, 1L, 4L, 5L, 2L, 3L, 2L, 2L, 2L, 5L, 2L, 0L, 1L, 5L, 1L, 1L, 0L, 3L, 1L, 5L, 0L, 2L, 5L, 0L, 4L, 1L, 1L, 4L]),
    Data(17,"rstanchak",1240316742,30,29,11,11,0,0,True,198,[2L, 5L, 2L, 2L, 5L, 1L, 2L, 4L, 0L, 1L, 3L, 5L, 5L, 4L, 5L, 4L, 0L, 0L, 1L, 3L, 0L, 3L, 3L, 0L, 1L, 1L, 4L, 4L, 0L, 1L]),
    Data(18,"ponychu",1240317287,0,-1,0,0,0,0,False,0,[5L, 4L, 2L, 4L, 2L, 2L, 1L, 1L, 1L, 2L, 0L, 2L, 1L, 1L, 0L, 3L, 1L, 3L, 3L, 5L, 3L, 5L, 1L, 2L, 5L, 5L, 3L, 1L, 1L, 4L]),
    Data(19,"edeegan2",1240317693,31,29,13,11,16,14,True,208,[1L, 1L, 4L, 0L, 2L, 4L, 0L, 3L, 0L, 0L, 2L, 0L, 0L, 3L, 2L, 2L, 3L, 3L, 3L, 1L, 0L, 2L, 4L, 1L, 5L, 5L, 1L, 4L, 2L, 0L]),
    Data(20,"srhuang",1240318317,30,29,13,13,1,1,True,199,[5L, 1L, 2L, 5L, 4L, 2L, 5L, 0L, 4L, 5L, 3L, 5L, 1L, 4L, 5L, 4L, 1L, 0L, 4L, 3L, 2L, 3L, 2L, 4L, 1L, 1L, 5L, 0L, 5L, 4L]),
    Data(21,"james.dna.white",1240318380,0,-1,0,0,0,0,False,0,[2L, 0L, 5L, 4L, 4L, 2L, 1L, 5L, 2L, 1L, 5L, 3L, 3L, 4L, 5L, 5L, 5L, 2L, 3L, 0L, 1L, 1L, 0L, 2L, 2L, 5L, 3L, 0L, 4L, 3L]),
    Data(22,"holsclaw",1240318380,30,29,13,12,9,8,True,208,[3L, 3L, 1L, 2L, 2L, 4L, 0L, 2L, 0L, 5L, 3L, 5L, 4L, 2L, 0L, 3L, 2L, 2L, 1L, 1L, 4L, 2L, 2L, 2L, 2L, 5L, 1L, 3L, 1L, 0L]),
    Data(23,"frangiadakis",1240318607,22,14,13,4,9,4,True,70,[2L, 0L, 1L, 4L, 5L, 4L, 5L, 2L, 0L, 0L, 4L, 2L, 1L, 5L, 0L, 2L, 3L, 2L, 3L, 5L, 1L, 2L, 4L, 1L, 4L, 3L, 4L, 5L, 2L, 0L]),
    Data(24,"holsclaw",1240318661,31,29,13,12,8,7,True,204,[1L, 4L, 1L, 3L, 0L, 5L, 4L, 2L, 5L, 1L, 5L, 1L, 3L, 0L, 2L, 1L, 5L, 0L, 0L, 0L, 4L, 0L, 0L, 3L, 5L, 0L, 0L, 0L, 0L, 2L]),
    Data(25,"frangiadakis",1240318792,30,29,13,13,7,5,True,210,[5L, 4L, 3L, 4L, 0L, 5L, 1L, 4L, 3L, 3L, 5L, 0L, 5L, 0L, 0L, 2L, 4L, 5L, 1L, 1L, 2L, 3L, 4L, 4L, 4L, 0L, 5L, 3L, 1L, 3L]),
    Data(26,"holsclaw",1240318843,31,29,13,12,17,6,True,230,[4L, 2L, 0L, 5L, 0L, 2L, 1L, 4L, 1L, 5L, 0L, 4L, 0L, 2L, 2L, 0L, 2L, 0L, 0L, 1L, 3L, 4L, 5L, 0L, 4L, 1L, 0L, 0L, 2L, 5L]),
    Data(27,"erichardisty",1240319432,31,29,13,11,14,10,True,216,[0L, 3L, 1L, 1L, 0L, 0L, 0L, 5L, 5L, 0L, 4L, 0L, 3L, 2L, 0L, 5L, 5L, 4L, 4L, 3L, 1L, 0L, 2L, 0L, 1L, 0L, 0L, 2L, 5L, 3L]),
    Data(28,"anvinson80",1240320125,32,29,13,13,13,10,True,218,[1L, 4L, 2L, 2L, 1L, 1L, 0L, 4L, 0L, 2L, 2L, 3L, 2L, 2L, 0L, 5L, 2L, 3L, 3L, 5L, 3L, 1L, 0L, 3L, 3L, 0L, 3L, 1L, 1L, 2L]),
    Data(29,"holsclaw",1240321084,31,29,13,13,0,0,True,201,[1L, 2L, 5L, 0L, 0L, 3L, 3L, 1L, 1L, 0L, 3L, 2L, 1L, 1L, 5L, 1L, 4L, 2L, 3L, 4L, 2L, 0L, 5L, 2L, 3L, 4L, 4L, 5L, 0L, 5L]),
    Data(30,"holsclaw",1240321210,30,22,13,6,17,13,True,110,[3L, 1L, 2L, 2L, 4L, 2L, 3L, 0L, 0L, 2L, 1L, 5L, 3L, 3L, 1L, 4L, 2L, 2L, 2L, 3L, 1L, 5L, 3L, 1L, 5L, 2L, 0L, 1L, 0L, 0L]),
    Data(31,"dmonner",1240323289,30,29,13,12,14,14,True,207,[1L, 0L, 3L, 3L, 5L, 1L, 0L, 0L, 4L, 1L, 2L, 4L, 0L, 0L, 3L, 5L, 0L, 2L, 1L, 5L, 3L, 2L, 3L, 3L, 5L, 1L, 0L, 4L, 4L, 5L]),
    Data(32,"rob.patro",1240323660,34,29,13,9,15,15,True,205,[3L, 0L, 4L, 3L, 5L, 5L, 0L, 0L, 3L, 0L, 5L, 0L, 3L, 1L, 1L, 3L, 4L, 3L, 3L, 2L, 4L, 0L, 3L, 5L, 2L, 0L, 1L, 0L, 2L, 0L]),
    Data(33,"jneilm",1240323990,32,29,13,13,13,8,True,214,[1L, 3L, 3L, 2L, 0L, 3L, 0L, 1L, 3L, 3L, 4L, 2L, 1L, 0L, 1L, 3L, 5L, 3L, 0L, 4L, 5L, 1L, 4L, 3L, 1L, 4L, 3L, 4L, 5L, 1L]),
    Data(34,"emery.mikel",1240324111,25,17,13,10,12,9,True,85,[4L, 1L, 0L, 3L, 2L, 3L, 5L, 3L, 5L, 3L, 1L, 4L, 0L, 4L, 2L, 3L, 0L, 3L, 1L, 3L, 5L, 0L, 3L, 0L, 2L, 5L, 5L, 1L, 4L, 0L]),
    Data(35,"itsdhiraj",1240324551,35,29,13,7,16,16,True,206,[3L, 3L, 1L, 1L, 0L, 1L, 2L, 4L, 1L, 4L, 1L, 2L, 4L, 0L, 1L, 4L, 3L, 0L, 2L, 4L, 3L, 4L, 3L, 3L, 3L, 1L, 2L, 3L, 4L, 3L]),
    Data(36,"rick@blocmedia.com",1240325314,31,29,13,10,12,8,True,210,[5L, 1L, 0L, 2L, 3L, 3L, 1L, 5L, 4L, 0L, 3L, 3L, 2L, 0L, 0L, 1L, 5L, 4L, 2L, 2L, 2L, 0L, 5L, 5L, 0L, 0L, 5L, 2L, 5L, 0L]),
    Data(37,"Micah.Akin",1240325369,27,19,13,9,14,10,True,95,[2L, 2L, 4L, 1L, 4L, 1L, 5L, 5L, 1L, 3L, 1L, 0L, 3L, 5L, 5L, 2L, 3L, 3L, 3L, 1L, 4L, 3L, 5L, 0L, 0L, 1L, 4L, 5L, 2L, 1L]),
    Data(38,"anthony.don",1240325985,0,-1,0,0,0,0,False,0,[4L, 4L, 5L, 2L, 2L, 1L, 1L, 0L, 1L, 0L, 5L, 0L, 3L, 5L, 3L, 2L, 2L, 4L, 5L, 3L, 2L, 1L, 5L, 2L, 2L, 1L, 4L, 1L, 1L, 4L]),
    Data(39,"holsclaw",1240326266,30,29,13,11,8,4,True,211,[5L, 3L, 2L, 2L, 5L, 5L, 5L, 4L, 5L, 4L, 2L, 4L, 5L, 3L, 1L, 1L, 1L, 2L, 0L, 0L, 4L, 3L, 2L, 5L, 4L, 3L, 1L, 5L, 1L, 1L]),
    Data(40,"michael.schatz",1240326788,35,29,13,8,22,12,True,231,[4L, 0L, 4L, 4L, 2L, 5L, 0L, 2L, 5L, 2L, 1L, 1L, 5L, 4L, 2L, 2L, 5L, 2L, 1L, 2L, 4L, 4L, 3L, 0L, 2L, 0L, 1L, 1L, 2L, 0L]),
    Data(41,"michael.schatz",1240327092,0,-1,0,0,0,0,False,0,[3L, 5L, 5L, 1L, 5L, 2L, 2L, 0L, 0L, 0L, 0L, 1L, 1L, 4L, 0L, 3L, 2L, 2L, 2L, 0L, 3L, 4L, 3L, 2L, 2L, 0L, 5L, 2L, 3L, 4L]),
    Data(42,"jneilm",1240327204,30,29,13,13,9,8,True,211,[0L, 5L, 0L, 5L, 0L, 5L, 2L, 0L, 5L, 1L, 2L, 5L, 5L, 2L, 0L, 2L, 2L, 0L, 0L, 0L, 5L, 0L, 0L, 5L, 4L, 5L, 2L, 4L, 5L, 0L]),
    Data(43,"jneilm",1240327310,31,29,13,12,12,12,True,212,[5L, 0L, 1L, 5L, 2L, 3L, 1L, 4L, 0L, 2L, 5L, 5L, 5L, 3L, 2L, 4L, 4L, 5L, 5L, 5L, 5L, 5L, 5L, 2L, 4L, 5L, 4L, 0L, 4L, 2L]),
    Data(44,"tomek.glinkowski",1240327472,30,29,13,12,5,4,True,206,[3L, 3L, 5L, 2L, 5L, 3L, 1L, 5L, 2L, 0L, 2L, 0L, 3L, 3L, 3L, 0L, 4L, 4L, 3L, 4L, 2L, 0L, 5L, 4L, 5L, 5L, 1L, 1L, 4L, 3L]),
    Data(45,"gracejanae@aol.com",1240327476,31,29,13,9,14,8,True,208,[5L, 3L, 2L, 0L, 1L, 2L, 1L, 3L, 0L, 0L, 4L, 3L, 2L, 3L, 1L, 2L, 4L, 4L, 5L, 5L, 3L, 3L, 0L, 2L, 5L, 1L, 4L, 0L, 3L, 0L]),
    Data(46,"aphillippy",1240328230,31,29,13,12,16,11,True,217,[5L, 3L, 4L, 1L, 1L, 5L, 5L, 2L, 4L, 4L, 3L, 5L, 5L, 3L, 4L, 2L, 0L, 5L, 4L, 5L, 5L, 0L, 5L, 5L, 2L, 2L, 1L, 0L, 5L, 5L]),
    Data(47,"nikhil.handigol",1240328459,30,29,13,11,12,11,True,206,[5L, 4L, 0L, 5L, 0L, 4L, 3L, 4L, 5L, 1L, 3L, 5L, 3L, 4L, 0L, 3L, 4L, 2L, 3L, 2L, 2L, 1L, 1L, 4L, 0L, 2L, 2L, 5L, 5L, 5L]),
    Data(48,"srini084",1240328475,30,29,13,11,10,8,True,212,[0L, 4L, 4L, 5L, 1L, 5L, 1L, 3L, 0L, 1L, 1L, 1L, 0L, 2L, 4L, 3L, 1L, 1L, 0L, 5L, 3L, 1L, 2L, 0L, 3L, 0L, 4L, 0L, 2L, 4L]),
    Data(49,"thenilly",1240328662,31,23,13,7,18,17,True,115,[1L, 2L, 1L, 2L, 0L, 5L, 4L, 3L, 2L, 5L, 3L, 5L, 0L, 3L, 2L, 3L, 3L, 1L, 3L, 3L, 1L, 4L, 0L, 0L, 4L, 1L, 5L, 5L, 4L, 3L]),
    Data(50,"srini084",1240328669,34,29,13,9,21,17,True,217,[2L, 1L, 2L, 2L, 1L, 4L, 5L, 2L, 5L, 0L, 3L, 1L, 4L, 3L, 2L, 4L, 3L, 5L, 4L, 5L, 5L, 1L, 5L, 2L, 5L, 3L, 5L, 3L, 0L, 2L]),
    Data(51,"sdhollis",1240328724,36,29,13,11,20,15,True,218,[4L, 3L, 3L, 2L, 0L, 0L, 0L, 0L, 4L, 2L, 3L, 4L, 0L, 3L, 4L, 2L, 0L, 4L, 4L, 2L, 0L, 4L, 2L, 0L, 0L, 4L, 2L, 2L, 5L, 5L]),
    Data(52,"thuanhuynh",1240329015,2,1,2,2,0,0,False,0,[2L, 1L, 2L, 1L, 1L, 2L, 0L, 5L, 3L, 1L, 5L, 5L, 4L, 1L, 3L, 0L, 0L, 4L, 0L, 5L, 0L, 5L, 0L, 4L, 0L, 1L, 3L, 1L, 5L, 4L]),
    Data(53,"m073912",1240329041,30,29,12,12,0,0,True,200,[4L, 4L, 5L, 2L, 0L, 3L, 2L, 3L, 3L, 2L, 4L, 0L, 4L, 2L, 1L, 3L, 4L, 2L, 2L, 3L, 2L, 0L, 4L, 2L, 3L, 5L, 1L, 0L, 5L, 3L]),
    Data(54,"holsclaw",1240329705,33,29,13,10,17,10,True,217,[5L, 4L, 1L, 1L, 2L, 1L, 4L, 4L, 2L, 4L, 4L, 0L, 3L, 1L, 1L, 0L, 0L, 0L, 2L, 2L, 1L, 3L, 5L, 0L, 2L, 4L, 4L, 5L, 0L, 4L]),
    Data(55,"holsclaw",1240329930,35,29,13,12,22,6,True,240,[4L, 1L, 4L, 4L, 4L, 3L, 5L, 5L, 5L, 5L, 5L, 0L, 1L, 3L, 2L, 4L, 0L, 3L, 1L, 4L, 4L, 2L, 5L, 2L, 3L, 4L, 2L, 5L, 0L, 2L]),
    Data(56,"m063834",1240331046,30,29,13,10,6,4,True,206,[2L, 3L, 4L, 4L, 5L, 4L, 3L, 3L, 4L, 0L, 1L, 4L, 4L, 4L, 3L, 3L, 5L, 2L, 4L, 2L, 2L, 5L, 1L, 4L, 4L, 1L, 4L, 4L, 4L, 4L]),
    Data(57,"whoistalg",1240331099,0,-1,0,0,0,0,False,0,[1L, 3L, 3L, 5L, 0L, 0L, 4L, 4L, 2L, 1L, 2L, 1L, 3L, 4L, 4L, 2L, 1L, 0L, 4L, 4L, 3L, 1L, 4L, 1L, 1L, 2L, 1L, 0L, 2L, 4L]),
    Data(58,"Dan.Talayco",1240331132,31,29,13,11,14,8,True,220,[3L, 3L, 5L, 5L, 3L, 4L, 5L, 4L, 4L, 5L, 1L, 4L, 2L, 1L, 2L, 2L, 3L, 1L, 1L, 5L, 2L, 1L, 0L, 3L, 0L, 5L, 5L, 5L, 0L, 3L]),
    Data(59,"m063834",1240331240,30,29,13,13,13,12,True,206,[0L, 5L, 0L, 2L, 0L, 3L, 3L, 0L, 5L, 5L, 5L, 3L, 3L, 3L, 3L, 1L, 5L, 5L, 3L, 5L, 2L, 5L, 1L, 2L, 0L, 5L, 2L, 0L, 0L, 1L]),
    Data(60,"KielAC",1240332028,32,29,13,10,17,11,True,212,[4L, 2L, 4L, 1L, 5L, 0L, 0L, 4L, 1L, 2L, 3L, 0L, 3L, 3L, 5L, 5L, 5L, 3L, 3L, 2L, 3L, 2L, 4L, 1L, 2L, 0L, 1L, 5L, 1L, 1L]),
    Data(61,"KielAC",1240332474,31,29,13,13,3,2,True,201,[3L, 0L, 3L, 1L, 3L, 5L, 2L, 4L, 4L, 1L, 5L, 1L, 4L, 4L, 3L, 4L, 1L, 2L, 5L, 2L, 2L, 4L, 4L, 1L, 2L, 5L, 5L, 3L, 2L, 4L]),
    Data(62,"rob.sherwood",1240332484,34,29,13,11,21,12,True,224,[5L, 4L, 0L, 0L, 4L, 2L, 2L, 2L, 2L, 2L, 4L, 5L, 2L, 0L, 3L, 2L, 2L, 0L, 3L, 1L, 4L, 2L, 0L, 2L, 2L, 0L, 4L, 5L, 5L, 3L]),
    Data(63,"brandon.heller",1240332760,34,29,13,10,13,11,True,205,[0L, 4L, 0L, 1L, 3L, 4L, 0L, 3L, 5L, 3L, 3L, 4L, 5L, 3L, 4L, 1L, 4L, 1L, 4L, 5L, 4L, 3L, 5L, 3L, 3L, 3L, 1L, 0L, 5L, 5L]),
    Data(64,"rob.sherwood",1240332784,30,29,13,12,6,4,True,204,[1L, 0L, 5L, 4L, 5L, 5L, 5L, 1L, 1L, 5L, 0L, 5L, 3L, 2L, 4L, 3L, 2L, 2L, 5L, 5L, 4L, 3L, 5L, 4L, 2L, 5L, 1L, 1L, 2L, 5L]),
    Data(65,"Burton.MA3",1240333239,30,29,13,11,4,3,True,208,[3L, 2L, 5L, 1L, 0L, 4L, 3L, 1L, 5L, 0L, 0L, 2L, 4L, 3L, 3L, 0L, 0L, 3L, 4L, 0L, 3L, 1L, 0L, 2L, 4L, 5L, 2L, 5L, 4L, 1L]),
    Data(66,"HOWLSvolunteer",1240333257,35,29,13,8,15,8,True,219,[2L, 3L, 4L, 5L, 2L, 4L, 2L, 5L, 3L, 1L, 2L, 2L, 2L, 1L, 2L, 2L, 0L, 5L, 3L, 2L, 2L, 2L, 0L, 1L, 2L, 3L, 1L, 5L, 0L, 1L]),
    Data(67,"rob.sherwood",1240333386,31,29,13,13,6,6,True,206,[1L, 3L, 0L, 1L, 3L, 5L, 3L, 3L, 4L, 3L, 5L, 1L, 1L, 0L, 3L, 2L, 5L, 1L, 4L, 1L, 1L, 0L, 5L, 3L, 1L, 1L, 4L, 5L, 4L, 2L]),
    Data(68,"jsylvest",1240333981,30,29,13,11,6,6,True,201,[5L, 2L, 0L, 4L, 2L, 1L, 0L, 0L, 4L, 2L, 0L, 2L, 5L, 5L, 5L, 2L, 5L, 4L, 3L, 4L, 1L, 1L, 2L, 5L, 3L, 4L, 3L, 4L, 2L, 1L]),
    Data(69,"anmattos",1240334464,30,29,13,10,6,5,True,204,[5L, 1L, 5L, 4L, 1L, 5L, 1L, 5L, 1L, 1L, 1L, 2L, 2L, 5L, 2L, 0L, 1L, 0L, 5L, 4L, 1L, 3L, 0L, 5L, 1L, 2L, 1L, 4L, 4L, 3L]),
    Data(70,"neda.beheshti",1240334805,31,29,13,12,17,6,True,224,[0L, 2L, 2L, 1L, 2L, 5L, 1L, 1L, 1L, 5L, 1L, 4L, 4L, 5L, 4L, 5L, 0L, 2L, 3L, 1L, 2L, 5L, 4L, 0L, 0L, 5L, 4L, 0L, 2L, 3L]),
    Data(71,"Mariah.Merritt",1240335165,16,8,13,7,3,0,True,40,[5L, 3L, 1L, 1L, 4L, 3L, 0L, 2L, 0L, 0L, 3L, 3L, 2L, 0L, 3L, 4L, 2L, 1L, 1L, 5L, 5L, 0L, 3L, 3L, 5L, 1L, 0L, 2L, 4L, 2L]),
    Data(72,"Mariah.Merritt",1240335306,34,29,13,11,15,12,True,212,[3L, 4L, 1L, 4L, 3L, 4L, 3L, 3L, 1L, 1L, 0L, 5L, 3L, 1L, 5L, 4L, 1L, 3L, 0L, 5L, 0L, 5L, 1L, 2L, 3L, 3L, 3L, 5L, 2L, 2L]),
    Data(73,"slhanks",1240335852,30,29,13,12,14,9,True,220,[1L, 2L, 2L, 2L, 2L, 3L, 2L, 2L, 4L, 1L, 5L, 3L, 2L, 2L, 5L, 2L, 0L, 5L, 1L, 4L, 5L, 4L, 3L, 1L, 5L, 2L, 1L, 3L, 0L, 0L]),
    Data(74,"JoyMarieJohnson",1240336113,4,3,4,2,0,0,False,0,[0L, 0L, 5L, 1L, 3L, 2L, 3L, 0L, 5L, 0L, 0L, 4L, 2L, 0L, 4L, 4L, 1L, 3L, 1L, 2L, 0L, 4L, 2L, 2L, 3L, 1L, 5L, 4L, 0L, 3L]),
    Data(75,"Mariah.Merritt",1240337296,33,29,13,8,16,15,True,206,[4L, 5L, 5L, 3L, 5L, 5L, 1L, 4L, 2L, 0L, 2L, 5L, 1L, 2L, 4L, 2L, 2L, 5L, 0L, 5L, 2L, 1L, 4L, 4L, 2L, 5L, 1L, 1L, 3L, 1L]),
    Data(76,"rdblue",1240338069,1,0,1,1,0,0,False,0,[1L, 0L, 3L, 3L, 0L, 3L, 4L, 1L, 2L, 0L, 0L, 3L, 4L, 1L, 1L, 0L, 0L, 1L, 1L, 1L, 4L, 5L, 4L, 5L, 2L, 5L, 4L, 2L, 3L, 4L]),
    Data(77,"FESOJJOSEF",1240338258,16,8,13,8,3,1,True,40,[1L, 0L, 5L, 5L, 4L, 4L, 2L, 0L, 3L, 2L, 5L, 3L, 1L, 2L, 5L, 4L, 1L, 0L, 3L, 2L, 5L, 4L, 1L, 4L, 4L, 2L, 4L, 2L, 2L, 1L]),
    Data(78,"FESOJJOSEF",1240338462,30,29,13,8,12,5,True,218,[3L, 0L, 3L, 4L, 5L, 3L, 4L, 3L, 5L, 4L, 4L, 5L, 5L, 0L, 5L, 5L, 2L, 3L, 2L, 0L, 2L, 0L, 1L, 2L, 0L, 2L, 5L, 5L, 0L, 0L]),
    Data(79,"anmattos",1240338674,31,29,13,12,9,7,True,208,[1L, 1L, 1L, 1L, 2L, 5L, 0L, 4L, 2L, 3L, 3L, 1L, 0L, 3L, 2L, 2L, 4L, 2L, 4L, 0L, 3L, 0L, 2L, 2L, 4L, 1L, 3L, 1L, 3L, 2L]),
    Data(80,"Gaylena.Howell",1240339160,0,-1,0,0,0,0,False,0,[5L, 5L, 2L, 0L, 1L, 5L, 1L, 2L, 4L, 1L, 4L, 2L, 2L, 3L, 4L, 5L, 0L, 2L, 3L, 0L, 2L, 2L, 2L, 5L, 3L, 3L, 3L, 3L, 4L, 5L]),
    Data(81,"appenz",1240339184,31,29,13,12,15,6,True,218,[4L, 1L, 1L, 4L, 1L, 1L, 4L, 0L, 5L, 4L, 2L, 1L, 5L, 2L, 5L, 2L, 0L, 4L, 1L, 0L, 3L, 0L, 3L, 5L, 4L, 5L, 1L, 3L, 2L, 4L]),
    Data(82,"jaclyn.lgy",1240340758,30,29,13,12,11,4,True,219,[4L, 4L, 4L, 3L, 2L, 4L, 1L, 3L, 4L, 4L, 0L, 2L, 3L, 3L, 0L, 0L, 0L, 3L, 3L, 5L, 2L, 2L, 0L, 4L, 1L, 1L, 2L, 2L, 5L, 3L]),
    Data(83,"jaclyn.lgy",1240341130,30,29,13,12,3,3,True,202,[0L, 5L, 5L, 5L, 1L, 3L, 0L, 2L, 0L, 5L, 4L, 3L, 0L, 5L, 2L, 4L, 4L, 4L, 4L, 3L, 2L, 4L, 2L, 5L, 1L, 5L, 5L, 1L, 3L, 5L]),
    Data(84,"disaacson",1240341490,30,29,13,13,8,8,True,207,[1L, 4L, 5L, 1L, 3L, 5L, 4L, 3L, 4L, 4L, 4L, 4L, 5L, 5L, 5L, 1L, 0L, 2L, 4L, 1L, 4L, 0L, 0L, 0L, 5L, 4L, 0L, 1L, 3L, 1L]),
    Data(85,"ashley.schelske",1240341733,30,29,13,11,9,6,True,212,[1L, 2L, 4L, 1L, 5L, 3L, 0L, 0L, 0L, 4L, 1L, 5L, 0L, 2L, 2L, 4L, 3L, 3L, 5L, 3L, 5L, 4L, 5L, 3L, 4L, 0L, 5L, 2L, 1L, 3L]),
    Data(86,"harry.robertson",1240341971,30,29,13,13,16,6,True,223,[5L, 3L, 1L, 0L, 4L, 5L, 1L, 2L, 4L, 4L, 3L, 3L, 1L, 4L, 4L, 0L, 5L, 3L, 2L, 1L, 4L, 5L, 0L, 3L, 1L, 0L, 2L, 1L, 3L, 4L]),
    Data(87,"coramdeo0719",1240342300,13,5,13,5,0,0,True,25,[1L, 2L, 4L, 3L, 2L, 2L, 5L, 4L, 4L, 5L, 2L, 5L, 0L, 3L, 1L, 2L, 1L, 4L, 3L, 4L, 4L, 0L, 4L, 3L, 2L, 5L, 3L, 4L, 3L, 0L]),
    Data(88,"coramdeo0719",1240342342,0,-1,0,0,0,0,False,0,[4L, 5L, 4L, 2L, 4L, 3L, 3L, 0L, 0L, 5L, 4L, 1L, 5L, 5L, 4L, 0L, 3L, 3L, 1L, 1L, 3L, 3L, 4L, 5L, 3L, 1L, 3L, 0L, 3L, 1L]),
    Data(89,"shannon.m.burke",1240343118,30,29,13,12,7,5,True,212,[5L, 5L, 0L, 3L, 0L, 5L, 2L, 4L, 2L, 0L, 2L, 1L, 3L, 5L, 1L, 4L, 4L, 4L, 3L, 1L, 0L, 1L, 0L, 4L, 2L, 5L, 3L, 1L, 4L, 4L]),
    Data(90,"croach01",1240343908,30,29,13,9,14,11,True,212,[0L, 3L, 2L, 3L, 0L, 5L, 0L, 4L, 1L, 2L, 5L, 0L, 2L, 4L, 1L, 1L, 5L, 0L, 5L, 1L, 3L, 4L, 2L, 2L, 2L, 1L, 3L, 1L, 4L, 3L]),
    Data(91,"croach01",1240344062,32,29,7,6,10,7,True,205,[4L, 1L, 5L, 0L, 5L, 2L, 0L, 2L, 5L, 1L, 4L, 5L, 4L, 2L, 2L, 3L, 0L, 4L, 4L, 4L, 0L, 3L, 4L, 1L, 5L, 1L, 3L, 1L, 3L, 4L]),
    Data(92,"jnaous",1240346419,31,29,13,11,13,10,True,212,[1L, 0L, 5L, 3L, 4L, 3L, 0L, 2L, 5L, 4L, 5L, 3L, 3L, 4L, 3L, 0L, 2L, 0L, 3L, 3L, 4L, 5L, 3L, 2L, 3L, 4L, 5L, 2L, 0L, 3L]),
    Data(93,"Derek.Anastasiades",1240348941,31,29,13,11,14,10,True,214,[1L, 0L, 1L, 5L, 5L, 1L, 0L, 5L, 5L, 5L, 2L, 1L, 5L, 5L, 4L, 0L, 2L, 1L, 5L, 2L, 3L, 2L, 0L, 4L, 5L, 1L, 4L, 4L, 4L, 3L]),
    Data(94,"buyukkaya",1240349769,32,29,13,9,13,13,True,205,[2L, 0L, 3L, 4L, 5L, 5L, 2L, 0L, 2L, 5L, 2L, 5L, 3L, 2L, 0L, 4L, 1L, 2L, 0L, 1L, 3L, 5L, 5L, 5L, 2L, 4L, 2L, 2L, 1L, 4L]),
    Data(95,"panther47",1240349923,15,7,13,5,2,0,True,35,[2L, 5L, 0L, 3L, 5L, 2L, 4L, 5L, 3L, 5L, 0L, 3L, 4L, 2L, 2L, 4L, 5L, 5L, 3L, 3L, 4L, 2L, 5L, 4L, 0L, 4L, 5L, 0L, 1L, 1L]),
    Data(96,"buyukkaya",1240349964,33,29,13,8,14,14,True,199,[1L, 3L, 3L, 4L, 5L, 1L, 3L, 1L, 1L, 0L, 2L, 4L, 0L, 1L, 3L, 1L, 0L, 1L, 4L, 0L, 5L, 2L, 1L, 4L, 0L, 5L, 2L, 5L, 1L, 3L]),
    Data(97,"panther47",1240350033,35,27,13,10,22,14,True,135,[0L, 2L, 2L, 0L, 2L, 5L, 5L, 5L, 4L, 0L, 5L, 0L, 3L, 3L, 5L, 5L, 4L, 0L, 1L, 3L, 2L, 2L, 1L, 3L, 1L, 4L, 0L, 0L, 1L, 2L]),
    Data(98,"professorcrabbe",1240350944,30,29,13,11,5,5,True,199,[2L, 3L, 5L, 5L, 1L, 4L, 1L, 3L, 1L, 3L, 0L, 4L, 0L, 3L, 4L, 3L, 2L, 1L, 3L, 1L, 1L, 3L, 4L, 5L, 5L, 3L, 5L, 4L, 0L, 2L]),
    Data(99,"LadyGYU",1240351017,31,29,13,9,14,13,True,202,[2L, 2L, 4L, 3L, 2L, 0L, 1L, 5L, 1L, 4L, 2L, 2L, 4L, 5L, 1L, 2L, 1L, 3L, 3L, 3L, 1L, 5L, 4L, 0L, 3L, 5L, 3L, 4L, 5L, 2L]),
    Data(100,"professorcrabbe",1240351312,30,29,13,13,3,3,True,204,[1L, 1L, 1L, 1L, 0L, 3L, 1L, 0L, 0L, 2L, 3L, 3L, 2L, 2L, 5L, 2L, 4L, 3L, 2L, 2L, 4L, 0L, 1L, 0L, 4L, 2L, 2L, 0L, 5L, 4L]),
    Data(101,"razmatazern",1240351568,31,29,13,10,18,14,True,217,[4L, 3L, 0L, 4L, 3L, 5L, 2L, 0L, 0L, 5L, 0L, 1L, 0L, 4L, 1L, 1L, 3L, 0L, 5L, 5L, 0L, 5L, 0L, 5L, 0L, 3L, 5L, 5L, 4L, 1L]),
    Data(102,"razmatazern",1240351757,31,29,13,10,14,14,True,198,[0L, 2L, 3L, 1L, 0L, 0L, 5L, 4L, 3L, 5L, 2L, 5L, 5L, 0L, 5L, 5L, 1L, 4L, 4L, 2L, 2L, 1L, 3L, 3L, 3L, 5L, 4L, 5L, 5L, 1L]),
    Data(103,"razmatazern",1240351866,30,29,13,9,13,13,True,204,[1L, 5L, 2L, 3L, 5L, 4L, 0L, 3L, 5L, 5L, 4L, 4L, 5L, 2L, 1L, 2L, 5L, 4L, 1L, 3L, 4L, 4L, 2L, 3L, 4L, 5L, 3L, 2L, 1L, 2L]),
    Data(104,"professorcrabbe",1240351878,30,29,13,12,1,1,True,203,[1L, 4L, 0L, 4L, 5L, 1L, 4L, 5L, 1L, 0L, 3L, 4L, 4L, 0L, 5L, 3L, 3L, 5L, 1L, 2L, 2L, 2L, 1L, 2L, 0L, 3L, 0L, 2L, 0L, 5L]),
    Data(105,"razmatazern",1240351975,31,29,13,11,3,3,True,204,[4L, 2L, 5L, 4L, 0L, 3L, 3L, 2L, 4L, 1L, 3L, 4L, 2L, 2L, 4L, 4L, 3L, 3L, 3L, 3L, 5L, 0L, 0L, 3L, 1L, 4L, 5L, 0L, 0L, 4L]),
    Data(106,"Nair.AbhilashC",1240354046,20,12,13,9,7,2,True,60,[1L, 3L, 3L, 2L, 5L, 5L, 3L, 1L, 2L, 5L, 0L, 3L, 2L, 2L, 4L, 3L, 4L, 3L, 4L, 0L, 5L, 3L, 2L, 3L, 5L, 4L, 1L, 3L, 4L, 4L]),
    Data(107,"alexiswilliamsinc",1240354069,30,29,13,11,10,5,True,220,[5L, 3L, 5L, 1L, 1L, 4L, 4L, 2L, 3L, 5L, 0L, 2L, 5L, 5L, 5L, 4L, 4L, 3L, 0L, 3L, 2L, 2L, 5L, 0L, 5L, 3L, 5L, 5L, 3L, 3L]),
    Data(108,"tyler.holsclaw",1240354645,30,22,13,8,17,7,True,110,[5L, 2L, 2L, 2L, 4L, 1L, 1L, 2L, 5L, 0L, 0L, 5L, 2L, 2L, 2L, 1L, 4L, 5L, 1L, 1L, 2L, 1L, 0L, 1L, 0L, 5L, 2L, 3L, 0L, 2L]),
    Data(109,"tyler.holsclaw",1240354964,36,29,13,9,22,20,True,205,[3L, 0L, 2L, 0L, 2L, 3L, 4L, 4L, 0L, 0L, 3L, 0L, 0L, 3L, 5L, 2L, 2L, 1L, 0L, 5L, 2L, 2L, 0L, 2L, 1L, 0L, 1L, 4L, 4L, 0L]),
    Data(110,"tyler.holsclaw",1240355307,30,29,13,12,8,8,True,207,[5L, 4L, 0L, 2L, 5L, 5L, 0L, 1L, 5L, 3L, 1L, 5L, 2L, 1L, 1L, 5L, 0L, 1L, 3L, 0L, 3L, 2L, 4L, 3L, 5L, 5L, 3L, 0L, 5L, 1L]),
    Data(111,"Carrie.Nyden",1240355454,28,20,13,7,15,12,True,100,[0L, 5L, 5L, 1L, 0L, 2L, 1L, 3L, 4L, 2L, 3L, 5L, 5L, 1L, 0L, 3L, 5L, 5L, 1L, 4L, 5L, 1L, 0L, 3L, 0L, 3L, 2L, 4L, 3L, 1L]),
    Data(112,"rdnobles33",1240355463,30,29,13,12,2,2,True,196,[4L, 0L, 3L, 2L, 3L, 3L, 4L, 1L, 3L, 2L, 0L, 3L, 5L, 5L, 0L, 5L, 0L, 3L, 2L, 5L, 3L, 2L, 5L, 4L, 0L, 3L, 1L, 0L, 5L, 4L]),
    Data(113,"theone070@aol.com",1240355606,30,29,13,10,15,6,True,221,[2L, 0L, 3L, 5L, 2L, 4L, 3L, 2L, 4L, 1L, 2L, 3L, 4L, 5L, 1L, 5L, 1L, 2L, 5L, 0L, 1L, 5L, 5L, 1L, 2L, 3L, 0L, 1L, 3L, 4L]),
    Data(114,"apmosley",1240356452,19,11,13,9,6,0,True,55,[0L, 5L, 5L, 1L, 0L, 5L, 3L, 1L, 3L, 4L, 2L, 4L, 2L, 1L, 0L, 5L, 2L, 0L, 5L, 3L, 5L, 3L, 2L, 2L, 4L, 1L, 3L, 2L, 1L, 5L]),
    Data(115,"brittneyafoster@yahoo.com",1240356577,22,14,13,8,9,4,True,70,[4L, 0L, 0L, 2L, 4L, 5L, 1L, 0L, 3L, 5L, 5L, 1L, 4L, 3L, 1L, 1L, 1L, 3L, 3L, 1L, 4L, 4L, 1L, 1L, 5L, 0L, 4L, 2L, 5L, 3L]),
    Data(116,"timur.chabuk",1240357293,31,29,13,12,16,14,True,213,[1L, 3L, 1L, 0L, 2L, 1L, 1L, 0L, 3L, 5L, 4L, 2L, 0L, 5L, 2L, 2L, 1L, 4L, 0L, 5L, 4L, 1L, 4L, 0L, 2L, 2L, 1L, 0L, 0L, 0L]),
    Data(117,"timur.chabuk",1240357574,30,29,13,13,9,6,True,213,[2L, 3L, 1L, 2L, 5L, 3L, 1L, 5L, 4L, 0L, 5L, 2L, 2L, 3L, 0L, 5L, 0L, 5L, 3L, 5L, 0L, 0L, 4L, 2L, 2L, 0L, 3L, 3L, 5L, 3L]),
    Data(118,"Arictus",1240358248,31,29,13,9,12,11,True,209,[2L, 1L, 1L, 3L, 4L, 2L, 4L, 5L, 3L, 3L, 1L, 3L, 4L, 1L, 2L, 5L, 2L, 3L, 4L, 4L, 0L, 5L, 4L, 2L, 1L, 3L, 0L, 1L, 0L, 0L]),
    Data(119,"Katherine.E.Chase",1240358521,31,29,13,10,12,9,True,211,[0L, 2L, 4L, 2L, 5L, 5L, 2L, 1L, 3L, 4L, 0L, 3L, 1L, 3L, 3L, 5L, 3L, 3L, 0L, 0L, 4L, 5L, 3L, 5L, 4L, 5L, 3L, 3L, 5L, 1L]),
    Data(120,"Cherry.Heather",1240359770,33,25,13,11,20,2,True,125,[0L, 5L, 3L, 5L, 5L, 2L, 0L, 3L, 3L, 4L, 0L, 2L, 2L, 5L, 1L, 3L, 4L, 0L, 1L, 0L, 5L, 5L, 0L, 1L, 4L, 2L, 1L, 2L, 3L, 0L]),
    Data(121,"saketn",1240360300,30,29,13,11,10,3,True,219,[4L, 2L, 0L, 5L, 3L, 1L, 5L, 4L, 0L, 4L, 0L, 0L, 2L, 3L, 3L, 1L, 3L, 0L, 3L, 0L, 1L, 2L, 0L, 5L, 3L, 0L, 3L, 2L, 0L, 2L]),
    Data(122,"saketn",1240360566,23,15,13,6,10,6,True,75,[0L, 3L, 3L, 3L, 1L, 5L, 0L, 3L, 1L, 3L, 2L, 0L, 1L, 4L, 0L, 2L, 3L, 0L, 2L, 3L, 5L, 4L, 5L, 4L, 3L, 5L, 2L, 3L, 0L, 3L]),
    Data(123,"spammetoheck",1240360992,30,29,13,13,3,2,True,207,[2L, 4L, 3L, 4L, 2L, 4L, 3L, 3L, 4L, 4L, 1L, 2L, 5L, 2L, 0L, 1L, 1L, 5L, 0L, 5L, 3L, 0L, 5L, 0L, 3L, 2L, 0L, 5L, 5L, 2L]),
    Data(124,"rickkennedy7",1240361123,33,29,13,10,16,13,True,208,[4L, 0L, 2L, 2L, 4L, 2L, 3L, 4L, 2L, 3L, 5L, 2L, 1L, 1L, 5L, 2L, 5L, 4L, 4L, 3L, 4L, 1L, 0L, 3L, 3L, 0L, 5L, 4L, 5L, 1L]),
    Data(125,"ansutton",1240361270,32,29,13,10,17,13,True,214,[0L, 3L, 4L, 2L, 1L, 2L, 1L, 1L, 2L, 1L, 2L, 1L, 4L, 3L, 3L, 1L, 0L, 4L, 5L, 3L, 4L, 4L, 0L, 4L, 1L, 0L, 3L, 1L, 1L, 3L]),
    Data(126,"noelle.wanzer",1240361447,30,29,13,11,14,9,True,215,[1L, 2L, 4L, 4L, 1L, 1L, 5L, 3L, 2L, 2L, 0L, 1L, 2L, 1L, 0L, 0L, 2L, 4L, 1L, 0L, 2L, 0L, 2L, 5L, 5L, 0L, 2L, 2L, 3L, 4L]),
    Data(127,"jamie.declue",1240361567,30,29,13,9,10,10,True,204,[1L, 0L, 5L, 0L, 5L, 5L, 2L, 0L, 0L, 0L, 3L, 5L, 1L, 2L, 2L, 5L, 3L, 3L, 2L, 0L, 1L, 2L, 4L, 2L, 3L, 5L, 2L, 3L, 2L, 5L]),
    Data(128,"ramil.lim",1240361764,22,14,13,7,9,5,True,70,[5L, 4L, 2L, 5L, 4L, 0L, 4L, 0L, 4L, 4L, 5L, 0L, 0L, 3L, 1L, 0L, 0L, 4L, 5L, 3L, 1L, 5L, 2L, 3L, 3L, 2L, 0L, 5L, 2L, 1L]),
    Data(129,"jamie.declue",1240361884,30,29,13,13,2,1,True,203,[3L, 3L, 0L, 4L, 4L, 1L, 4L, 0L, 0L, 2L, 4L, 5L, 1L, 4L, 3L, 0L, 4L, 5L, 5L, 3L, 5L, 0L, 0L, 3L, 5L, 4L, 2L, 0L, 0L, 3L]),
    Data(130,"echaffin1984",1240362036,31,29,12,12,0,0,True,196,[2L, 0L, 3L, 5L, 1L, 4L, 5L, 3L, 5L, 3L, 4L, 4L, 1L, 3L, 2L, 2L, 4L, 4L, 3L, 3L, 2L, 1L, 0L, 1L, 2L, 4L, 4L, 2L, 3L, 1L]),
    Data(131,"ramil.lim",1240362172,31,29,13,11,7,7,True,202,[5L, 5L, 5L, 4L, 1L, 2L, 3L, 3L, 5L, 1L, 5L, 2L, 0L, 4L, 2L, 2L, 5L, 4L, 4L, 0L, 0L, 2L, 2L, 5L, 4L, 3L, 2L, 5L, 4L, 1L]),
    Data(132,"echaffin1984",1240362348,0,-1,0,0,0,0,False,0,[0L, 0L, 4L, 5L, 0L, 3L, 2L, 2L, 3L, 2L, 4L, 4L, 4L, 5L, 5L, 5L, 1L, 3L, 1L, 0L, 1L, 0L, 4L, 3L, 4L, 4L, 3L, 1L, 3L, 5L]),
    Data(133,"mrsholsclaw",1240363374,32,29,13,9,14,12,True,209,[1L, 3L, 2L, 3L, 4L, 2L, 5L, 1L, 5L, 5L, 4L, 0L, 4L, 5L, 5L, 2L, 4L, 4L, 1L, 4L, 5L, 4L, 4L, 1L, 2L, 4L, 1L, 5L, 1L, 2L]),
    Data(134,"mrsholsclaw",1240363498,21,13,13,6,8,3,True,65,[1L, 0L, 5L, 1L, 3L, 0L, 0L, 0L, 5L, 4L, 5L, 4L, 1L, 3L, 5L, 1L, 3L, 2L, 4L, 2L, 1L, 5L, 3L, 5L, 3L, 5L, 2L, 0L, 3L, 2L]),
    Data(135,"mrsholsclaw",1240363531,19,11,13,5,6,4,True,55,[1L, 2L, 5L, 1L, 3L, 3L, 4L, 0L, 3L, 0L, 3L, 3L, 1L, 5L, 5L, 0L, 5L, 0L, 3L, 1L, 4L, 2L, 1L, 0L, 5L, 3L, 2L, 4L, 0L, 4L]),
    Data(136,"g9coving",1240363554,30,29,13,13,2,2,True,206,[4L, 4L, 0L, 2L, 1L, 5L, 1L, 5L, 0L, 5L, 4L, 4L, 5L, 2L, 4L, 5L, 4L, 0L, 2L, 4L, 0L, 4L, 2L, 2L, 0L, 5L, 2L, 3L, 3L, 4L]),
    Data(137,"mrsholsclaw",1240363570,34,29,13,7,21,19,True,207,[3L, 0L, 2L, 2L, 0L, 0L, 5L, 5L, 5L, 0L, 3L, 1L, 2L, 1L, 2L, 4L, 3L, 1L, 2L, 4L, 3L, 1L, 3L, 0L, 2L, 1L, 1L, 3L, 2L, 3L]),
    Data(138,"prayforMOJO524",1240363822,30,29,13,13,17,10,True,218,[2L, 5L, 3L, 0L, 3L, 0L, 5L, 3L, 5L, 4L, 4L, 5L, 3L, 0L, 3L, 1L, 4L, 1L, 0L, 0L, 5L, 1L, 3L, 0L, 4L, 1L, 2L, 5L, 2L, 1L]),
    Data(139,"Cdobsonwv",1240363984,18,10,13,3,5,2,True,50,[1L, 0L, 4L, 5L, 3L, 5L, 0L, 5L, 3L, 5L, 4L, 3L, 1L, 5L, 2L, 5L, 2L, 5L, 3L, 0L, 2L, 1L, 4L, 0L, 2L, 1L, 1L, 1L, 2L, 3L]),
    Data(140,"kellyehayes",1240364913,31,29,13,12,11,10,True,211,[5L, 4L, 2L, 1L, 0L, 4L, 0L, 1L, 4L, 2L, 3L, 2L, 1L, 0L, 0L, 2L, 3L, 1L, 5L, 3L, 2L, 0L, 1L, 2L, 1L, 1L, 4L, 2L, 3L, 4L]),
    Data(141,"SteveUnderhill",1240365318,31,29,13,13,12,5,True,218,[4L, 5L, 4L, 2L, 4L, 4L, 1L, 3L, 4L, 4L, 5L, 5L, 3L, 1L, 3L, 5L, 0L, 1L, 1L, 1L, 3L, 0L, 4L, 4L, 2L, 3L, 2L, 1L, 3L, 4L]),
    Data(142,"firetora",1240365443,31,29,13,13,13,6,True,221,[4L, 0L, 1L, 0L, 2L, 5L, 5L, 2L, 3L, 4L, 1L, 4L, 0L, 3L, 0L, 4L, 5L, 3L, 5L, 5L, 3L, 0L, 4L, 1L, 1L, 5L, 3L, 4L, 5L, 1L]),
    Data(143,"flinn.jennifer",1240366799,32,29,13,7,12,10,True,203,[3L, 4L, 3L, 3L, 4L, 3L, 3L, 1L, 3L, 5L, 4L, 3L, 4L, 3L, 5L, 2L, 5L, 1L, 3L, 3L, 1L, 2L, 0L, 1L, 5L, 5L, 2L, 4L, 0L, 0L]),
    Data(144,"CBynum",1240366977,6,5,6,5,0,0,False,0,[4L, 5L, 1L, 2L, 1L, 0L, 5L, 5L, 1L, 1L, 4L, 0L, 0L, 4L, 1L, 4L, 0L, 4L, 0L, 2L, 2L, 0L, 4L, 3L, 0L, 5L, 3L, 1L, 5L, 1L]),
    Data(145,"eamclemore",1240367066,30,29,13,12,15,8,True,225,[5L, 1L, 1L, 2L, 1L, 5L, 2L, 1L, 4L, 1L, 3L, 4L, 3L, 4L, 3L, 2L, 2L, 1L, 5L, 3L, 2L, 1L, 1L, 4L, 0L, 0L, 1L, 2L, 0L, 4L]),
    Data(146,"eamclemore",1240367421,31,29,13,11,18,12,True,219,[5L, 3L, 1L, 2L, 5L, 4L, 2L, 0L, 4L, 2L, 4L, 4L, 4L, 1L, 2L, 1L, 4L, 3L, 5L, 3L, 5L, 0L, 2L, 1L, 1L, 3L, 5L, 4L, 0L, 1L]),
    Data(147,"Kev.McCadden",1240371345,31,29,13,11,8,7,True,205,[4L, 3L, 2L, 4L, 0L, 1L, 2L, 1L, 3L, 1L, 4L, 4L, 2L, 4L, 4L, 3L, 4L, 0L, 5L, 4L, 2L, 4L, 5L, 2L, 2L, 5L, 2L, 5L, 1L, 3L]),
    Data(148,"Kev.McCadden",1240371605,34,29,13,10,16,15,True,211,[1L, 0L, 2L, 0L, 3L, 3L, 4L, 5L, 1L, 1L, 5L, 2L, 1L, 4L, 4L, 0L, 1L, 2L, 2L, 2L, 1L, 0L, 4L, 4L, 4L, 0L, 0L, 2L, 5L, 5L]),
    Data(149,"Nair.AbhilashC",1240372698,33,29,13,10,20,10,True,223,[4L, 4L, 5L, 1L, 1L, 1L, 1L, 0L, 1L, 0L, 1L, 2L, 3L, 2L, 0L, 1L, 5L, 3L, 0L, 2L, 1L, 2L, 2L, 5L, 4L, 2L, 4L, 0L, 2L, 1L]),
    Data(150,"Nair.AbhilashC",1240372833,4,3,4,4,0,0,False,0,[4L, 1L, 5L, 5L, 4L, 2L, 1L, 5L, 2L, 5L, 0L, 5L, 4L, 1L, 1L, 2L, 0L, 5L, 1L, 0L, 4L, 3L, 1L, 2L, 2L, 0L, 1L, 0L, 5L, 3L]),
    Data(151,"jlittl13@mail.nccu.edu",1240376363,18,10,13,4,5,4,True,50,[3L, 4L, 3L, 3L, 3L, 0L, 0L, 3L, 2L, 1L, 5L, 2L, 3L, 2L, 4L, 4L, 5L, 0L, 0L, 1L, 0L, 2L, 2L, 4L, 2L, 4L, 3L, 5L, 5L, 2L]),
    Data(152,"jfriedl",1240377127,30,29,10,9,0,0,True,197,[0L, 5L, 1L, 2L, 4L, 0L, 5L, 1L, 1L, 4L, 0L, 2L, 5L, 5L, 3L, 5L, 3L, 0L, 1L, 4L, 0L, 3L, 0L, 0L, 0L, 2L, 4L, 4L, 5L, 0L]),
    Data(153,"michael.styer",1240380734,30,29,13,13,4,2,True,206,[2L, 0L, 3L, 5L, 4L, 3L, 3L, 0L, 5L, 5L, 3L, 5L, 4L, 2L, 0L, 3L, 4L, 1L, 1L, 5L, 3L, 1L, 2L, 5L, 2L, 4L, 5L, 4L, 1L, 4L]),
    Data(154,"michael.styer",1240381104,30,29,13,13,2,1,True,204,[4L, 1L, 5L, 1L, 5L, 3L, 2L, 5L, 3L, 4L, 5L, 4L, 1L, 2L, 5L, 4L, 3L, 4L, 0L, 0L, 1L, 1L, 2L, 1L, 4L, 0L, 5L, 0L, 2L, 0L]),
    Data(155,"KielAC",1240381726,32,29,13,8,19,19,True,197,[4L, 5L, 1L, 0L, 2L, 2L, 2L, 3L, 0L, 5L, 4L, 2L, 3L, 4L, 4L, 0L, 5L, 5L, 3L, 3L, 3L, 5L, 4L, 5L, 5L, 4L, 1L, 2L, 5L, 5L]),
    Data(156,"zjlang83",1240388461,31,29,13,11,9,5,True,213,[3L, 5L, 2L, 3L, 1L, 0L, 2L, 5L, 4L, 5L, 0L, 0L, 2L, 2L, 4L, 5L, 5L, 4L, 5L, 0L, 4L, 2L, 2L, 0L, 2L, 3L, 2L, 2L, 0L, 3L]),
    Data(157,"lanajo1234@hotmail.com",1240400788,32,29,13,10,13,12,True,202,[3L, 2L, 1L, 2L, 4L, 5L, 0L, 5L, 4L, 5L, 2L, 2L, 4L, 3L, 1L, 4L, 2L, 1L, 5L, 2L, 4L, 5L, 4L, 2L, 2L, 3L, 2L, 3L, 2L, 1L]),
    Data(158,"glen.gibb",1240408015,31,29,13,13,10,10,True,210,[5L, 3L, 2L, 3L, 5L, 0L, 0L, 5L, 1L, 0L, 2L, 2L, 3L, 5L, 0L, 4L, 3L, 3L, 0L, 2L, 0L, 0L, 2L, 3L, 3L, 2L, 1L, 3L, 0L, 1L]),
    Data(159,"glen.gibb",1240408303,30,29,13,13,2,2,True,203,[3L, 3L, 3L, 4L, 3L, 3L, 0L, 3L, 5L, 4L, 0L, 3L, 3L, 1L, 3L, 4L, 3L, 1L, 1L, 2L, 0L, 0L, 2L, 0L, 4L, 2L, 2L, 4L, 2L, 3L]),
    Data(160,"Underhill2010",1240414944,32,29,13,12,7,7,True,203,[1L, 5L, 5L, 5L, 2L, 2L, 5L, 3L, 5L, 3L, 0L, 2L, 1L, 5L, 3L, 5L, 0L, 0L, 5L, 2L, 5L, 2L, 3L, 5L, 2L, 2L, 4L, 2L, 2L, 3L]),
    Data(161,"Underhill2010",1240415114,31,29,13,13,14,11,True,220,[3L, 1L, 4L, 4L, 1L, 0L, 5L, 0L, 1L, 5L, 0L, 3L, 1L, 4L, 5L, 4L, 4L, 4L, 0L, 1L, 3L, 0L, 2L, 4L, 4L, 2L, 1L, 1L, 1L, 5L]),
    Data(162,"chido.enyinna",1240415819,32,29,13,9,12,9,True,212,[0L, 1L, 1L, 3L, 1L, 1L, 3L, 5L, 0L, 5L, 5L, 3L, 5L, 2L, 5L, 3L, 4L, 1L, 3L, 3L, 4L, 3L, 4L, 0L, 4L, 2L, 0L, 1L, 0L, 2L]),
    Data(163,"gillian.beans",1240416601,36,29,13,7,14,13,True,201,[1L, 3L, 3L, 4L, 3L, 2L, 0L, 1L, 5L, 0L, 1L, 2L, 0L, 1L, 1L, 1L, 5L, 4L, 5L, 3L, 4L, 5L, 0L, 2L, 5L, 4L, 3L, 1L, 1L, 0L]),
    Data(164,"qwx1984",1240419743,15,7,13,8,2,0,True,35,[2L, 1L, 4L, 0L, 0L, 3L, 1L, 0L, 1L, 3L, 1L, 3L, 0L, 0L, 2L, 4L, 5L, 5L, 3L, 0L, 1L, 5L, 0L, 4L, 1L, 2L, 5L, 0L, 4L, 5L]),
    Data(165,"Underhill2010",1240420443,30,29,13,13,5,5,True,207,[1L, 4L, 3L, 2L, 2L, 2L, 1L, 5L, 0L, 0L, 1L, 4L, 2L, 0L, 3L, 3L, 1L, 5L, 4L, 1L, 4L, 1L, 2L, 5L, 1L, 4L, 0L, 2L, 0L, 2L]),
    Data(166,"Underhill2010",1240420554,17,3,13,3,4,0,True,15,[5L, 0L, 5L, 5L, 2L, 4L, 2L, 1L, 4L, 0L, 3L, 5L, 5L, 4L, 3L, 3L, 3L, 1L, 1L, 5L, 3L, 3L, 5L, 2L, 4L, 5L, 4L, 2L, 4L, 0L]),
    Data(167,"qlin01",1240421119,31,29,13,13,4,3,True,206,[3L, 0L, 5L, 5L, 0L, 1L, 1L, 5L, 4L, 5L, 0L, 1L, 2L, 5L, 5L, 5L, 3L, 2L, 0L, 2L, 4L, 0L, 1L, 3L, 5L, 2L, 3L, 1L, 0L, 1L]),
    Data(168,"lukemcd",1240423391,30,29,11,11,0,0,True,198,[5L, 0L, 1L, 3L, 4L, 3L, 3L, 1L, 5L, 1L, 2L, 2L, 4L, 2L, 5L, 4L, 2L, 0L, 4L, 5L, 0L, 0L, 0L, 3L, 1L, 4L, 4L, 3L, 3L, 4L]),
    Data(169,"Frani.Hess",1240425339,32,29,13,9,18,13,True,211,[0L, 4L, 2L, 4L, 5L, 3L, 0L, 3L, 1L, 2L, 5L, 4L, 4L, 4L, 5L, 2L, 3L, 2L, 2L, 1L, 3L, 4L, 5L, 2L, 2L, 0L, 4L, 4L, 1L, 5L]),
    Data(170,"Frani.Hess",1240425532,31,29,13,11,12,4,True,222,[4L, 2L, 3L, 3L, 5L, 2L, 3L, 4L, 4L, 5L, 3L, 3L, 2L, 1L, 5L, 0L, 1L, 1L, 5L, 4L, 0L, 5L, 2L, 5L, 5L, 5L, 3L, 3L, 3L, 3L]),
    Data(171,"AndrewStephenson11",1240427416,35,29,13,10,19,18,True,210,[1L, 4L, 1L, 1L, 5L, 4L, 5L, 4L, 0L, 4L, 2L, 4L, 4L, 1L, 3L, 4L, 0L, 1L, 1L, 4L, 5L, 0L, 2L, 5L, 4L, 5L, 3L, 0L, 4L, 2L]),
    Data(172,"TheHurriCrane",1240429296,31,29,13,11,18,15,True,214,[2L, 4L, 1L, 3L, 2L, 4L, 2L, 5L, 1L, 3L, 2L, 2L, 1L, 0L, 1L, 1L, 1L, 1L, 2L, 2L, 2L, 1L, 5L, 5L, 3L, 1L, 5L, 1L, 5L, 2L]),
    Data(173,"mattmerkt",1240432061,31,29,13,7,17,16,True,201,[4L, 0L, 2L, 5L, 2L, 1L, 0L, 3L, 0L, 5L, 5L, 1L, 4L, 0L, 5L, 4L, 3L, 1L, 1L, 0L, 1L, 4L, 2L, 5L, 1L, 2L, 2L, 1L, 3L, 5L]),
    Data(174,"becky.berryman",1240432099,31,29,13,11,17,8,True,227,[3L, 0L, 1L, 0L, 4L, 0L, 5L, 0L, 2L, 2L, 0L, 1L, 4L, 5L, 4L, 5L, 3L, 0L, 3L, 3L, 1L, 4L, 3L, 4L, 5L, 2L, 2L, 4L, 2L, 5L]),
    Data(175,"jdmadness@hotmail.com",1240432477,31,29,13,13,6,3,True,208,[0L, 2L, 0L, 4L, 0L, 3L, 0L, 3L, 4L, 3L, 0L, 2L, 4L, 2L, 5L, 0L, 5L, 2L, 1L, 1L, 5L, 2L, 2L, 3L, 1L, 3L, 4L, 1L, 2L, 3L]),
    Data(176,"jdmadness@hotmail.com",1240433516,30,29,12,11,0,0,True,200,[0L, 0L, 3L, 2L, 5L, 4L, 5L, 0L, 1L, 0L, 5L, 4L, 2L, 0L, 3L, 3L, 2L, 0L, 2L, 0L, 4L, 0L, 2L, 3L, 0L, 5L, 1L, 4L, 5L, 1L]),
    Data(177,"jsanislo@sbcglobal.net",1240436002,2,0,2,0,0,0,False,0,[0L, 2L, 4L, 3L, 5L, 0L, 4L, 3L, 2L, 4L, 3L, 3L, 0L, 1L, 2L, 0L, 1L, 1L, 4L, 5L, 5L, 1L, 2L, 1L, 1L, 3L, 2L, 0L, 4L, 2L]),
    Data(178,"JMLazarz",1240438925,32,29,13,10,17,9,True,227,[2L, 2L, 3L, 0L, 5L, 4L, 4L, 2L, 0L, 0L, 4L, 1L, 1L, 0L, 2L, 2L, 2L, 1L, 0L, 0L, 5L, 0L, 1L, 0L, 3L, 2L, 5L, 0L, 5L, 4L]),
    Data(179,"stablegirl_luvshorses@yahoo.com",1240439013,30,29,13,13,3,3,True,205,[1L, 1L, 3L, 1L, 1L, 3L, 0L, 1L, 3L, 4L, 5L, 5L, 0L, 0L, 5L, 5L, 2L, 2L, 2L, 3L, 4L, 0L, 0L, 3L, 0L, 1L, 4L, 3L, 0L, 2L]),
    Data(180,"misunrj@uwec.edu",1240442108,33,25,13,10,20,15,True,125,[2L, 5L, 1L, 2L, 0L, 5L, 2L, 0L, 4L, 1L, 0L, 3L, 3L, 3L, 1L, 2L, 4L, 1L, 0L, 5L, 5L, 5L, 1L, 0L, 5L, 5L, 3L, 2L, 3L, 1L]),
    Data(181,"misunrj@uwec.edu",1240442509,31,29,13,8,18,15,True,210,[1L, 0L, 1L, 3L, 2L, 5L, 1L, 0L, 4L, 4L, 3L, 2L, 3L, 0L, 3L, 3L, 3L, 3L, 3L, 3L, 4L, 0L, 3L, 5L, 2L, 5L, 2L, 1L, 5L, 3L]),
    Data(182,"Rhittika.R95",1240442622,32,29,13,10,15,11,True,211,[4L, 5L, 0L, 4L, 1L, 2L, 2L, 3L, 3L, 4L, 0L, 1L, 2L, 5L, 4L, 3L, 0L, 2L, 3L, 3L, 3L, 3L, 5L, 1L, 2L, 1L, 4L, 5L, 4L, 5L]),
    Data(183,"Izzy.Clarizio",1240442732,34,29,13,10,14,13,True,211,[4L, 1L, 5L, 4L, 5L, 2L, 2L, 2L, 1L, 2L, 2L, 4L, 5L, 5L, 0L, 5L, 2L, 5L, 4L, 5L, 1L, 0L, 5L, 4L, 2L, 2L, 5L, 2L, 5L, 4L]),
    Data(184,"samantha102194",1240444017,1,0,1,1,0,0,False,0,[2L, 4L, 3L, 2L, 1L, 4L, 1L, 0L, 2L, 1L, 4L, 2L, 1L, 4L, 5L, 5L, 0L, 3L, 3L, 0L, 1L, 4L, 3L, 3L, 3L, 0L, 5L, 1L, 4L, 5L]),
    Data(185,"m063834",1240445035,31,29,13,13,10,6,True,213,[2L, 4L, 4L, 1L, 5L, 3L, 3L, 2L, 0L, 0L, 2L, 2L, 4L, 0L, 4L, 4L, 1L, 2L, 3L, 5L, 5L, 3L, 1L, 0L, 4L, 0L, 4L, 2L, 5L, 0L]),
    Data(186,"ajkaus",1240447681,30,29,13,11,16,2,True,231,[4L, 4L, 0L, 2L, 1L, 4L, 0L, 1L, 4L, 3L, 3L, 3L, 0L, 4L, 0L, 1L, 2L, 3L, 1L, 5L, 1L, 3L, 1L, 3L, 2L, 5L, 3L, 0L, 5L, 3L]),
    Data(187,"ajkaus",1240447950,32,29,13,11,18,7,True,242,[2L, 4L, 3L, 1L, 0L, 3L, 2L, 2L, 3L, 5L, 1L, 3L, 2L, 4L, 5L, 3L, 2L, 3L, 2L, 4L, 1L, 4L, 4L, 2L, 2L, 4L, 4L, 1L, 3L, 2L]),
    Data(188,"ashhassan53",1240448256,31,29,13,11,18,17,True,212,[3L, 1L, 0L, 2L, 1L, 1L, 4L, 1L, 5L, 1L, 1L, 1L, 0L, 3L, 1L, 1L, 1L, 5L, 1L, 4L, 3L, 1L, 5L, 0L, 0L, 1L, 4L, 3L, 1L, 0L]),
    Data(189,"katieromportl",1240448397,30,29,13,13,6,5,True,206,[3L, 3L, 4L, 5L, 0L, 0L, 2L, 4L, 4L, 4L, 5L, 0L, 3L, 4L, 4L, 5L, 1L, 5L, 5L, 5L, 4L, 5L, 3L, 0L, 2L, 0L, 0L, 0L, 4L, 2L]),
    Data(190,"ryanrabemshs",1240448836,30,29,13,12,16,8,True,225,[2L, 3L, 5L, 3L, 2L, 4L, 0L, 1L, 1L, 3L, 4L, 0L, 3L, 1L, 2L, 2L, 4L, 1L, 1L, 5L, 5L, 5L, 2L, 3L, 1L, 3L, 4L, 4L, 4L, 5L]),
    Data(191,"aidana.saudabayeva",1240449031,31,29,13,10,17,9,True,218,[2L, 0L, 5L, 5L, 1L, 2L, 3L, 0L, 4L, 4L, 0L, 1L, 1L, 0L, 4L, 4L, 1L, 5L, 4L, 3L, 1L, 1L, 4L, 3L, 2L, 0L, 5L, 0L, 1L, 0L]),
    Data(192,"aidana.saudabayeva",1240449348,5,4,5,4,0,0,False,0,[5L, 3L, 3L, 5L, 5L, 5L, 1L, 3L, 2L, 5L, 3L, 5L, 1L, 5L, 0L, 2L, 3L, 4L, 3L, 5L, 3L, 0L, 2L, 3L, 2L, 4L, 5L, 0L, 4L, 1L]),
    Data(193,"AuntieK",1240451611,31,29,13,11,18,16,True,212,[1L, 0L, 3L, 0L, 0L, 0L, 4L, 3L, 4L, 4L, 1L, 1L, 2L, 3L, 5L, 3L, 5L, 0L, 0L, 1L, 1L, 4L, 0L, 1L, 1L, 5L, 0L, 4L, 1L, 2L]),
    Data(194,"zhengl84",1240452715,33,29,13,6,20,20,True,197,[4L, 5L, 0L, 0L, 5L, 0L, 3L, 4L, 2L, 1L, 2L, 1L, 3L, 3L, 1L, 4L, 1L, 3L, 5L, 5L, 4L, 3L, 1L, 2L, 1L, 1L, 3L, 0L, 0L, 3L]),
    Data(195,"AuntieK",1240452787,30,29,13,13,3,3,True,203,[4L, 0L, 1L, 4L, 3L, 4L, 1L, 5L, 1L, 3L, 1L, 0L, 3L, 1L, 1L, 3L, 3L, 1L, 2L, 3L, 1L, 5L, 5L, 1L, 4L, 2L, 0L, 2L, 1L, 1L]),
    Data(196,"zhengl84",1240452995,15,12,13,9,2,2,False,0,[0L, 2L, 2L, 3L, 3L, 3L, 3L, 2L, 3L, 3L, 4L, 1L, 2L, 3L, 1L, 0L, 4L, 0L, 5L, 3L, 4L, 1L, 2L, 4L, 1L, 2L, 0L, 3L, 0L, 1L]),
    Data(197,"amelbo2@yahoo.com",1240453560,31,29,13,12,10,6,True,217,[4L, 3L, 4L, 0L, 1L, 3L, 3L, 4L, 0L, 0L, 4L, 2L, 4L, 1L, 2L, 5L, 1L, 4L, 1L, 3L, 0L, 1L, 5L, 3L, 5L, 5L, 1L, 2L, 1L, 0L]),
    Data(198,"teoh.od",1240453794,33,29,13,9,17,13,True,213,[4L, 0L, 4L, 1L, 4L, 5L, 1L, 3L, 5L, 5L, 1L, 1L, 1L, 3L, 3L, 4L, 2L, 5L, 2L, 3L, 2L, 5L, 3L, 2L, 3L, 5L, 4L, 2L, 2L, 1L]),
    Data(199,"Colin.Dill",1240454691,31,29,13,13,7,7,True,203,[1L, 4L, 2L, 0L, 1L, 0L, 4L, 2L, 1L, 0L, 3L, 3L, 5L, 2L, 4L, 1L, 3L, 5L, 0L, 4L, 1L, 4L, 2L, 3L, 4L, 1L, 1L, 0L, 5L, 0L]),
    Data(200,"Mister.Ed.Mann@googlemail.com",1240487382,3,2,3,2,0,0,False,0,[2L, 0L, 4L, 0L, 2L, 4L, 1L, 2L, 0L, 0L, 4L, 4L, 5L, 1L, 3L, 2L, 4L, 0L, 2L, 5L, 1L, 0L, 5L, 0L, 2L, 3L, 3L, 3L, 0L, 4L]),
    Data(201,"donald.lazarz",1240505416,30,29,13,13,14,6,True,224,[5L, 1L, 5L, 0L, 3L, 1L, 3L, 5L, 5L, 5L, 1L, 4L, 5L, 5L, 2L, 4L, 0L, 4L, 0L, 0L, 4L, 0L, 5L, 2L, 4L, 3L, 5L, 3L, 0L, 4L]),
    Data(202,"karla.saur",1240509513,30,29,13,12,6,6,True,204,[0L, 3L, 4L, 2L, 3L, 4L, 1L, 2L, 2L, 1L, 4L, 1L, 2L, 5L, 0L, 2L, 1L, 0L, 4L, 0L, 2L, 2L, 3L, 2L, 3L, 3L, 5L, 0L, 1L, 1L]),
    Data(203,"glen.gibb",1240514236,36,29,13,12,14,5,True,225,[3L, 5L, 5L, 0L, 0L, 1L, 0L, 5L, 3L, 0L, 3L, 2L, 0L, 1L, 4L, 5L, 5L, 2L, 0L, 4L, 0L, 1L, 3L, 3L, 4L, 5L, 2L, 2L, 2L, 2L]),
    Data(204,"glen.gibb",1240514586,36,29,13,12,21,6,True,243,[0L, 3L, 2L, 5L, 0L, 0L, 3L, 4L, 2L, 2L, 4L, 5L, 4L, 2L, 1L, 2L, 1L, 3L, 3L, 2L, 4L, 2L, 3L, 5L, 1L, 0L, 5L, 1L, 5L, 5L]),
    Data(205,"nicnak",1240515241,30,29,13,12,10,6,True,220,[3L, 5L, 4L, 5L, 5L, 3L, 3L, 1L, 0L, 3L, 2L, 0L, 1L, 2L, 3L, 4L, 3L, 0L, 1L, 5L, 2L, 0L, 0L, 2L, 0L, 4L, 0L, 5L, 3L, 0L]),
    Data(206,"nicnak",1240516038,31,29,13,12,17,13,True,215,[0L, 5L, 1L, 1L, 1L, 5L, 2L, 2L, 3L, 2L, 2L, 0L, 4L, 5L, 2L, 0L, 1L, 3L, 3L, 3L, 2L, 0L, 0L, 2L, 5L, 5L, 2L, 2L, 0L, 5L]),
    Data(207,"nicnak",1240517496,31,29,13,13,16,13,True,217,[4L, 1L, 4L, 1L, 0L, 5L, 0L, 0L, 5L, 5L, 1L, 4L, 2L, 5L, 5L, 2L, 0L, 1L, 2L, 1L, 5L, 2L, 3L, 3L, 1L, 0L, 0L, 3L, 2L, 3L]),
    Data(208,"nicnak",1240519731,30,29,13,13,1,1,True,204,[2L, 0L, 3L, 3L, 1L, 0L, 1L, 1L, 2L, 5L, 5L, 0L, 3L, 2L, 4L, 1L, 4L, 4L, 2L, 4L, 3L, 5L, 3L, 0L, 2L, 4L, 4L, 3L, 2L, 1L]),
    Data(209,"nicnak",1240519916,35,29,13,12,22,7,True,242,[1L, 5L, 2L, 4L, 2L, 2L, 4L, 1L, 0L, 3L, 0L, 1L, 1L, 2L, 5L, 5L, 1L, 2L, 0L, 0L, 4L, 5L, 2L, 3L, 5L, 2L, 5L, 2L, 3L, 1L]),
    Data(210,"stablegirl_luvshorses@yahoo.com",1240525737,30,29,13,13,4,4,True,202,[1L, 3L, 2L, 5L, 0L, 4L, 1L, 0L, 5L, 3L, 4L, 5L, 2L, 0L, 3L, 3L, 3L, 0L, 2L, 0L, 0L, 2L, 1L, 4L, 4L, 4L, 5L, 1L, 2L, 3L]),
    Data(211,"hardware.hank",1240525931,34,29,13,11,15,12,True,218,[1L, 3L, 4L, 4L, 1L, 0L, 3L, 5L, 5L, 0L, 1L, 3L, 3L, 2L, 3L, 4L, 1L, 5L, 4L, 3L, 0L, 2L, 4L, 1L, 5L, 4L, 2L, 4L, 4L, 3L]),
    Data(212,"wick98",1240528708,31,29,13,12,12,12,True,207,[2L, 4L, 0L, 1L, 3L, 1L, 1L, 3L, 5L, 1L, 1L, 1L, 2L, 1L, 4L, 3L, 0L, 1L, 4L, 5L, 0L, 3L, 0L, 1L, 2L, 5L, 5L, 1L, 4L, 3L]),
    Data(213,"jobros3",1240529593,21,13,13,9,8,1,True,65,[0L, 3L, 5L, 1L, 4L, 1L, 2L, 1L, 5L, 0L, 5L, 0L, 5L, 4L, 1L, 1L, 1L, 1L, 0L, 5L, 2L, 2L, 1L, 4L, 3L, 5L, 1L, 2L, 5L, 4L]),
    Data(214,"watermelon58",1240532413,30,29,13,11,13,8,True,212,[5L, 4L, 2L, 5L, 4L, 5L, 4L, 5L, 1L, 5L, 1L, 0L, 1L, 5L, 4L, 0L, 4L, 1L, 0L, 2L, 4L, 2L, 4L, 0L, 4L, 0L, 2L, 3L, 4L, 2L]),
    Data(215,"zypher",1240532698,30,29,13,11,14,4,True,233,[3L, 2L, 1L, 1L, 1L, 0L, 1L, 0L, 1L, 1L, 2L, 4L, 3L, 0L, 3L, 0L, 1L, 0L, 4L, 1L, 1L, 2L, 1L, 5L, 2L, 0L, 5L, 4L, 5L, 1L]),
    Data(216,"donald.lazarz",1240585429,30,29,13,12,0,0,True,199,[3L, 4L, 3L, 0L, 5L, 3L, 4L, 3L, 0L, 1L, 2L, 5L, 2L, 3L, 0L, 3L, 4L, 1L, 5L, 4L, 3L, 3L, 1L, 0L, 0L, 1L, 0L, 0L, 1L, 2L]),
    Data(217,"ukuter",1240597011,30,29,13,12,6,6,True,202,[2L, 1L, 5L, 1L, 2L, 0L, 1L, 2L, 2L, 5L, 4L, 5L, 1L, 3L, 1L, 3L, 2L, 2L, 3L, 4L, 1L, 4L, 0L, 3L, 3L, 5L, 5L, 2L, 1L, 2L]),
    Data(218,"ukuter",1240597420,30,29,13,12,6,5,True,206,[2L, 0L, 1L, 3L, 4L, 5L, 5L, 0L, 4L, 1L, 3L, 2L, 4L, 1L, 5L, 2L, 4L, 2L, 1L, 2L, 5L, 0L, 4L, 4L, 3L, 3L, 1L, 1L, 3L, 1L]),
    Data(219,"m063834",1240629994,30,29,13,13,3,3,True,199,[4L, 2L, 5L, 3L, 5L, 4L, 3L, 0L, 4L, 0L, 4L, 5L, 4L, 4L, 3L, 3L, 4L, 3L, 0L, 2L, 3L, 4L, 4L, 2L, 1L, 1L, 3L, 5L, 1L, 2L])
]


# data without duplicates
tmp_played = {}
def is_new_player(d):
    if tmp_played.has_key(d.player):
        return False
    else:
        tmp_played[d.player] = True
        return True
data_first_only = filter(is_new_player, data_all)


# data without duplicates and only for finished games
data_first_and_fin = filter(lambda d : d.game_over, data_first_only)


# data where first round is rational at least some percentage of the time AND
# there have been at least some number of decisions made in the second round
def get_rational_data(d, min_rational_per, min_r2_choices):
    return filter(lambda d : d.rationality(1)>=min_rational_per and d.num_choices[2]>=min_r2_choices,
                  data_first_only)
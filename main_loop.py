#from PiCamController import getBoard
from ideal_cam import getBoard
from square_grid_validator import validate_board

empty_status = {"1":False,"2":False,"3":False,"4":False,"5":False,"6":False,"7":False,"8":False,"9":False}

class Archer:
    _range = 2
    _damage = 2
    def __init__(self, node):
        self.health = 10
        self.node = node

    def __str__(self):
        return 'Archer at ['+self.node+'] with health '+str(self.health)

class Pikeman:
    _range = 1
    _damage = 1
    def __init__(self, node):
        self.health = 6
        self.node = node
    def __str__(self):
        return 'Pikeman at ['+self.node+'] with health '+str(self.health)

class Player:
    def __init__(self):
        self.pieces = []

player1 = Player()
player2 = Player()

def get_until_only_added(status_map):
    (g, new_status_map) = getBoard(None, status_map)
    for k, v in new_status_map.iteritems():
        if v and not status_map[k]:
            print "Don't move the pieces yet!"
            get_until_only_added(status_map)

    return new_status_map

def do_it(): 
    g = None
    occupied_status = empty_status
    (g, occupied_status) = getBoard(g, occupied_status)
    while True:
        if validate_board(g):
            break
        else:
            (g2, occupied_status2) = getBoard(g, occupied_status)
    print "Got a valid board. Player 1, place your archers now!"
    (g1, new_occupied_status) = getBoard(g, occupied_status)
    for k, v in new_occupied_status.iteritems():
        if v:
            print "Adding player 1 archer at "+k
            player1.pieces.append(Archer(k))
    occupied_status_after_p1_archers = new_occupied_status
    print "Yay archers!. Player 2, place your archers please"
    new_occupied_status = get_until_only_added(occupied_status_after_p1_archers)
    for k, v in new_occupied_status.iteritems():
        if v and not occupied_status_after_p1_archers[k]:
            print "Adding player 2 archer at "+k
            player2.pieces.append(Archer(k))
    occupied_status_after_p2_archers = new_occupied_status
    print "Yay more archers!. Player 1, place your pikemen!"
    new_new_occupied_status = get_until_only_added(occupied_status_after_p2_archers)
    for k, v in new_new_occupied_status.iteritems():
        if v and not occupied_status_after_p2_archers[k]:
            player1.pieces.append(Pikeman(k))
    occupied_status_after_p1_pikes = new_new_occupied_status
    print "Yay pikemen!. Player 2, place your pokemon!"
    new_new_new_occupied_status = get_until_only_added(occupied_status_after_p1_pikes)
    for k, v in new_new_new_occupied_status.iteritems():
        if v and not occupied_status_after_p1_pikes[k]:
            player2.pieces.append(Pikeman[k])



    


do_it()

for p in player1.pieces:
    print p
for p in player2.pieces:
    print p

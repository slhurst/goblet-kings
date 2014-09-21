from PiCamController import getGraph
#from ideal_cam import getBoard
from square_grid_validator import validate_board

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
    def __init__(self, name):
        self.pieces = []
        self.name = name
    def __str__(self):
        return self.name

player1 = Player("Player 1")
player2 = Player("Player 2")

def get_until_only_added(status_map):
    (g, new_status_map) = getGraph()

    newBlobs = []
    
    for k, v in status_map.iteritems():
        if v: #if true then old map had a piece here
            if not new_status_map[k]:  #if true the ne wmap doesn't error
                print "Don't move the pieces yet!"
                get_until_only_added(status_map)
        elif new_status_map[k]: #didnt used to be a piece here, check if there is now            
                newBlobs.append(k)
            
           

    return (new_status_map, newBlobs)

def do_it(): 
    (g, occupied_status) = getGraph() 
    while True:
        if validate_board(g):
            break
        else:
            (g, occupied_status) = getGraph()
    print "Got a valid board. Player 1, place your archers now! Enter to continue"
    raw_input()
    (g1, new_occupied_status) = getGraph()
    for k, v in new_occupied_status.iteritems():
        if v:
            print ("Adding player 1 archer at ", k)
            player1.pieces.append(Archer(k))
    occupied_status_after_p1_archers = new_occupied_status
    print "Yay archers!. Player 2, place your archers please! Enter to continue"
    raw_input()
    (new_occupied_status, new_blobs) = get_until_only_added(occupied_status_after_p1_archers)    
    for blob in new_blobs:
        print ("Adding player 2 archer at ", blob)
        player2.pieces.append(Archer(blob))
    occupied_status_after_p2_archers = new_occupied_status

    return occupied_status_after_p2_archers
##    print "Yay more archers!. Player 1, place your pikemen! Enter to continue"
##    raw_input()
##    new_new_occupied_status = get_until_only_added(occupied_status_after_p2_archers)
##    for k, v in new_new_occupied_status.iteritems():
##        if v and not occupied_status_after_p2_archers[k]:
##            player1.pieces.append(Pikeman(k))
##    occupied_status_after_p1_pikes = new_new_occupied_status
##    print "Yay pikemen!. Player 2, place your pokemon! Enter to continue"
##    raw_input()
##    new_new_new_occupied_status = get_until_only_added(occupied_status_after_p1_pikes)
##    for k, v in new_new_new_occupied_status.iteritems():
##        if v and not occupied_status_after_p1_pikes[k]:
##            player2.pieces.append(Pikeman[k])


def getMove(oldStatus, newStatus):

    old_location = None
    new_location = None
    
    for  old_key, old_value in oldStatus.iteritems():
        new_value = newStatus[old_key]
        if old_value and not new_value:
            if old_location is None:
                old_location = old_key
            else:
                print("Found more than one movemvent, reset board to only one move")
                return
        if not old_value and new_value:
            if new_location is None:
                new_location = old_key
            else:
                print("Found more than one movemvent, reset board to only one move")
                return
                
            
    if old_location is not None and new_location is not None:
        return (old_location, new_location)
    else:
        return None
    
    


current_status = do_it()
current_player = player1




while(True):
    for p in player1.pieces:
        print player1, p
    for p in player2.pieces:
        print player2, p
    print "next turn for",current_player
    raw_input()
    (g, new_status) = getGraph()

    move_return = getMove(current_status, new_status)
    print("-------------------")
    for space in current_status:                
                print(space, current_status[space])
    print("*******************")                
    for space in new_status:                
                print(space, new_status[space])
    print("-------------------")                
    
    if move_return is not None:
        print "in move return"
        (old_location, new_location) = move_return
        for p in current_player.pieces:
            if p.node == old_location:
                print "piece ", p, " moved from ", old_location, " to ", new_location
                p.node = new_location

        current_status = new_status
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
    else:
        print "You didn't move anything, try again"
        raw_input()

    

    

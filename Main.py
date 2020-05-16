######################################################################################################################
# Name: Zach Hoover, Bryce Cook, Tyler Porrier
# Date: 5-13-20
# Description: Connect-4 Dungeon Crawler
##################################################################################################################
from GUI import *
from CONNECT import *
import pygame
        
    


#####################################################################################        
#Main Code

#Make the map.
m = Map(8)


win = False
turn = "player"
WIDTH = 800
HEIGHT = 600
gui = GUI(WIDTH, HEIGHT, turn)
gui.initialize()
running = True
dev = False
##Main loop of the game
complete = False
while True:
    x, y = gui.roomSelect(m)
    print "({},{})".format(x,y)
    if m.grid(x, y) and m.grid(x, y).unlocked and not m.grid(x, y).win:
        gui.initialize()
        sleep(.25)
        gui.board()
        if dev or gui.game(m.grid(x,y)):
            if x == (m.length - 1):
                m.unlock(x, y)
                complete = True
                break
            m.unlock(x, y)
        else:
            break
print "You won {} games.".format(m.wins)
if complete:
    print "Congratulations, you made it to the end of the map!"
        

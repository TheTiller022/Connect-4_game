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


win = False
turn = "player"
WIDTH = 800
HEIGHT = 600
gui = GUI(WIDTH, HEIGHT, turn)
gui.initialize()
running = True
dev = False
complete = False
##Main loop of the game
#Mode selection
mode = gui.modeSelect()
if mode == "Easy":
    m = Map(5, 0, 1, 5)
elif mode == "Medium":
    m = Map()
elif mode == "Hard":
    m = Map(12, 2, 3, 1)

while True:
    x, y = gui.roomSelect(m)
    if m.grid(x, y) and m.grid(x, y).unlocked and not m.grid(x, y).win:
        gui.initialize()
        gui.playerLives(m)
        sleep(.25)
        gui.enemy(m, x)
        sleep(2)
        if dev or gui.game(m.grid(x,y)):
            if x == (m.length - 1):
                m.unlock(x, y)
                complete = True
                break
            m.unlock(x, y)
            gui.phrase("Stage Complete!")
            sleep(2)
        else:
            m.grid(x,y).game.setup()
            m.lives -= 1
            sleep(2)
            if m.lives == 0:
                break
gui.phrase("You won {} games.".format(m.wins))
if complete:
    gui.phrase("Congratulations, you've made it to the end of the map!", + 30)
        

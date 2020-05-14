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
m = Map(8, 0)

#set the players x and y coords to 0,0
playerx, playery = 0, 0


win = False
turn = "player"
WIDTH = 800
HEIGHT = 600
gui = GUI(WIDTH, HEIGHT, turn)
gui.initialize()
running = True

for i in range(0,8):
    gui.initialize()
    gui.game(m.grid(i,0))



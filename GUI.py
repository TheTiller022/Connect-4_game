import pygame
from math import *
from time import *
from collections import defaultdict


class GUI(object):
    def __init__(self, WIDTH, HEIGHT, turn, window = None, x = None, y = None, taken = None, list = None):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.turn = turn
        self.window = window
        self.x = x
        self.y = y
        self.taken = {}
        
        

    def initialize(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Connect Game")
        icon = pygame.image.load("logo.png")
        pygame.display.set_icon(icon)
        del self.taken
        self.taken = {}
        self.turn = "player"

    def board(self):
        BoardImg = pygame.image.load("Board.png")
        BoardX = self.WIDTH/5
        BoardY = self.HEIGHT/8
        self.window.blit(BoardImg, (BoardX, BoardY))

    def row(self):
        dy = 70
        self.y = self.HEIGHT/8+6+5*dy
        pos = 0
        try:
            Y = self.taken[self.x]
            if Y == (self.HEIGHT / 8 + 6):
                return False
            if self.y>= Y:
                Y = self.taken[self.x]
                pos+= 1
                self.y = self.HEIGHT / 8 + 6 + 5*dy - pos*dy
                if self.y>= Y:
                    Y = self.taken[self.x]
                    pos+= 1
                    self.y = self.HEIGHT / 8 + 6 + 5*dy - pos*dy
                    if self.y>= Y:
                        Y = self.taken[self.x]
                        pos+=1
                        self.y= self.HEIGHT / 8 + 6 + 5*dy - pos*dy
                        if self.y>= Y:
                            Y = self.taken[self.x]
                            pos+=1
                            self.y= self.HEIGHT / 8 + 6 + 5*dy - pos*dy
                            if self.y>= Y:
                                Y = self.taken[self.x]
                                pos+=1
                                self.y= self.HEIGHT / 8 + 6 + 5*dy - pos*dy
        except:
            self.y = self.HEIGHT / 8 + 6 + 5*dy
            
    def check(self, pos, Y, dy):
        while self.y >= Y:
            pos+= 1
            self.y = self.HEIGHT / 8 + 6 + 5*dy - pos*dy
            print "up one"
            self.check(pos, Y, dy)
        return self.y, pos

    def column(self, pos):
        dx = 70
        X = self.WIDTH / 5 + 4
        if pos < (X + dx):
            pos = 0
        elif (pos > X + dx and pos < X + 2*dx): 
            pos = 1
        elif (pos > X + 2*dx and pos < X + 3*dx):
            pos = 2
        elif (pos > X + 3*dx and pos < X + 4*dx):
            pos = 3
        elif (pos > X + 4*dx and pos < X + 5*dx):
            pos = 4
        elif (pos > X + 5*dx and pos < X + 6*dx):
            pos = 5
        else:
            pos = 6
        self.x = X + pos*dx
        return self.x, pos

    def addPiece(self):
        redpiece = pygame.image.load("redpiece.png")
        yellowpiece = pygame.image.load("yellowpiece.png")
        self.row()
        if self.turn == "player":
            self.window.blit(redpiece, (self.x, self.y))
            self.taken[self.x] = self.y
            self.turn = "ai"
        elif self.turn == "ai":
            self.window.blit(yellowpiece, (self.x, self.y))
            self.taken[self.x] = self.y
            self.turn = "player"
        elif self.row == False:
            pass

    def win(self):
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("You Win!!!", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (self.WIDTH // 2, self.HEIGHT //2)
        self.window.blit(text, textRect)
        
        

    # where game being run
    def game(self, r):
        while True:
            #print self.taken[0]
            self.board()
            pygame.display.update()
            pressed1, pressed2, presssed3 = pygame.mouse.get_pressed()
            x,y = pygame.mouse.get_pos()
            x, pos = self.column(x)
            if pressed1:
                if r.game.play("P", pos):
                    print r.game
                    self.addPiece()
                    self.board()
                    pygame.display.update()
                    if r.game.winCheck():
                        return True
                    sleep(0.25)
                    aix = r.AI.move()
                    print r.game
                    X = self.WIDTH / 5 + 4
                    self.x = X + (aix)*70
                    self.addPiece()
                    self.board()
                    pygame.display.update()
                    if r.game.winCheck():
                        return False
                    
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # update screen here
            
            

##win = False
##turn = "player"
######ai = k.AI()
######GAME = k.ConnectGame()
##WIDTH = 800
##HEIGHT = 600
##start = GUI(WIDTH, HEIGHT, turn)
##start.initialize()
##start.game()


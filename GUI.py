import pygame
from math import *
from time import *
from collections import defaultdict
from random import randint


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
        self.fontLarge = pygame.font.Font("freesansbold.ttf", 30)
        self.fontSmall = pygame.font.Font("freesansbold.ttf", 12)
        self.fontMedium = pygame.font.Font("freesansbold.ttf", 24)
        
    def modeSelect(self):
        self.initialize()
        #Easy
        i = pygame.Rect(151, 151, 500, 75)
        pygame.draw.rect(self.window, (127, 127, 127), i)
        text = self.fontLarge.render("Easy", True, (0, 125, 0))
        textRect = text.get_rect()
        textRect.center = (self.WIDTH // 2, 186)
        self.window.blit(text, textRect)
        
        #Medium
        i = pygame.Rect(151, 251, 500, 75)
        pygame.draw.rect(self.window, (127, 127, 127), i)
        text = self.fontLarge.render("Medium", True, (0, 0, 125))
        textRect = text.get_rect()
        textRect.center = (self.WIDTH // 2, 186 + 100)
        self.window.blit(text, textRect)
        
        #Hard
        i = pygame.Rect(151, 351, 500, 75)
        pygame.draw.rect(self.window, (127, 127, 127), i)
        text = self.fontLarge.render("Hard", True, (125, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.WIDTH // 2, 186 + 200)
        self.window.blit(text, textRect)
        
        pygame.display.update()
        while True:
            pressed1, pressed2, presssed3 = pygame.mouse.get_pressed()
            x,y = pygame.mouse.get_pos()
            if pressed1:
                if x >= 151 and x <= 651:
                    if y >= 151 and y <= 226:
                        return "Easy"
                    elif y >= 251 and y <= 326:
                        return "Medium"
                    elif y >= 351 and y <= 426:
                        return "Hard"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            
    def enemy(self, m, x):
        #gray border for the enemy
        i = pygame.Rect(self.WIDTH - 270, 0, 270, 270)
        pygame.draw.rect(self.window, (127,127,127), i)
        #black background for the enemy
        i = pygame.Rect(self.WIDTH - 260, 10, 250, 250)
        pygame.draw.rect(self.window, (0,0,0), i)
        pygame.display.update()
        #choose a random enemy or if it is the final boss, choose boss
        png = pygame.image.load("enemy/{}.png".format(randint(0,9)))
        if x == m.length - 1:
            png = pygame.image.load("enemy/boss.png")
        self.window.blit(png, (self.WIDTH - 260, 10))
        pygame.display.update()
        
    def playerLives(self, m):
        text = self.fontMedium.render("Lives:  {}".format(m.lives), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (75, 24)
        self.window.blit(text, textRect)
        pygame.display.update()
    
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

    def phrase(self, pstring, offset = 0):
        text = self.fontLarge.render(pstring, True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (self.WIDTH // 2, (self.HEIGHT //2) + offset)
        self.window.blit(text, textRect)
        pygame.display.update()
        
        
    def roomGrid(self, m):
        self.initialize()
        self.playerLives(m)
        color = (127, 127, 127)
        #The gap between rooms
        gap = 10
        #The number of rooms in the x and y direction
        rlength = m.length
        rheight = m.height
        #gray background for the map
        i = pygame.Rect(76, 76, 650, 400)
        pygame.draw.rect(self.window, color, i)
        #Title
        text = self.fontLarge.render("Connect-4 Dungeon Crawler", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (self.WIDTH // 2, 100)
        self.window.blit(text, textRect)
        # make sure length and width are functions of how many rooms
        # also make sure that placement is a function
        # arbittary stuff
        width = ((self.WIDTH - 150)/len(m.rooms)) - gap
        height = ((self.HEIGHT - 250) / m.height) - gap
        y = 126 + gap / 2
        for s in range(0, rheight):
            x = 76 + gap / 2
            for d in range(0, rlength):
                #print "{},{}".format(x,y)
                #picks color based on room's status
                color = self.roomColor(m, d, s)
                #draws room
                i = pygame.Rect(x,y,width,height)
                pygame.draw.rect(self.window, color, i)
                #displays room's status over the room
                self.roomText(m, d, s, (x + (width / 2)), y, height)
                x += gap + width
            y += gap + height
        pygame.display.update()

    def roomSelect(self, m):
        self.roomGrid(m)
        pygame.display.update()
        xi = 76
        yi = 126
        gap = 10
        dx = ((self.WIDTH - 150)/len(m.rooms)) - gap
        dy = ((self.HEIGHT - 250) / m.height) - gap
        while True:
            pressed1, pressed2, presssed3 = pygame.mouse.get_pressed()
            x,y = pygame.mouse.get_pos()
            if pressed1:
                sleep(.25)
                for i in range(0, m.length):
                    if x >= xi and x <= (xi + dx):
                        for j in range(0, m.height):
                            if y >= yi and y <= (yi + dy):
                                j -= m.divergence
                                return i, j
                            yi += (dy + gap)
                    xi += (dx + gap)
                xi = 76
                yi = 126

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
        

    def roomText(self, m, d, s, x, y, height):
        s -= m.divergence
        #checks to make sure the room is vaild and unlocked
        if m.grid(d,s) and m.grid(d,s).unlocked:
            #Shows the difficulty of the room
            text = self.fontSmall.render("Difficulty", True, (255,255,255))
            textRect = text.get_rect()
            textRect.center = ((x), (y + 12))
            self.window.blit(text, textRect)
            text = self.fontSmall.render(str(m.grid(d,s).AI.diff), True, (255,255,255))
            textRect = text.get_rect()
            textRect.center = ((x), (y + 24))
            self.window.blit(text, textRect)
            #The status of the room
            if m.grid(d,s).win:
                status = "Defeated"
            else:
                status = "Unlocked"
            text = self.fontSmall.render(status, True, (255,255,255))
            textRect = text.get_rect()
            textRect.center = ((x), (y + height - 12))
            self.window.blit(text, textRect)
        
    def roomColor(self, m, x, y):
        y -= m.divergence
        #Default color is gray
        color = (127, 127, 127)
        #color = (0, 0, 0)
        if m.grid(x,y):
            #if the room is beaten, the color of it is red
            if m.grid(x,y).win:
                color = (125, 0, 0)
            #if the room is unlocked, the color is blue
            elif m.grid(x,y).unlocked:
                color = (0, 0, 125)
        return color
            
        
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
                    #print r.game
                    self.addPiece()
                    self.board()
                    pygame.display.update()
                    if r.game.winCheck():
                        return True
                    sleep(0.25)
                    aix = r.AI.move()
                    #print r.game
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


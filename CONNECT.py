######################################################################################################################
# Name: Zach Hoover, Bryce Cook, Tyler Porrier
# Date: 5-13-20
# Description: Connect-4 Dungeon Crawler
##################################################################################################################
from random import randint
from random import shuffle
from time import sleep


#####################################################################################        
#Dungeon map class
class Map(object):
    def __init__(self, length = 8, divergence = 1, diff = 1):
        #How many rooms will spawn between the beginning and the end, horizontally.
        self.length = length
        #How many rooms up or down the paths are alowed to diverge.
        self.divergence = divergence
        #Difficulty of the dungeon
        self.diff = diff
        self.rooms = {}
        self.playerx = 0
        self.playery = 0
        self.setup()
        self.wins = 0

    #length Setter/getter
    @property
    def length(self):
        return self._length
    @length.setter
    def length(self, value):
        self._length = value

    #divergence Setter/getter
    @property
    def divergence(self):
        return self._divergence
    @divergence.setter
    def divergence(self, value):
        self._divergence = value

    #Takes a grid coord and returns the room that is there, none if no room is there
    #or false if it's an invalid room
    def grid(self,x,y):
        response = False
        if x >= 0 and x < self.length:
            if y >= -self.divergence and y <= self.divergence:
                response = self.rooms[x][y]
        return response
        
    
    #Setups the dungeon
    def setup(self):
        for i in range(0, self.length):
            self.rooms[i] = {}
            for j in range((-self.divergence), (self.divergence + 1)):
                self.rooms[i][j] = None
        self.rooms[0][0] = Room(0, self.diff)
        self.roomWorm(0,0)
        self.rooms[0][0].unlocked = True

        #the height of the dungeon
        self.height = (2 * self.divergence) + 1
        

    #Randomly generates dungeon
    def roomWorm(self, x, y):
        
        exits = 0

        #Up
        if randint(1,100) < 15:
            if self.grid((x),(y+1)) == None:
                exits += 1
                self.rooms[x][y+1] = Room(x, self.diff)
                self.roomWorm(x, y+1)
        #Down
        if randint(1,100) < 15:
            if self.grid((x),(y-1)) == None:
                exits += 1
                self.rooms[x][y-1] = Room(x, self.diff)
                self.roomWorm(x, y-1)
        
        if randint(1, 100) < 15 or (exits == 0):
            if self.grid((x+1),y) == None:
                if ((x+1) == self.length -1):
                    self.rooms[x+1][y] = Room(x, self.diff)
                else:
                    self.rooms[x+1][y] = Room(x, self.diff)
                    self.roomWorm(x+1, y)
            
    #Runs after the player wins a room, unlocking adjacent rooms
    def unlock(self, x, y):
        self.wins += 1
        self.grid(x,y).win = True 
        neighborsx = [x, x, (x+1), (x-1)]
        neighborsy = [(y-1), (y+1), y, y]
        for i in range(0,4):
            if self.grid(neighborsx[i],neighborsy[i]):
                self.grid(neighborsx[i],neighborsy[i]).unlocked = True
        
        

    def __str__(self):
        draw = ""
        for j in range((-self.divergence), (self.divergence + 1)):
            for i in range(0, self.length):
                draw += str(self.rooms[i][j])
                draw += "\t"
            draw += "\n"
        return draw

#####################################################################################        
#Dungeon Room class
class Room(object):
    def __init__(self, x, diff):
        self.x = x
        self.game = ConnectGame()
        self.diff = diff
        self.AI = None
        self.unlocked = False
        self.win = False
        self.reward = None
        self.setup()

    def setup(self):
        self.AI = AI(self.game, ((self.diff * 25) + randint(0,10) + (self.x * 4)))
        
            
        
        
    
    def __str__(self):
        return " {} ".format(self.unlocked)

    

#####################################################################################        
#Connect-4 game class
class ConnectGame(object):
    
    def __init__(self, width = 7, height = 6, winLength = 4):
        self.width = width
        self.height = height
        self.winLength = winLength
        self.columns = {}
        self.setup()
        #The last move played using self.play
        self.prevMove = None


    #winLength Setter/getter
    @property
    def winLength(self):
        return self._winLength
    @winLength.setter
    def winLength(self, value):
        if (value > 1):
            self._winLength = value

    #height Setter/getter
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if (value >= 3):
            self._height = value

    #width Setter/getter
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if (value >= 3):
            self._width = value

    #Sets up a clean board
    def setup(self):
        for i in range(self.width):
            self.columns[i] = []
        self.win = False
        self.winner = None

    #Used to play a chip
    def play(self, player, column):
        if (len(self.columns[column]) < self.height):
            self.columns[column].append(player)
            self.prevMove = column
            return True
        else:
            return False
        

    #Checks to see if the top chip on a column causes 4 in a row.
    def winCheck(self):
        player = self.columns[self.prevMove][-1]
        return self.check(player, self.winLength, self.prevMove)

    
    #Takes grid coordinates and returns the player positioned there, or None if
    #no player is there or False if the spot is invalid.
    def grid(self, col, hei):
        response = False
        if (col < self.width and col >= 0 ):
            if (hei < self.height and hei >= 0):
                response = None
                if hei < len(self.columns[col]):
                    response = self.columns[col][hei]
        return response
                
    #Checks to see if there are a certain number of chips in a row, with one
    #of the chips being in the given coordinates
    def check(self, player, count, col, hei = -1):
        #Changes the default height to the height of the top chip of the column
        if hei == -1:
            hei = (len(self.columns[col]) - 1)
        #Check assumes the given coordinate is the same chip as the player
        #Top/Bot
        num = 1
        #Top
        if not hei == (self.height - 1):
            for i in range((hei + 1), self.height):
                if (self.grid(col, i) == player):
                    num += 1
                else:
                    break
        #Bot
        if not hei == (0):
            for i in range((hei - 1), -1, -1):
                if (self.grid(col, i) == player):
                    num += 1
                else:
                    break
        if num >= count:
            return True

        #Left/Right
        num = 1
        #Left
        if not col == 0:
            for i in range((col - 1), -1, -1):
                if (self.grid(i, hei) == player):
                    num += 1
                else:
                    break
        #Right
        if not col == (self.width - 1):
            for i in range((col + 1), self.width):
                if (self.grid(i, hei) == player):
                    num += 1
                else:
                    break
        if num >= count:
            return True

        #TopLeft/BotRight
        num = 1
        #TopLeft
        if col != 0 and hei != (self.height - 1):
            y = hei
            for i in range((col - 1), -1, -1):
                y += 1
                if (self.grid(i, y) == player):
                    num += 1
                else:
                    break
        #BotRight
        if col != (self.width - 1) and hei != 0:
            y = hei
            for i in range((col + 1), self.width):
                y += -1
                if (self.grid(i, y) == player):
                    num += 1
                else:
                    break
        if num >= count:
            return True

        #BotLeft/TopRight
        num = 1
        #BotLeft
        if col != 0 and hei != 0:
            y = hei
            for i in range((col - 1), -1, -1):
                y += -1
                if (self.grid(i, y) == player):
                    num += 1
                else:
                    break
        #TopRight
        if col != (self.width - 1) and hei != (self.height - 1):
            y = hei
            for i in range((col + 1), self.width):
                y += 1
                if (self.grid(i, y) == player):
                    num += 1
                else:
                    break
        if num >= count:
            return True
        return False

        
    ##Prints the board in the shell
    ##Used for debug and dev
    def __str__(self):
        draw = ""
        #Prints column # above column
        draw += "||"
        for j in range(self.width):
            draw += str(j)
            draw += "|"
        draw += "|\n"
        draw += "||"
        for j in range(self.width):
            draw += "||"
        draw += "|\n"
        #Prints the board with the chips in it.
        for i in range((self.height - 1), -1, -1):
            draw += "||"
            for j in range(self.width):
                if (len(self.columns[j]) < (i + 1)):
                    draw += " "
                else:
                    draw += str(self.columns[j][i])
                draw += "|"
            draw += "|\n"
        return draw


#####################################################################################        
#Class of the computer controlled enemies
class AI(object):
    #This list holds the possible moves the AI queues
    def __init__(self, game, diff = 30, player = "P", AIplayer = "E"):
        #The difficulty of the AI
        self.diff = diff
        #The game the AI is playing in (ConnectGame class)
        self.game = game
        #The AI and player's chip
        self.player = player
        self.AIplayer = AIplayer
        self.moves = []


    #diff Setter/getter
    @property
    def diff(self):
        return self._diff
    @diff.setter
    def diff(self, value):
        if (value >= 1 and value <= 100):
            self._diff = value
        elif (value > 100):
            self._diff = 100

    #The main function of the AI; All functions in this class
    #are used in this function.
    def move(self):
        #Clears the self.moves list
        self.moves = []
        #Adds possible moves to a list
        availible = []
        for i in range(0, self.game.width):
            if not len(self.game.columns[i]) == self.game.height:
                availible.append(i)
        shuffle(availible)
        
        #First check to see if any spaces make a connect 4
        for i in availible:
            if self.game.check(self.AIplayer, self.game.winLength, i, len(self.game.columns[i])):
                self.moves.append(i)
                availible.remove(i)

        #Next, check to see if the player will be able to make a connect 4       
        for i in availible:
            if self.game.check(self.player, self.game.winLength, i, len(self.game.columns[i])):
                self.moves.append(i)
                availible.remove(i)
        
        #Next, try to build towards a 4 in a row.
            #The AI will attempt to make 3 in a row, then 2 in a row.
        for j in range((self.game.winLength - 1), 1, -1):
            for i in availible:
                if self.game.check(self.AIplayer, j, i, len(self.game.columns[i])):
                    self.moves.append(i)
                    availible.remove(i)

        #Finaly, a move is better than no move
        if not len(availible) == 0:
            self.moves.append(availible[randint(0,(len(availible)-1))])

        #if a move would result in the player having the ability to Connect 4
        #it should go to the end of the list.
        for i in self.moves:
            if self.game.check(self.player, self.game.winLength, i, (len(self.game.columns[i]) + 1)):
                #Except for moves that would win the AI the game
                if not self.game.check(self.AIplayer, self.game.winLength, i, (len(self.game.columns[i]))):
                    self.moves.remove(i)
                    self.moves.append(i)
                

        #Now the AI will attempt to execute the first of the listed moves by
        #rolling a d100. If the roll is less or equal to the AI difficulty, the 
        #move will be executed. If not, the move is deleted and the AI tries 
        #again with the next move.

        move = self.moves[-1]
        for i in self.moves:
            if self.diff >= randint(1,100):
                move = self.moves[0]
            else:
                self.moves.remove(i)
        
        #Now the AI will play the move
        self.game.play(self.AIplayer, move)
        return move
    
        

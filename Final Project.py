######################################################################################################################
# Name: Zach Hoover, Bryce Cook, Tyler Porrier
# Date: 5-13-20
# Description: Connect-4 Dungeon Crawler
##################################################################################################################

#####
#Game Class
#####

class ConnectGame(object):
    def __init__(self, width = 7, height =6):
        self.width = width
        self.height = height
        self.columns = {}
        self.setup()
        ##


    #height Setter/getter
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if (value >= 1):
            self._height = value

    #width Setter/getter
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if (value >= 1):
            self._width = value

    #Sets up a clean board
    def setup(self):
        for i in range(self.width):
            self.columns[i] = []

    #Used to play a chip
    def play(self, player, column):
        if (len(self.columns[column]) < self.height):
            self.columns[column].append(player)
            #winCheck(column)
            return True
        else:
            return False

    #Checks to see if the inputed chip causes 4 in a row.
    def winCheck(self, column):
        player = self.columns[column][-1]

        #Determines the height of the chip
        chipHeight = len(self.columns[column]) - 1

        #Top to bottom
        count = 1
        for i in range((len(self.columns[column]) - 2), -1, -1):
            if self.columns[column][i] == player:
                topBot += 1
            else:
                break
        if (count >= 4):
            return True

        #Left to right
        count = 1
        #Left
        if (column != 0):
            for i in range((column - 1), -1, -1):
                if (len(self.columns[i]) < (chipHeight + 1)):
                    break
                elif (self.columns[i][chipHeight] == player):
                    count += 1
                else:
                    break
        #Right
        if (column != self.width):
            for i in range((column + 1), self.width):
                if (len(self.columns[i]) < (chipHeight + 1)):
                    break
                elif (self.columns[i][chipHeight] == player):
                    count += 1
                else:
                    break
        if (count >= 4):
            return True

        #Diagonal top left to  bottom right
        count = 1
        #Left
        offset = 1
        if (column != 0):
            for i in range((column - 1), -1, -1):
                if (len(self.columns[i]) < (chipHeight + 1 + offset)):
                    break
                elif (self.columns[i][chipHeight + offset] == player):
                    count += 1
                else:
                    break
                offset += 1
        #Right
        offset = -1
        if (column != self.width):
            for i in range((column + 1), self.width):
                if (len(self.columns[i]) < (chipHeight + 1 + offset)) or ((chipHeight + offset) < 0):
                    break
                elif (self.columns[i][chipHeight + offset] == player):
                    count += 1
                else:
                    break
                offset -= 1

        if (count >= 4):
            return True

        #Diagonal top right to  bottom left
        count = 1
        #Left
        offset = -1
        if (column != 0):
            for i in range((column - 1), -1, -1):
                if (len(self.columns[i]) < (chipHeight + 1 + offset)) or ((chipHeight + offset) < 0):
                    break
                elif (self.columns[i][chipHeight + offset] == player):
                    count += 1
                else:
                    break
                offset -= 1
        #Right
        offset = 1
        if (column != self.width):
            for i in range((column + 1), self.width):
                if (len(self.columns[i]) < (chipHeight + 1 + offset)):
                    break
                elif (self.columns[i][chipHeight + offset] == player):
                    count += 1
                else:
                    break
                offset += 1

        if (count >= 4):
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
        


        
g = ConnectGame()

g.play("X",3)
g.play("X",3)
g.play("X",3)
g.play("X",2)
g.play("X",2)
g.play("X",1)


g.play("O",0)
g.play("O",1)
g.play("O",2)
g.play("O",3)

g.play("X",5)
print g
print g.winCheck(0)
print g.winCheck(1)
print g.winCheck(2)
print g.winCheck(3)

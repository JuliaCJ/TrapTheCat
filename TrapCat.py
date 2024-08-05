import random
import pygame
import os


#Constants
TILESIZE = 32
ROWS = 10
COLS = 10

HEIGHT = ROWS * TILESIZE #Y
WIDTH = COLS * TILESIZE #X

#Import Assests
pygame.init()
pygame.mixer.init()
yellowBox = pygame.transform.scale(pygame.image.load("yellowBox.png"), (TILESIZE, TILESIZE))
brownBox = pygame.transform.scale(pygame.image.load("brownBox.png"), (TILESIZE, TILESIZE))
catSprite = pygame.transform.scale(pygame.image.load("catSprite.png"), (TILESIZE, TILESIZE))
catSound = pygame.mixer.Sound("Meow.ogg")
tileSound = pygame.mixer.Sound("Click.wav")

#Tile Class
class Tile:

    #Intialize Tile Position and Color to Yellow
    def __init__(self, x, y):
        self.xPos = x * TILESIZE #Columns
        self.yPos = y * TILESIZE #Rows
        self.box = yellowBox
        self.clicked = False

    #Update Tile if Clicked
    #Return True if Tile was Successfully Clicked
    def click(self):
        if not self.clicked:
            self.clicked = True
            self.box = brownBox
            pygame.mixer.Sound.play(tileSound)
            return True
        else:
            return False

    #Draw the Tile
    def draw(self, surface):
        #X is Rows, Y is Columns
        surface.blit(self.box, (self.xPos, self.yPos))

#Board Class
class Board:

    #Keeps Track of if the Cat or User wins
    #Keeps Track of Whose Turn it is
    def __init__(self):
        self.start = True
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.tileList = [[Tile(i, j) for i in range(ROWS)] for j in range(COLS)]
        self.catX = random.randint(4, 7) #Generate Random Column
        self.catY = random.randint(4, 7) #Generate Random Row
        self.catTurn = False #Starts on User's Turn
        self.catWin = False
        self.userWin = False

        #Pre-Click 10 Tiles
        for i in range(15):
            new = False
            while not new:
                row = random.randint(0, ROWS-1)
                col = random.randint(0, COLS-1)
                new = self.tileList[row][col].click()

    #Draw the Board
    def draw(self, screen):
        for row in self.tileList:
            #Draw Every Tile in the Board
            for tile in row:
                tile.draw(self.surface)
        #Blit the Cat on Last
        if self.start:
            while self.tileList[self.catY] [self.catX].clicked:
                self.catX = random.randint(4, 7)  # Generate Random Column
                self.catY = random.randint(4, 7)  # Generate Random Row
            self.catX *= TILESIZE  # Convert to Coordinates
            self.catY *= TILESIZE  # Convert to Coordinates
            self.start = False
        self.surface.blit(catSprite, (self.catX, self.catY))
        #Finish Blit-ing the Entire Surface
        screen.blit(self.surface, (0,0))

    #Move the Cat on it's Turn
    #Updates catWin if the Cat Escapes
    def moveCat(self):
        #Check Validity of Move
        valid = False
        #Keep Trying Until Valid Move Occurs
        while not valid:
            #Randomly Pick a Direction
            direction = random.randint(1, 8)
            # Convert Coordinates to Rows and Columns
            x = int(self.catX / 32)
            y = int(self.catY / 32)
            match (direction):
                case 1:  #Move Up
                    y -= 1

                case 2:  #Move Up-Right
                    y -= 1
                    x += 1

                case 3:  #Move Right
                    x += 1

                case 4:  #Move Down-Right
                    y += 1
                    x += 1

                case 5:  #Move Down
                    y += 1

                case 6:  #Move Down-Left
                    y += 1
                    x -= 1

                case 7:  #Move Left
                    x -= 1

                case 8:  #Move Up-Left
                    y -= 1
                    x -= 1

            #Check if the Cat Wins
            if x <= -1 or y <= -1 or y >= ROWS or x >= COLS:
                self.catWin = True #Update catWin Variable
                self.updateCatPos(x, y) #Move the Cat Offscreen
                valid = True #The Winning Move is Valid
                pygame.mixer.Sound.play(catSound)
                break

            else:
                #Check if the Move is Valid
                valid = self.validMove(x, y)
                if valid:
                    #Move the Cat and Change the Turn
                    pygame.mixer.Sound.play(catSound)
                    self.updateCatPos(x, y)
                    self.catTurn = False

    #Check if the Cat's Move is Valid
    def validMove(self, x, y):
        if self.tileList[y][x].clicked:
            return False
        else:
            return True

    #Take in New Cat Row and Column and Convert to Coordinates
    def updateCatPos(self, x, y):
        self.catX = x * TILESIZE
        self.catY = y * TILESIZE

    def checkUserWin(self):
        directions = [
            (-1, 0),  # Up
            (-1, 1),  # Up-Right
            (0, 1),  # Right
            (1, 1),  # Down-Right
            (1, 0),  # Down
            (1, -1),  # Down-Left
            (0, -1),  # Left
            (-1, -1)  # Up-Left
        ]

        x = int(self.catX / TILESIZE)
        y = int(self.catY / TILESIZE)

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy

            if new_x < 0 or new_y < 0 or new_x >= COLS or new_y >= ROWS:
                return

            if not self.tileList[new_y][new_x].clicked:
                return

        self.userWin = True



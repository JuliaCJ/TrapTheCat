import pygame, sys
from pygame.locals import *
from TrapCat import *

#Constants
BLACK = (0,0,0)
WHITE = (255, 255, 255)

HEIGHT = ROWS * TILESIZE #Y
WIDTH = COLS * TILESIZE #X

RESOLUTION = (HEIGHT, WIDTH)

#Initialize Game Variables
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("TRAP THE CAT")
screen.fill(BLACK)
clock = pygame.time.Clock()

gameBoard = Board()

clickCol = 0
clickRow = 0

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 50)
text = my_font.render("", False, (0, 0, 0))
center = text.get_rect(center = (WIDTH/2, HEIGHT / 2))

winSound = pygame.mixer.Sound("WinSound.wav")
loseSound = pygame.mixer.Sound("LoseSound.wav")

end = False

while True:
    #Check if Anybody Wins. If They Do, Stop the Game
    if gameBoard.userWin:
        text = my_font.render("You Win!", False, (0,255,0))
        if not pygame.mixer.get_busy():
            pygame.mixer.Sound.play(winSound)
        end = True
    elif gameBoard.catWin:
        text = my_font.render("Cat Wins!", False, (255, 0, 0))
        if not pygame.mixer.get_busy():
            pygame.mixer.Sound.play(loseSound)
        end = True

    #Check if it's the Cat's Turn
    if gameBoard.catTurn and not end :
        gameBoard.moveCat()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keys[pygame.K_ESCAPE]:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN and not gameBoard.catTurn and not end:
            mx, my = pygame.mouse.get_pos()

            #Convert to Row and Column
            clickCol = int(mx // TILESIZE)
            clickRow  = int(my / TILESIZE)

            #Check if Cat is Standing on Tile
            catCol = int(gameBoard.catX / 32)
            catRow = int(gameBoard.catY / 32)


            if clickCol != catCol or clickRow != catRow:
                valid = gameBoard.tileList[clickRow][clickCol].click()
                #If the Tile Hasn't been Clicked, It Becomes the Cat's Turn
                if valid:
                    gameBoard.checkUserWin()
                    pygame.time.delay(100)

                    if not gameBoard.userWin:
                        gameBoard.catTurn = True

    #Update the Screen
    center = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.fill(BLACK)
    gameBoard.draw(screen)
    screen.blit(text, center)
    pygame.display.flip()
    clock.tick(60)



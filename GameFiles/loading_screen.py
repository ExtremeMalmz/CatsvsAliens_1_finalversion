#VT2022-DA336A-TS195 - Cats vs Aliens - Anita Olsson, Eric Malmström, Ibrahim Kara Man, Sayed Hassan
import pygame
import pygame, sys
from pygame.locals import *
import random

from Levels.level1 import level_1_game_loop

def loading_screen_main(levelNumber):
    '''
    main för loading screen allt händer har som är relaterad till loading screen
    '''    
    pygame.init()

    pygame.display.set_caption('LOADING THE GAME')

    WINDOW_SIZE = (900,700)

    screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

    display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    
    font = pygame.font.Font('freesansbold.ttf', 32)

    loadingMessage = font.render("Loading the game", True, (25, 255, 255))
    star = font.render("***", True, (25, 255, 255))
        
    einz,zwei,drei = random.randint(0,50),random.randint(50,70),random.randint(70,100)

    timer = 0

    while True:
        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(loadingMessage, (300, 300))

        timer += 1
 
        if einz <= timer:
            screen.blit(star, (300, 450))
            if zwei <= timer:
                screen.blit(star, (400,450))
                if drei <= timer:
                    screen.blit(star, (500, 450))
                    if zwei <= timer:
                        if levelNumber == "1":
                            level_1_game_loop()
                        
        pygame.display.update()
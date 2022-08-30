#VT2022-DA336A-TS195 - Cats vs Aliens - Anita Olsson, Eric Malmström, Ibrahim Kara Man, Sayed Hassan
import pygame
import pygame, sys
from pygame.locals import *
from pygame import mixer
import os

def winning_screen_main():    
    pygame.init()

    mixer.music.load(os.path.join('MusicVideos','background.wav'))
    # set to -1 for infinite music peoples
    mixer.music.play(-1)

    pygame.display.set_caption('CONGRATULATIONS YOU WON THE GAME')

    WINDOW_SIZE = (900,700)

    screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

    display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled
    
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))

    font = pygame.font.Font('freesansbold.ttf', 32)
    largerFont = pygame.font.Font('freesansbold.ttf', 64)

    winningMessage = font.render("Congratulations you won the game!", True, (25, 255, 255))

    thankYouMessage = font.render("Thanks for playing Cats vs Aliens", True, (25, 255, 255))
    pygameMessage = font.render("Made with PyGame", True, (25, 255, 255))

    cvaMessage = largerFont.render("Cats  VS  Aliens", True, (25, 255, 255))
    madeByMessage = font.render("Made By", True, (25, 255, 255))
    anitaMessage = font.render("Anita Olsson", True, (25, 255, 255))
    ericMessage = font.render("Eric Malmström", True, (25, 255, 255))
    ibrahimMessage = font.render("Ibrahim Kara Man", True, (25, 255, 255))
    sayedMessage = font.render("Sayed Hassan", True, (25, 255, 255))
    
    quitMessage = font.render("The game doesn't close by itself -Management", True, (229, 20, 29))
    timer = 0
    
    mixer.music.load(os.path.join('MusicVideos','ARelatoinshipWithTheCatlime.wav'))
    mixer.music.play(-1)
    
    while True:
        screen.fill((0,0 ,0))

        timer += 1 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if timer >= 0 and timer <= 2000: 
            screen.blit(winningMessage, (150, 300))

        if timer >= 2100 and timer <= 7000:
            screen.blit(thankYouMessage, (150, 300))
            screen.blit(pygameMessage, (270, 350))
        
        if timer >= 7600:
            screen.blit(cvaMessage, (200, 120))
            screen.blit(madeByMessage, (365, 200))
            screen.blit(anitaMessage, (335, 350))
            screen.blit(ericMessage, (312, 400))
            screen.blit(ibrahimMessage, (295, 450))
            screen.blit(sayedMessage, (320, 500))
            
        if timer >= 10000:
            screen.blit(quitMessage,(100,600))
    
        pygame.display.update()
#VT2022-DA336A-TS195 - Cats vs Aliens - Anita Olsson, Eric Malmström, Ibrahim Kara Man, Sayed Hassan
import pygame
import time
import os

from GameFiles.pyvidplayer import Video

surface = pygame.display.set_mode((900, 700))

vid = Video(os.path.join('MusicVideos',"EvenFunnierVideo.mp4"))
vid.set_size((900,700))
vid.toggle_pause()

vid1 = Video(os.path.join('MusicVideos',"MoreFunnierVideo.mp4"))
vid1.set_size((900,700))
vid1.toggle_pause()

def intro():
    '''
    plays the video which is entered as the vid variable
    '''
    pygame.display.set_caption('Gustav >:)')
    vid.toggle_pause()

    vid.set_volume(30)
    start = time.time()
    while True:
        vid.draw(surface,(0,0))
        pygame.display.update()

        duration = time.time() - start

        if duration >= 5:
            vid.restart()
            exit()

def outro():
    '''
    plays the video which is entered
    '''
    pygame.display.set_caption('Hi Chris')
    vid1.toggle_pause()

    vid1.set_volume(30)
    start = time.time()
    while True:
        
        vid1.draw(surface,(0,0))
        pygame.display.update()

        duration = time.time() - start
        if duration >= 30:
            vid1.restart()
            exit()
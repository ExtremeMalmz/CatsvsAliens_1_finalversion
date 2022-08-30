#VT2022-DA336A-TS195 - Cats vs Aliens - Anita Olsson, Eric Malmström, Ibrahim Kara Man, Sayed Hassan
import pygame
from pygame import mixer
from typing import Optional
from pygame.locals import *
from pygame_menu.examples import create_example_window
from pygame import mixer
import pygame_menu
import json
import os

from GameFiles.loading_screen import loading_screen_main

from GameFiles.video import intro, outro

pygame.init()

__all__ = ['main']

FPS = 60
WINDOW_SIZE = (900, 700)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pygame.Surface'] = None
main_menu: Optional['pygame_menu.Menu'] = None
bg_img = pygame.image.load(os.path.join('Assets', 'bg.png'))
background_image = pygame_menu.BaseImage(os.path.join('Assets', 'bg.png'))

def set_difficulty(value, difficulty):
    '''
    Game difficulty. 9 lives on easy. 1 life on hard.
    '''
    pass

def give_9_lives():
    with open(os.path.join('Assets','games.json'), 'r+') as f:
        data = json.load(f)

        for i in data['Games']:
            i['Player_Life_amount'] = 9
    
    with open(os.path.join('Assets','games.json'), 'w') as f:
        json.dump(data, f, indent = 2 )

    loading_screen_main("1")

def start_the_game():
    '''
    Sends you to the level 1 game loop unless your name is Gustav which if you are just enjoy the ride
    '''
    pygame.mixer.music.stop()

    with open(os.path.join('Assets','games.json'), 'r+') as f:
        data = json.load(f)

        for i in data['Games']:  
            if (i['Player_Name'].upper()).strip() == "GUSTAV":
                intro()
            if (i['Player_Name'].upper()).strip() == "CHRIS":
                outro()
            else:
                if (i['Player_Life_amount']) != 9:
                    give_9_lives()
                else:
                    loading_screen_main("1")

def MyTextValue(name):
    '''
    Gets the name which is in the JSON file
    '''    
    with open(os.path.join('Assets','games.json'), 'r+') as f:
        data = json.load(f)

        for i in data['Games']:
            i['Player_Name'] = name

    with open(os.path.join('Assets','games.json'), 'w') as f:
        json.dump(data, f, indent = 2 )

def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    background_image.draw(surface)

def the_main(test: bool = False) -> None:
    '''
    Main menu screen along with buttons
    :param test: Indicate function is being tested
    '''
    global main_menu
    global sound
    global surface
    pygame.display.set_caption('Menu')

    mixer.music.load(os.path.join('MusicVideos','background.wav'))
    mixer.music.play(-1)
    
    surface = create_example_window('Cats vs Aliens', WINDOW_SIZE)
    clock = pygame.time.Clock()

    main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    main_menu_theme.set_background_color_opacity(0.2)  # 50% opacity
    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=main_menu_theme,
        title='Menu',
        width=WINDOW_SIZE[0] * 0.8,
    )
    
    theme_bg_image = main_menu_theme.copy()
    theme_bg_image.background_color = pygame_menu.BaseImage(
        image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER
    )
    theme_bg_image.title_font_size = 25
    menu_with_bg_image = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.EXIT,
        theme=theme_bg_image,
        title='Cats vs Aliens Menu',
        width=WINDOW_SIZE[0] * 0.8
    )
    menu_with_bg_image.add.button('Back', pygame_menu.events.BACK)

    widget_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
    widget_menu_theme.widget_margin = (0, 10)
    widget_menu_theme.widget_padding = 0
    widget_menu_theme.widget_selection_effect.margin_xy(10, 5)
    widget_menu_theme.widget_font_size = 20
    widget_menu_theme.set_background_color_opacity(0.2)  # 50% opacity

    widget_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=widget_menu_theme,
        title='FAQ',
        width=WINDOW_SIZE[0] * 0.8,
    )

    button_image = pygame_menu.BaseImage(
        pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER)
    widget_menu.add.label(
        title="Type in the name Gustav before starting a New Game and se what happens! ", max_char=-1, font_size=20)
    
    with open(os.path.join('Assets','games.json'), 'r') as f:
        data = json.loads(f.read())

        for i in data['Games']:
            name = i['Player_Name']
            
    main_menu.add.text_input('Name : ', default = name, onchange=MyTextValue)
    main_menu.add.selector('Difficulty :', [(
        'Catnip', 1), ('Food', 2), ('Veternarian', 3)], onchange=set_difficulty)
    main_menu.add.button('New Game', start_the_game)
    main_menu.add.button('Continue',
                         lambda: print('continue to game...'))
    main_menu.add.button('FAQ', widget_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        clock.tick(FPS)

        main_menu.mainloop(surface, main_background,
            disable_loop=test, fps_limit=FPS)

        pygame.display.flip()
import pygame, sys, os, json
from pygame.locals import *

import pygame as pg

pg.init()

from Levels.level17 import level_17_game_loop

def player_coordinates_printer(playerX,playerY):
    '''
    prints player rects x and y coordinates, is only for debugging
    '''
    print("X is")
    print(playerX)

    print("Y is")
    print(playerY)

def send_to_level_17():
    '''
    Sends the player to level5.py
    '''
    level_17_game_loop()

def send_back_to_main():
    '''
    Sends the program back to the main menu file. Python doesnt allow circular imports so I was forced to do it like this
    '''
    import GameFiles.main_menu
    returnToMain = GameFiles.main_menu.the_main()
    returnToMain

def enemy_movement_direction(enemy):
    '''
    Returns the enemy Ai moving direction
    '''
    if enemy.x == 32:
        direction = "right"
        return direction

    if enemy.x == 267:
        direction = "left"
        return direction

def enemy_movement(enemy,direction):
    '''
    Determines which direction the AI should move
    '''
    if direction == "left":
        enemy.x -= 1
    else:
        enemy.x += 1
    
def player_death(rect):
    '''
    Respawns the player in case of death
    '''
    rect.y = 96
    rect.x = 16

    with open(os.path.join('Assets','games.json'), 'r+') as f:
        data = json.load(f)
                
        for i in data['Games']:
            i['Player_Life_amount'] = i['Player_Life_amount'] - 1
            
            if i['Player_Life_amount'] == i['Player_Life_amount'] == 0:
                send_back_to_main()

    with open(os.path.join('Assets','games.json'), 'w') as f:
        json.dump(data, f, indent = 2 ) 

def load_map(path):
    '''
    adds a .txt to inputted file which should be a level map
    '''
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    '''
    Handles player movement
    '''
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def level_16_game_loop():
    '''
    Game loop for main, basically the main for the game
    '''
    WINDOW_SIZE = (900,700)

    screen = pygame.display.set_mode(WINDOW_SIZE,5,32) 

    display = pygame.Surface((300,200)) 

    clock = pygame.time.Clock()
    pygame.display.set_caption('Level cuatro')

    with open(os.path.join('Assets','games.json'), 'r+') as f:
            data = json.load(f)

            for i in data['Games']:
                i['Player_Level'] = 4

    with open(os.path.join('Assets','games.json'), 'w') as f:
            json.dump(data, f, indent = 2 )

    pygame.display.set_caption('Level 17')

    game_map = load_map(os.path.join('levels', 'level16'))

    stone6_image = pygame.image.load(os.path.join('Assets', 'stone6.jpeg'))
    ice_image = pygame.image.load(os.path.join('Assets','Snow.TIFF'))
    flag_image = pygame.image.load(os.path.join('Assets','flag.tiff'))
    whitebricks_image = pygame.image.load(os.path.join('Assets','whitebricks.jpg'))
    snowrock_image = pygame.image.load(os.path.join('Assets','snowrock.png'))
    tree_image = pygame.image.load(os.path.join('Assets','tree.png'))
    

    player_image = pygame.image.load(os.path.join('Assets','player.png')).convert()
    player_image_original = pygame.image.load(os.path.join('Assets','player.png')).convert()
    player_image_mirror = pygame.image.load(os.path.join('Assets','playermirror.png')).convert()

    player_image.set_colorkey((0, 0, 0))
    player_image_original.set_colorkey((0, 0, 0))
    player_image_mirror.set_colorkey((0, 0, 0))

    player_image_hunch = pygame.image.load(os.path.join('Assets','playerhunched.png')).convert()
    player_image_hunch.set_colorkey((0, 0, 0))

    player_image_hunch_mirrored = pygame.image.load(os.path.join('Assets','playermirrorhunched.png')).convert()
    player_image_hunch_mirrored.set_colorkey((0,0,0))

    super_bullet_image = pygame.image.load(os.path.join('Assets','BULLETWORKPLEASE.png')).convert()
    super_bullet_image.set_colorkey((0,0,0))

    super_bullet_image_mirror = pygame.image.load(os.path.join('Assets','BULLETWORKPLEASEmirror.png')).convert()
    super_bullet_image_mirror.set_colorkey((0,0,0))
    
    player_rect = pygame.Rect(100,100,16,32)

    enemy_image = pygame.image.load(os.path.join('Assets','enemy.png')).convert()
    enemy_image.set_colorkey((0, 0, 0))
    enemy_rect = pygame.Rect(267, 120, 16, 16)

    background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    true_scroll = [0,0]

    while True: 
        playerXcoordinate = player_rect.x
        playerYcoordinate = player_rect.y

        display.fill((235,235,235)) 

        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(146, 187, 135),pygame.Rect(0,120,300,80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(display,(224,224,224),obj_rect)
            else:
                pygame.draw.rect(display,(146, 187, 135),obj_rect)

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(stone6_image,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '2':
                    display.blit(ice_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '3':
                    display.blit(flag_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '4':
                    display.blit(whitebricks_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '5':
                    display.blit(stone6_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '6':
                    display.blit(snowrock_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '7':
                    display.blit(tree_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                x += 1
            y += 1

        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        player_rect,collisions = move(player_rect,player_movement,tile_rects)

        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        display.blit(player_image,(player_rect.x-scroll[0],player_rect.y-scroll[1]))

        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                    if player_image == player_image_mirror:
                        player_image = player_image_original
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                    if player_image == player_image_hunch:
                       player_image = player_image_hunch_mirrored
                    else:
                        player_image = player_image_mirror
                if event.key == K_SPACE:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                        pass
                    else:
                        if player_image == player_image_original:
                            super_bullet_rect = pygame.Rect(playerXcoordinate+20, playerYcoordinate, 50, 14)
                            display.blit(super_bullet_image,(player_rect.height+135,player_rect.width+100))

                            if super_bullet_rect.colliderect(enemy_rect):
                                enemy_rect.x,enemy_rect.y = -1000,-1000
     
                        elif player_image == player_image_mirror:
                            super_bullet_mirror_rect = pygame.Rect(playerXcoordinate-30, playerYcoordinate,50,14)
                            display.blit(super_bullet_image_mirror,(player_rect.height+85,player_rect.width+100))
                                                    
                            if super_bullet_mirror_rect.colliderect(enemy_rect):
                                enemy_rect.x,enemy_rect.y = -1000,-1000
                        else:
                            super_bullet_rect = pygame.Rect(playerXcoordinate+20, playerYcoordinate, 50, 14)
                            display.blit(super_bullet_image,(player_rect.height+135,player_rect.width+100))

                            if super_bullet_rect.colliderect(enemy_rect):
                                enemy_rect.x,enemy_rect.y = -1000,-1000

                if event.key == K_UP or event.key == K_w:
                    if air_timer < 6:
                        vertical_momentum = -5
                if event.key == K_DOWN or event.key == K_s:
                    player_rect = pygame.Rect(playerXcoordinate,playerYcoordinate, 16,14)
                    player_image = player_image_hunch
    
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
                if event.key == K_DOWN or event.key == K_s:
                    player_rect = pygame.Rect(playerXcoordinate,playerYcoordinate, 16,32)
                    player_image = player_image_original

        if player_rect.y >= 300 :
            player_death(player_rect)

        display.blit(enemy_image,(enemy_rect.x-scroll[0],enemy_rect.y-scroll[1]))

        if enemy_rect.x == 32 or enemy_rect.x == 267:
            direction = enemy_movement_direction(enemy_rect)

        enemy_movement(enemy_rect,direction)
       
        #take away # if you want x and y coords
        #player_coordinates_printer(playerXcoordinate,playerYcoordinate)

        if enemy_rect.colliderect(player_rect):
            player_death(player_rect)

        if player_rect.x >= 1562 and player_rect.y == 16:
           send_to_level_17()

         # 1. pickes player life from json file: 
        with open(os.path.join('Assets','games.json'), 'r') as f:
            data = json.loads(f.read())

            for i in data['Games']:
                life = i['Player_Life_amount']

        # 2. Show player life in pygame display: 
        FONT = pg.font.Font(None, 42)

        text_surface = FONT.render('Life: ' + str(life), True, pg.Color('dodgerblue1'))
        text_rect = text_surface.get_rect()
        text_rect.midleft = (screen.get_width()-100, 38)
            
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        clock.tick(60)
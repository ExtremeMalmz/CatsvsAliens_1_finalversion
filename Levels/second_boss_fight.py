#VT2022-DA336A-TS195 - Cats vs Aliens - Anita Olsson, Eric Malmström, Ibrahim Kara Man, Sayed Hassan
import pygame, sys, os, json
from pygame.locals import *

from GameFiles.winning_screen import winning_screen_main

def player_coordinates_printer(playerX,playerY):
    '''
    prints player rects x and y coordinates, is only for debugging
    '''
    print("X is")
    print(playerX)

    print("Y is")
    print(playerY)

def win_game():
    '''
    sends the program back to the main menu
    '''
    winning_screen_main()

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
    print("moves")

def enemy_movement(enemy,direction):
    '''
    Determines which direction the AI should move
    '''
    print("direction")

def player_death(rect):
    '''
    Respawns the player in case of death
    '''
    rect.y = 32
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
    '''
    handles collisions between map tiles and player rect
    '''
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

def second_boss_fight_main():
    '''
    Game loop for main, basically the main for the game
    '''
    
    WINDOW_SIZE = (900,700)

    screen = pygame.display.set_mode(WINDOW_SIZE,5,32) 

    display = pygame.Surface((300,200))

    clock = pygame.time.Clock()
    pygame.display.set_caption('Level 20')

    with open(os.path.join('Assets','games.json'), 'r+') as f:
            data = json.load(f)
            for i in data['Games']:
                i['Player_Level'] = 1

    with open(os.path.join('Assets','games.json'), 'w') as f:
            json.dump(data, f, indent = 2 )

    game_map = load_map(os.path.join('levels', 'second_boss_fight'))

    grass_img = pygame.image.load(os.path.join('Assets', 'grass.png'))
    dirt_img = pygame.image.load(os.path.join('Assets','dirt.png'))
    knd_image = pygame.image.load(os.path.join('Assets','knd.png'))
    flag_image = pygame.image.load(os.path.join('Assets','flag.tiff'))
    red_image = pygame.image.load(os.path.join('Assets','red.png'))

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

    player_rect = pygame.Rect(32,152,16,32)

    boss_image = pygame.image.load(os.path.join('Assets','SecondBoss.png')).convert()
    boss_image.set_colorkey((0, 0, 0))
    boss_rect = pygame.Rect(208, 162, 26, 64)

    background_objects = [[0.1,[320,50,70,400]]]

    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    true_scroll = [0,0]    

    while True: 
        playerXcoordinate = player_rect.x
        playerYcoordinate = player_rect.y

        display.fill((151, 120, 120)) 

        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(255,255,255),pygame.Rect(0,120,300,40))

        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
            if background_object[0] == 0.1:
                pygame.draw.rect(display,(222,20,60),obj_rect)
            else:
                pygame.draw.rect(display,(9,91,85),obj_rect)

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '2':
                    display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '3':
                    display.blit(knd_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '4':
                    display.blit(flag_image, (x * 16-scroll[0], y * 16-scroll[1]))
                if tile == '6':
                    display.blit(red_image, (x * 16-scroll[0], y * 16-scroll[1]))
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
    	
        for event in pygame.event.get():
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

                            if super_bullet_rect.colliderect(boss_rect):
                                winning_screen_main()
                                
                        elif player_image == player_image_mirror:
                            super_bullet_mirror_rect = pygame.Rect(playerXcoordinate-30, playerYcoordinate,50,14)
                            display.blit(super_bullet_image_mirror,(player_rect.height+85,player_rect.width+100))
                                          
                            if super_bullet_mirror_rect.colliderect(boss_rect):
                                winning_screen_main()
                        else:
                            super_bullet_rect = pygame.Rect(playerXcoordinate+20, playerYcoordinate, 50, 14)
                            display.blit(super_bullet_image,(player_rect.height+135,player_rect.width+100))

                            if super_bullet_rect.colliderect(boss_rect):
                                winning_screen_main()                                

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

        if player_rect.y >= 500 :
            player_death(player_rect)
     
        display.blit(boss_image,(boss_rect.x-scroll[0],boss_rect.y-scroll[1]))

        if boss_image:
            if boss_rect.colliderect(player_rect):
                player_death(player_rect)
            if boss_rect.x <= 208 and boss_rect.y == 162 and boss_rect.x != 0:
                boss_rect.x -= 0.5
            elif boss_rect.x == 0 and boss_rect.y != 52:
                boss_rect.y -= 1

        if playerXcoordinate == 64 and playerYcoordinate == 192 or playerXcoordinate == 336 and playerYcoordinate == 192:
            rocket = 1

        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)
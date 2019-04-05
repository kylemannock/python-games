import random
import pygame, sys
from pygame.locals import *

BLACK = (0,  0,  0)
BROWN = (153,76, 0)
GREEN = (0,  255,0)
BLUE  = (0,  0,  255)
GREY  = (211,211,211)
RED   = (255,0,  0)
WHITE = (255,255,255)

DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
ROCK  = 4
LAVA  = 5
CLOUD = 6

resources = [DIRT, GRASS, WATER, COAL, ROCK, LAVA]

'''colours = {
    DIRT  : BROWN,
    GRASS : GREEN,
    WATER : BLUE,
    COAL  : BLACK,
    ROCK  : GREY,
    LAVA  : RED
    }'''

textures = {
    DIRT  : pygame.image.load("images/dirt.png"),
    GRASS : pygame.image.load("images/grass.png"),
    WATER : pygame.image.load("images/water.png"),
    COAL  : pygame.image.load("images/coal.png"),
    ROCK  : pygame.image.load("images/rock.png"),
    LAVA  : pygame.image.load("images/lava.png"),
    CLOUD  : pygame.image.load("images/cloud.png")
    }

inventory = {
    DIRT  : 0,
    GRASS : 0,
    WATER : 0,
    COAL  : 0,
    ROCK  : 0,
    LAVA  : 0
    }

'''tilemap = [
    [GRASS, COAL, DIRT, DIRT, ROCK],
    [WATER, WATER, GRASS, ROCK, ROCK],
    [COAL, GRASS, WATER, LAVA, ROCK],
    [DIRT, GRASS, COAL, LAVA, COAL],
    [GRASS, WATER, DIRT, GRASS, LAVA]
    ]'''

TILESIZE = 40
MAPWIDTH = 40
MAPHEIGHT = 20

'''tilemap = [[random.choice(resources)
            for w in range(MAPWIDTH)]
           for h in range(MAPHEIGHT)]'''

tilemap = [[DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT)]

count = [0] * (LAVA + 1)

for rw in range(MAPHEIGHT):
    for cl in range(MAPWIDTH):
        randomNumber = random.randint(0,20)
        if randomNumber == 0:
            tile = LAVA
        elif randomNumber == 1 or randomNumber == 2:
            tile = ROCK
        elif randomNumber >= 3 and randomNumber <=5:
            tile = COAL
        elif randomNumber >= 6 and randomNumber <=8:
            tile = WATER
        elif randomNumber >= 9 and randomNumber <=11:
            tile = GRASS
        else:
            tile = DIRT
        count[tile] += 1
        tilemap[rw][cl] = tile

for index in range(len(count)):
    print(index, " = ", count[index])

pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE + 50))

INVFONT = pygame.font.Font('fonts/FreeSansBold.ttf',18)
PLAYER = pygame.image.load('images/player.png').convert_alpha()
playerPos = [0,0]

cloudx = -200
cloudy = 0

fpsClock = pygame.time.Clock()

pygame.display.set_caption('My Minecraft')
pygame.display.set_icon(pygame.image.load('images/player.png'))

while True:
    DISPLAYSURF.fill(BLACK)
    
    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_RIGHT) and playerPos[0] < MAPWIDTH - 1:
                playerPos[0] += 1
            elif (event.key == K_LEFT) and playerPos[0] > 0:
                playerPos[0] -= 1
            elif (event.key == K_UP) and playerPos[1] > 0:
                playerPos[1] -= 1
            elif (event.key == K_DOWN) and playerPos[1] < MAPHEIGHT - 1:
                playerPos[1] += 1
            elif event.key == K_SPACE:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                inventory[currentTile] += 1
                tilemap[playerPos[1]][playerPos[0]] = DIRT
            elif event.key == K_1:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if inventory[DIRT] > 0:
                    inventory[DIRT] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = DIRT
                    inventory[currentTile] += 1
            elif event.key == K_2:
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                if inventory[GRASS] > 0:
                    inventory[GRASS] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = GRASS
                    inventory[currentTile] += 1

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(textures[tilemap[row][column]],
                             (column*TILESIZE,row*TILESIZE))
            '''pygame.draw.rect(DISPLAYSURF,colours[tilemap[row][column]],
                             (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))'''
            
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))
    
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(),(cloudx,cloudy))
    cloudx += 3
    if cloudx > MAPWIDTH*TILESIZE:
        cloudy = random.randint(0,MAPHEIGHT*TILESIZE)
        cloudx = -200

    placePosition = 10
    barPosition = MAPHEIGHT*TILESIZE + 10
    for item in resources:
        DISPLAYSURF.blit(textures[item],(placePosition,barPosition))
        placePosition += 60
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,barPosition + 10))
        placePosition += 50
    
    pygame.display.update()
    fpsClock.tick(24)

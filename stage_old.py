# -*- coding: utf-8 -*-

import pygame
from characters import *
from pygame.locals import *
from resourceManager import *
from control import *
from utilities import *
import os

##
# CONSTANTS
##
PLAYER_INIT_POS_X = 50
PLAYER_INIT_POS_Y = 835

ENEMY_INIT_POS_X = 500
ENEMY_INIT_POS_Y = 835

# Borders to scroll with
MIN_X_PLAYER = 100
MAX_X_PLAYER = ANCHO_PANTALLA - MIN_X_PLAYER

WHITE = (255, 255, 255)

FLOORPLATFORM = (0, 842, 2200, 5)
PLATFORM1 = (300, 780, 150, 12)
PLATFORM2 = (550, 750, 12, 150)

##
# Stage Class
##

class Stage:
	#Stage number as class parameter, only 1 stage, not parameters needed for now
	#creating it with no paramerter
    def __init__(self):
        self.background = Background()

	   #scroll (not implemented)

	   #Character Sprites:
        # self.player = RangedPlayer(Bow())
        self.player = MeleePlayer(Sword())
        self.playerGroup = pygame.sprite.Group( self.player )

        #Set of the background we are visualizing
        self.scrollx = 0

       #Enemy Sprite
        self.enemy = Skeleton()
        self.enemyGroup = pygame.sprite.Group(self.enemy)

        #Set enemy position
        self.enemy.setPosition((ENEMY_INIT_POS_X, ENEMY_INIT_POS_Y))
        #Set player position
        self.player.setPosition((PLAYER_INIT_POS_X, PLAYER_INIT_POS_Y))

        #Floor platform
        floorPlatform = Platform(pygame.Rect(FLOORPLATFORM))
        #Other Platforms
        platform1 = Platform(pygame.Rect(PLATFORM1))
        platform2 = Platform(pygame.Rect(PLATFORM2))
        self.platformGroup = pygame.sprite.Group(floorPlatform, platform1, platform2)
        
        #Group with dynamic Sprites
        #self.dynamicSpritesGroup = pygame.sprite.Group(self.enemy)

        #Group with dynamic Sprites
        self.dynamicSpritesGroup = pygame.sprite.Group(self.player, self.enemy)

        #Group with all Sprites
        self.spritesGroup = pygame.sprite.Group(self.player, self.enemy, floorPlatform, platform1)

        self.control = ControlKeyboard()

    #player scroll left side
    def updateOrganizedScroll(self, player):

        #player beyond left side
        if (player.rect.left < MIN_X_PLAYER):
            movement = MIN_X_PLAYER - player.rect.left

            #if we cant move more to left side
            if self.scrollx <= 0:
                self.scrollx = 0

                if (player.rect.left<= 0):
                    player.setPosition((0, player.position[1]))

                return False
            

            #if we can scroll left side
            else:    
                self.scrollx = self.scrollx - movement
                return True
        #AQUI NO TESTED
        elif (player.rect.right > MAX_X_PLAYER):

            movement = player.rect.right - MAX_X_PLAYER

            if (self.scrollx + ANCHO_PANTALLA >= self.background.rect.right):
                self.scrollx = self.background.rect.right - ANCHO_PANTALLA

                if (player.rect.right >= ANCHO_PANTALLA):
                #MIRAR SI EXISTE PLAYER SIZE
                    player.setPosition((self.scrollx + ANCHO_PANTALLA - player.rect.width, player.position[1]))
                return False
            else:

                self.scrollx = self.scrollx + movement
            return True

    def updateScroll(self, player):
        changeScroll = self.updateOrganizedScroll(player)

        if changeScroll:
            for sprite in iter(self.spritesGroup):
                sprite.setScreenPosition((self.scrollx, 0))
            
            self.background.update(self.scrollx)

    def update(self, time):
        self.enemy.move_cpu(self.player)
        self.dynamicSpritesGroup.update(self.platformGroup, self.enemyGroup, time)
        
        #updating scroll
        self.updateScroll(self.player)
        return False

    def draw(self, screen):
      
      self.background.draw(screen)
      self.spritesGroup.draw(screen)
    	
    def events(self, events_list):
    	# Exit events
        for event in events_list:
            # Exiting game
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            
            if event.type == pygame.KEYDOWN:
                self.control.atack(self.player, self.dynamicSpritesGroup, self.spritesGroup, self.scrollx, event)
        
        self.player.move(self.control)
        # Action to realize depending on key pressed
        #keyPressed = pygame.key.get_pressed()
        # No se sale del programa
        #return False


##
# Platform class
##
class Platform(MySprite):
    def __init__(self, rectangulo):
        MySprite.__init__(self)
        self.rect = rectangulo
        self.setPosition((self.rect.left, self.rect.bottom))

        #Not showing platforms
        self.image = pygame.Surface((0,0))





##
# Background class
##

class Background:
    def __init__(self):
        self.image = ResourceManager.LoadImage('Images','forest.png')
        self.image = pygame.transform.smoothscale(self.image, (1535, 1400))

        self.rect = self.image.get_rect()
        #self.rect.bottom = ALTO_PANTALLA

        #Subimage we are seeing
        self.rectSubimage = pygame.Rect(0, ALTO_PANTALLA/2, ANCHO_PANTALLA, ALTO_PANTALLA)
        #self.rectSubimage.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

        

    def update(self, scrollx):
        self.rectSubimage.left = scrollx

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.rectSubimage)

        pygame.draw.rect(screen, WHITE, PLATFORM1)
        pygame.draw.rect(screen, WHITE, PLATFORM2)
        #pygame.draw.rect(screen, WHITE, (FLOORPLATFORM))
        #screen.blit(self.image, self.rect)
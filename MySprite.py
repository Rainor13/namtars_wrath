import pygame
import sys
import os

#Movement variables
IDLE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

#Animations
SPRITE_IDLE = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2

BULLET_SPEED  = (1,0)
#Char speed
CHAR_SPEED = 0.13 #pixels per ms
CHAR_JUMP_SPEED = 0.29 #pixels per ms
CHAR_ANIMATION_DELAY = 5 #Char image update time

GRAVITY = 0.0003 #pixels/ms²

#Clase MySprite
class MySprite(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)
        self.speed = (0, 0)
        self.scroll = (0, 0)

    #This method changes the global position. 
    def setPosition(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    #Changes the scroll value in the screen, but not the global position.
    #Changes in the local position does not imply global position change
    def setScreenPosition(self, decorScroll):
        self.scroll = decorScroll
        (scrollX, scrollY) = self.scroll
        (posX, posY) = self.position
        self.rect.left = posX - scrollX
        self.rect.bottom = posY - scrollY


    def increasePosition(self, increment):
        (posX, posY) = self.position
        (incrementX, incrementY) = increment
        self.setPosition((posX + incrementX, posY + incrementY))

    def update(self, time):
        incrementX = self.speed[0] * time
        incrementY = self.speed[1] * time
        self.increasePosition((incrementX, incrementY))
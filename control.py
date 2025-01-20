import pygame
from pygame.locals import *

class Control:

    # Acciones que puede realizar un jugador
    def idle(self):
        raise NotImplementedError()

    def jump(self):
        raise NotImplementedError()

    def left(self):
        raise NotImplementedError()

    def right(self):
        raise NotImplementedError()

    def shoot(self):
        raise NotImplementedError()


class ControlKeyboard(Control):
    key_jump = K_w
    key_left = K_a
    key_right = K_d
    key_atack = K_SPACE

    def idle(self):
        pressedKeys = pygame.key.get_pressed()
        return all(v == 0 for v in pressedKeys[:290])

    def jump(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_jump]

    def left(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_left]

    def right(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_right]

    def isAttacking(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_atack]
        
    def atack(self, player, grupoSpritesDinamicos, grupoSprites, scrollx, event):
        if event.key == pygame.K_SPACE:
           player.attack(grupoSpritesDinamicos, grupoSprites, scrollx)
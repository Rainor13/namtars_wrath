# -*- coding: utf-8 -*-

import pygame
import sys
import os
from pygame.locals import *
from resourceManager import *
from utilities import *
from MySprite import *
import stage
import director

#Movement variables
IDLE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
ATTACKING = 5
HURT = 6
DIE = 7

#Animations
SPRITE_IDLE = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2
SPRITE_ATTACKING = 3
SPRITE_KNOCKED = 4
SPRITE_DYING = 5

BULLET_SPEED  = (1,0)
#Char speed
CHAR_SPEED = 0.13 #pixels per ms
CHAR_JUMP_SPEED = 0.35 #pixels per ms
CHAR_ANIMATION_DELAY = 5 #Char image update time
CHAR_KNOCK = 1000 #Char knockback time

GRAVITY = 0.0003 #pixels/ms²

#HP
PLAYER_HP = 10

class Character(MySprite):
    "Any game character, ally or enemy"

    def __init__(self, imageFile, coordFile, numImages, runSpeed, jumpSpeed, animationDelay, hp):
        #First of all we call the constructor of MySprite
        MySprite.__init__(self)

        #Load the sprite sheet
        self.sheet = ResourceManager.LoadImage('Characters',imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        #Movement
        self.movement = IDLE
        #
        self.looking = LEFT

        self.isJumping = False
        self.isKnocked = False
        self.lastHit = pygame.time.get_ticks()
        self.cooldownHit = 1500

        data = ResourceManager.LoadCoordsFile('Characters',coordFile)
        data = data.split()
        self.animationNumber = 1
        self.postureImageNum = 0
        count = 0

        self.sheetCords = []
        for line in range (0, 8):
            self.sheetCords.append([])
            tmp = self.sheetCords[line]
            for animation in range(1, numImages[line] + 1):
                tmp.append(pygame.Rect((int(data[count]), 
                int(data[count + 1]), int(data[count + 2]), 
                int(data[count + 3]))))
                count += 4

        #Delay when we change Sprite image (this prevents moving fast)
        self.movementDelay = 0

        #Initial animation
        self.animationNumber = IDLE

        #Sprite initial position
        self.rect = pygame.Rect(100, 100, 
                                self.sheetCords[self.animationNumber]
                                [self.postureImageNum][2],
                                self.sheetCords[self.animationNumber]
                                [self.postureImageNum][3])

        #Walking and jumping speeds
        self.runSpeed = runSpeed
        self.jumpSpeed = jumpSpeed

        #Character animation delay
        self.animationDelay = animationDelay

        #Character HPself.steps = ResourceManager.LoadSound("steps.wav")
        self.hp = hp

        #Update Initial Animation Sprite, callong update
        self.updatePosture()

        #if gravity applies to char
        self.gravity = True

        #if enemy foe is a jumper
        self.jumper = False

    #Movement method. Stores which one it will use
    def move(self, movement):
        if not(self.isKnocked):
            if movement == UP:
                #If we are knocked and you want to jump, you can't
                if self.animationNumber == SPRITE_JUMPING:
                    self.isJumping = True
                else:
                    self.movement = UP
            elif movement == HURT:
                if self.animationNumber == SPRITE_KNOCKED:
                    self.isKnocked = True
                else:
                    self.movement = HURT
            else:
                self.movement = movement


    def updatePosture(self):
        self.movementDelay -= 1
        #Check if delay has happen to draw new animation
        if self.movementDelay < 0:
            self.movementDelay = self.animationDelay
            #If it has happen, update posture
            self.postureImageNum += 1
            if self.postureImageNum >= len(self.sheetCords[self.animationNumber]):
                self.postureImageNum = 0
            if self.postureImageNum < 0:
                self.postureImageNum = len(self.sheetCords[self.animationNumber]) - 1

            self.image = self.sheet.subsurface(self.sheetCords[self.animationNumber][self.postureImageNum])

            #If we are looking to the left, we use the sheet portion
            if self.looking == RIGHT:
                self.image = self.sheet.subsurface(self.sheetCords[self.animationNumber][self.postureImageNum])
            #If not we flip the image
            elif self.looking == LEFT:
                self.image = pygame.transform.flip(self.sheet.subsurface(self.sheetCords[self.animationNumber]
                                                [self.postureImageNum]), True, False)


    def update(self, platformGroup, enemyGroup, time):
        
        #Check if char is alive
        if self.hp <= 0:
            if self.alive == True:
                self.hurt.set_volume(0.7)
                self.hurt.play()
            orb = ResourceManager.LoadImage("Images", "orb_yellow.png", -1)
            image = pygame.transform.scale(orb, (20, 20))
            self.alive = False
            self.image = image

            #Orbs fall with gravity
            platforms_collided = pygame.sprite.spritecollide(self, platformGroup, False)
            (speedX, speedY) = self.speed
            speedY = GRAVITY * time
            (speedX, speedY) = self.check_collisions_with_floor_ceiling(platforms_collided, (speedX, speedY), time)
            self.speed = (0, speedY)
            MySprite.update(self, time)
        else:
            (speedX, speedY) = self.speed
            now = pygame.time.get_ticks()
            #If we are knocked can't do other animation
            if not (self.animationNumber == SPRITE_KNOCKED and ((now - self.lastHit) < CHAR_KNOCK)):
                #If going left or right
                if (self.movement == LEFT or self.movement == RIGHT):
                    #Assign the looking direction
                    self.looking = self.movement
                    #If looking left
                    if self.movement == LEFT:
                        speedX = -self.runSpeed

                    #If looking right
                    else:
                        speedX = self.runSpeed
                    #If not jumping
                    if self.animationNumber != SPRITE_JUMPING:
                        #Posture would be walking
                        self.animationNumber = SPRITE_WALKING

                        if pygame.sprite.spritecollideany(self, platformGroup) == None:
                            self.animationNumber = SPRITE_JUMPING

                    if self.jumper == True:
            
                        Character.move(self, UP)
                        self.movement = UP

                #If we want to jump
                elif self.movement == UP:
                    #Check if we are already jumping
                    if not (self.isJumping):
                        self.animationNumber = SPRITE_JUMPING
                        speedY = -self.jumpSpeed
                
                #If attacking (must be in idle)
                elif self.animationNumber == SPRITE_IDLE and self.movement == ATTACKING:
                    self.animationNumber = SPRITE_ATTACKING
                
                #If we are hit
                elif self.movement == HURT:
                    self.animationNumber = SPRITE_KNOCKED
                    if not (self.isKnocked):
                        if self.looking == RIGHT:
                            speedX = -self.runSpeed
                        else:
                            speedX = self.runSpeed
                        speedY = (-self.jumpSpeed / 4)

                #If we are in idle
                elif self.movement == IDLE:
                    #If we are not jumping or knocked
                    if not (self.animationNumber == SPRITE_JUMPING or self.animationNumber == SPRITE_KNOCKED):
                        self.animationNumber = SPRITE_IDLE
                    speedX = 0

                #Platfmorms we are colliding with
                platforms_collided = pygame.sprite.spritecollide(self, platformGroup, False)

                # if we are falling we use the gravity
                if self.animationNumber == SPRITE_JUMPING:
                    if self.gravity == True:
                        speedY += GRAVITY * time
                    else:
                        speedY = 0.02
                    (speedX, speedY) = self.check_collisions_with_floor_ceiling(platforms_collided, (speedX, speedY), time)

                (speedX, speedY) = self.check_collisions_with_wall(platforms_collided, (speedX, speedY))
            
            elif self.animationNumber == SPRITE_KNOCKED and ((now - self.lastHit) < CHAR_KNOCK):
                platforms_collided = pygame.sprite.spritecollide(self, platformGroup, False)
                (speedX, speedY) = self.check_collisions_with_floor_ceiling(
                    platforms_collided, (speedX, speedY), time)
                (speedX, speedY) = self.check_collisions_with_wall(
                    platforms_collided, (speedX, speedY))

            #Update the image
            self.updatePosture()
            
            #Update speed
            self.speed = (speedX, speedY)
            
            #Calling the parent class to update the Sprite position with time and speed
            MySprite.update(self, time)

            return

    def check_collisions_with_floor_ceiling(self, platforms_collided, speed, tiempo):
        (speedX, speedY) = speed
        floor_collision = False
        for platform in platforms_collided:
            if (speedY > 0) and (platform.rect.bottom > self.rect.bottom) \
                    and platform.rect.left < self.rect.centerx < platform.rect.right:
                floor_collision = True
                self.setPosition(
                    (self.position[0], 
                    platform.position[1] - platform.rect.height + 1))

                self.animationNumber = SPRITE_IDLE

                speedY = 0
                self.isJumping = False
                self.isKnocked = False

            elif (speedY < 0) and (platform.rect.bottom < self.rect.bottom) \
                    and platform.rect.left < self.rect.centerx < platform.rect.right:
                """self.setPosition(
                    (self.position[0], 
                    platform.position[1] + platform.rect.height))"""
                speedY = 0
        
        if not floor_collision:
            if self.animationNumber == SPRITE_JUMPING:
                if self.gravity == True:
                    speedY += GRAVITY * tiempo
            else:
                if self.gravity == True:
                    speedY += GRAVITY * tiempo

        return (speedX, speedY)

    def check_collisions_with_wall(self, platforms_collided, speed):
        (speedX, speedY) = speed
        for platform in platforms_collided:
            if platform.rect.top < self.rect.centery < platform.rect.bottom:

                if platform.rect.centerx > self.rect.centerx:
                    self.setPosition(
                        (platform.position[0] - self.rect.width,
                        self.position[1]))
                else:
                    self.setPosition(
                        (platform.position[0] + platform.rect.width,
                        self.position[1]))
                
                speedX = 0
                break

        return (speedX, speedY)

class MeleePlayer(Character):

    def __init__(self, initialWeapon):
        self.weapon = initialWeapon
        self.orbs_picked = False
        self.damage = 7.5
        Character.__init__(self, 'main2.1.png', 'Coordenadas_inkemba.txt', [4,6,10,11,6,5,5,5], CHAR_SPEED, CHAR_JUMP_SPEED, CHAR_ANIMATION_DELAY, PLAYER_HP)
        self.steps = ResourceManager.LoadSound("steps.wav")
        self.knockback = ResourceManager.LoadSound("knockback.wav")

    def move(self, control):
        #Moving character
        now = pygame.time.get_ticks()
        if control.jump():        
            Character.move(self, UP)
        elif control.left():
            Character.move(self, LEFT)
        elif control.right():
            Character.move(self, RIGHT)
        elif control.isAttacking():
            Character.move(self, ATTACKING)
        else:
            Character.move(self, IDLE)

    def attack(self, dynamicSpritesGroup, spritesGroup, scrollX):
        Character.move(self, ATTACKING)
        self.weapon.shoot(self,scrollX, dynamicSpritesGroup, spritesGroup, self.damage)

    def update(self, platformGroup, enemyGroup, time):

        enemy = pygame.sprite.spritecollideany(self, enemyGroup)        
        now = pygame.time.get_ticks()

        if enemy is not None:
            if enemy.alive == False:
                self.orbs_picked = True
                enemy.orbsound.set_volume(0.2)
                enemy.orbsound.play()
                enemy.kill()
            elif now - self.lastHit >= self.cooldownHit:
                self.lastHit = now
                self.hp -= enemy.dmg
                self.knockback.set_volume(0.2)
                self.knockback.play()
                Character.move(self, HURT)
        Character.update(self, platformGroup, enemyGroup, time)


class RangedPlayer(Character):

    def __init__(self, initialWeapon):
        self.weapon = initialWeapon
        self.orbs_picked = False
        self.damage = 5
        Character.__init__(self, 'Ranged_sheet.png', 'Coordenadas_Lukarc.txt', [2,8,10,11,2,1,1,1], CHAR_SPEED, CHAR_JUMP_SPEED, CHAR_ANIMATION_DELAY, PLAYER_HP)
        self.knockback = ResourceManager.LoadSound("knockback.wav")

    def move(self, control):
        #Moving character
        if control.jump():        
            Character.move(self, UP)
        elif control.left():
            Character.move(self, LEFT)
        elif control.right():
            Character.move(self, RIGHT)
        elif control.isAttacking():
            Character.move(self, ATTACKING)
        else:
            Character.move(self, IDLE)
    
    def attack(self, dynamicSpritesGroup, spritesGroup, scrollX):
        Character.move(self, ATTACKING)
        self.weapon.shoot(self,scrollX, dynamicSpritesGroup, spritesGroup, self.damage)

    def update(self, platformGroup, enemyGroup, time):
        #COMPROBAMOS si hacemos una colision

        #Colision with enemy
        enemy = pygame.sprite.spritecollideany(self, enemyGroup)        
        now = pygame.time.get_ticks()

        if enemy is not None:
            if enemy.alive == False:
                self.orbs_picked = True
                enemy.orbsound.set_volume(0.2)
                enemy.orbsound.play()
                enemy.kill()
            elif now - self.lastHit >= self.cooldownHit:
                self.lastHit = now
                self.hp -= enemy.dmg
                self.knockback.set_volume(0.2)
                self.knockback.play()
                Character.move(self, HURT)

        if (self.weapon.quiver <= 0) and ( (now - self.weapon.lastArrow) >= self.weapon.reloadSpeed):
            self.weapon.quiver = self.weapon.maxArrow
        Character.update(self, platformGroup, enemyGroup, time)

#Class NPC
class NPC(Character):
    "Non playable characters"

    def __init__(self, imageFile, coordFile, numImages, speed, jumpSpeed, animationDelay, hp):
        #Parent class calling
        Character.__init__(self, imageFile, coordFile, numImages, speed, jumpSpeed, animationDelay, hp)

    #This method implements the AI movement
    #This is implemented by each enemy in particular
    def move_cpu(self, player):
        return


#Enemy class. All enemies will use this class
class Enemy(NPC):

    def __init__(self, image, coords, numImages, enemy_speed=0.04, enemy_jump_speed=0.05, enemy_animation_speed_delay=5, hp=10, dmg=1):
        #Parent class calling with the configuration of this enemy
        NPC.__init__(self, image, coords, numImages, enemy_speed, enemy_jump_speed, enemy_animation_speed_delay, hp)

        self.dmg = dmg
        self.alive = True

    def get_orb_position(self):
        return self.orb_position

    #Implementation of AI. Enemies will follow any player.
    def move_cpu(self, player):
        #Only visible enemies will move
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            #Enemy moves towards the player
            if player.position[0] - 7 < self.position[0]:
                Character.move(self, LEFT)
            else:
                Character.move(self, RIGHT)
            
        if self.alive == False:
            Character.move(self, DIE)

    
#Class Skeleton
class Skeleton(Enemy):
    def __init__(self):
        Enemy.__init__(self, 'Skeleton enemy.png', 'Coordenadas_skeleton.txt', [1, 13, 12, 4, 3, 1, 1, 1], hp=15)
        self.hurt = ResourceManager.LoadSound("hurtenemy.wav")
        self.orbsound = ResourceManager.LoadSound("orb.wav")

#Class Golem
class Golem(Enemy):
    #def __init__(self, initialOrb):
    def __init__(self, initialWeaponEnemy, playerSpriteGroup, spritesGroup, scrollX):
        Enemy.__init__(self, 'Old_Golem_walk.png', 'Coordenadas_golem.txt', 
                [1, 8, 1, 1, 1, 1, 1, 1], enemy_speed=0.02, enemy_jump_speed=0.01, 
                enemy_animation_speed_delay=6, hp=30, dmg=10)
        self.hurt = ResourceManager.LoadSound("hurtenemy.wav")
        self.orbsound = ResourceManager.LoadSound("orb.wav")
        
        self.weapon = initialWeaponEnemy
        self.playerSpriteGroup = playerSpriteGroup
        self.spritesGroup = spritesGroup
        self.scrollX = scrollX
        self.damage = 10
        self.looking = RIGHT

        self.jumper = True

    def attack(self, playerSpriteGroup, spritesGroup, scrollX):
        Character.move(self, ATTACKING)
        self.weapon.shoot(self,scrollX, playerSpriteGroup, spritesGroup, self.damage)

    def move_cpu(self, player):
        #Only visible enemies will move
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            #Enemy moves towards the player
            if player.position[0] - 7 < self.position[0]:
                Character.move(self, LEFT)
            else:
                Character.move(self, RIGHT)
        if (self.weapon.quiver > 0 and self.alive == True):
            self.attack(self.playerSpriteGroup, self.spritesGroup, self.scrollX)
            
        if self.alive == False:
            Character.move(self, DIE)
    
    def update(self, platformGroup, enemyGroup, time):
        now = pygame.time.get_ticks()
        
        if (self.weapon.quiver == 0) and ( (now - self.weapon.lastBullet) >= self.weapon.reloadSpeed):
            self.weapon.quiver = self.weapon.maxArrow
        Character.update(self, platformGroup, enemyGroup, time)

class Guardian(Enemy):
    def __init__(self):
        Enemy.__init__(self, 'Old_Guardian_walk.png', 'Coordenadas_guardian.txt', 
                [1, 6, 1, 1, 1, 1, 1, 1], enemy_speed=0.01, enemy_jump_speed=0.01, 
                enemy_animation_speed_delay=25, hp=300, dmg=10)
        self.hurt = ResourceManager.LoadSound("hurtenemy.wav")
        self.orbsound = ResourceManager.LoadSound("orb.wav")

#class hound
class Hound(Enemy):
    def __init__(self):
        Enemy.__init__(self, 'hell-hound-run.png', 'Coordenadas_dog.txt', [1, 5, 1, 1, 1, 1, 1, 1], hp = 7, enemy_speed=0.13)
        self.bark = ResourceManager.LoadSound("bark.wav")
        self.hurt = ResourceManager.LoadSound("hurtenemy.wav")
        self.orbsound = ResourceManager.LoadSound("orb.wav")

class Spectre(Enemy):
    def __init__(self):
        Enemy.__init__(self, 'Soul_move.png', 'Coordenadas_spectre.txt', [8, 8, 8, 8, 8, 8, 8, 8], hp = 7)
        self.hurt = ResourceManager.LoadSound("hurtenemy.wav")
        self.orbsound = ResourceManager.LoadSound("orb.wav")
        self.soul = ResourceManager.LoadSound("soul.wav")
        self.gravity = False

class Sprout(Enemy):
    def __init__(self, initialWeaponEnemy, playerSpriteGroup, spritesGroup, scrollX):
        Enemy.__init__(self, 'Sprout_idle.png', 'Coordenadas_sprout.txt', [4, 4, 4, 4, 4, 4, 4, 4], hp = 7, enemy_speed = 0.01, enemy_jump_speed=0.08)
        self.hurt = ResourceManager.LoadSound("hurtenemy.wav")
        self.orbsound = ResourceManager.LoadSound("orb.wav")
        self.weapon = initialWeaponEnemy
        self.playerSpriteGroup = playerSpriteGroup
        self.spritesGroup = spritesGroup
        self.scrollX = scrollX
        self.damage = 1
        self.looking = RIGHT

        self.jumper = True

    def attack(self, playerSpriteGroup, spritesGroup, scrollX):
        Character.move(self, ATTACKING)
        self.weapon.shoot(self,scrollX, playerSpriteGroup, spritesGroup, self.damage)

    def move_cpu(self, player):
        #Only visible enemies will move
        if self.rect.left > 0 and self.rect.right < ANCHO_PANTALLA and self.rect.bottom > 0 and self.rect.top < ALTO_PANTALLA:
            #Enemy moves towards the player
            if player.position[0] - 7 < self.position[0]:
                Character.move(self, LEFT)
            else:
                Character.move(self, RIGHT)
        if (self.weapon.quiver > 0 and self.alive == True):
            self.attack(self.playerSpriteGroup, self.spritesGroup, self.scrollX)
            
        if self.alive == False:
            Character.move(self, DIE)
    
    def update(self, platformGroup, enemyGroup, time):
        now = pygame.time.get_ticks()
        
        if (self.weapon.quiver == 0) and ( (now - self.weapon.lastArrow) >= self.weapon.reloadSpeed):
            self.weapon.quiver = self.weapon.maxArrow
        Character.update(self, platformGroup, enemyGroup, time)
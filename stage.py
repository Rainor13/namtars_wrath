import pygame
import scene
from scene import *
from pygame.locals import *
from resourceManager import ResourceManager
from control import *
from utilities import *
from menu import *
import os
from characters import *
import random



#Constant variables like screen width and height

#Borders to scroll
MIN_X_PLAYER = (ANCHO_PANTALLA / 2) - PLAYER_SIZE
MAX_X_PLAYER = ANCHO_PANTALLA - MIN_X_PLAYER

#Mechs
LUMINOSITY_DECREASE_PER_ENEMY = 10
LIFE_MAGNITUDE = 3

#SPAWNS 1 y 4
SPAWN_1 = (530, 590) # encima de plataforma con pared
SPAWN_2 = (30, 730) #suelo principio del mapa
SPAWN_3 = (1000, 730) #suelo en medio del mapa
SPAWN_4 = (1300, 600) #Derecha encima de platform
SPAWN_5 = (600, 730) #suelo medio derecha mapa

SPAWN_6 = (10, 590)
SPAWN_7 = (400, 550)

SPAWN_8 = (60, 100)#aire

#SPAWNS STAGE 2
SPAWN2_1 = (1536, 288) # encima de plataforma mas alta
SPAWN2_2 = (1248, 384) # plataforma izquierda de mas alta
SPAWN2_3 = (1792, 480) # plataforma más a la derecha
SPAWN2_4 = (1888, 730) # suelo más a la derecha
SPAWN2_5 = (928, 160) # aire medio
SPAWN2_6 = (1856, 160) # aire izquierda
SPAWN2_7 = (1120, 730) # suelo medio
SPAWN2_8 = (1000, 730) # suelo medio 2
SPAWN2_9 = (1184, 640) # arbol

#SPAWNS STAGE 3
SPAWN3_1 = (32, 544) # suelo izquierda
SPAWN3_2 = (1152, 544) # suelo derecha
SPAWN3_3 = (288, 416) # plataforma izquierda
SPAWN3_4 = (800, 448) # plataforma derecha
SPAWN3_5 = (192, 128) # aire izquierda
SPAWN3_6 = (960, 192) # aire derecha
SPAWN3_7 = (832, 544) # suelo derecha, izquierda de monticulo

#Class Stage
class Stage(Scene):
    
    def __init__(self, director, num_levels, char):
        #num_level is the level number, it will load a config file
        #for each level in the game

        #Parent constructor method
        Scene.__init__(self, director)

        #Level config file loading
        file = 'level_' + str(num_levels) + '.tmx'
        config = ResourceManager.LoadConfigFile('Stages', file)

        #Background image
        try:
            background_payer = config.get_layer_by_name('background')
        except ValueError:
            raise ReferenceError("Background layer not found.")

        background_img = os.path.basename(background_payer.source)
        self.scenary = Scenary(background_img)


        #Platform layer
        try:
            platform_layer = config.get_layer_by_name('platforms')
        except ValueError:
            raise ReferenceError("Platform layer not found.")
        
        self.platformGroup = pygame.sprite.Group()
        for tile in platform_layer.tiles():
            x = tile[0]
            y = tile[1]
            tile_img = os.path.basename(tile[2][0])
            tile_coords = tile[2][1]

            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, tile_coords[2], tile_coords[3])

            #Image fragment to paint
            subimage_rectangle = pygame.Rect(tile_coords[0],tile_coords[1], tile_coords[2], tile_coords[3])

            platform = Platform(tile_img, rect, subimage_rectangle)
            self.platformGroup.add(platform)


        # What we see in the screen
        self.scrollX = 0
        #We only have horizontal scroll, so it's self.scrollX instead of self.scroll = (0,0)
        
        #music
        #Player sprite creation
        if char == 1:
            self.player = MeleePlayer(Sword())
        elif char == 2:
            self.player = RangedPlayer(Bow())
            if self.director.game_level == 1:
                self.player.damage = 5
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/Sounds/1.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            elif self.director.game_level == 2:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/Sounds/2.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                self.player.hp = self.player.hp * 2
            elif self.director.game_level == 3:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/Sounds/3.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                self.player.hp = self.player.hp * 2
                self.player.damage = 10
            elif self.director.game_level == 4:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/Sounds/4.wav")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
                self.player.hp = self.player.hp * 2
                self.player.damage = 10
                

        #We spawn the player in the initial position
        try:
            player_layer = config.get_layer_by_name('character')
            tile = next(player_layer.tiles())
        except StopIteration:
            raise ReferenceError("Player's sprite not found.")
        except ValueError:
            raise ReferenceError("Player's sprite not found.")

        x = tile[0]
        y = tile[1]
        self.player.setPosition((x * TILE_SIZE, y * TILE_SIZE))

        #Group for the range player
        self.shootsGroup = pygame.sprite.Group()

        #Group for enemies in the level
        self.enemyGroup = pygame.sprite.Group()
        if num_levels != 4:
            try:
                enemy_layer = config.get_layer_by_name('enemies')
            except ValueError:
                raise ReferenceError("Enemies layer not found.")
            
            for tile in enemy_layer.tiles():
                    x = tile[0]
                    y = tile[1]
                    enemy_name = os.path.basename(tile[2][0])
                    enemy = self.__get_enemy(enemy_name)
                    enemy.setPosition((x * TILE_SIZE, y * TILE_SIZE))
                    self.enemyGroup.add(enemy)


        if num_levels == 4:
            try:
                boss_layer = config.get_layer_by_name('boss')

                tile = next(boss_layer.tiles())
            except StopIteration:
                raise ReferenceError("Boss layer not found.")

            except ValueError:
                raise ReferenceError("Boss layer not found.")
            x = tile[0]
            y = tile[1]
            boss_name = os.path.basename(tile[2][0])
            self.boss = self.__get_enemy(boss_name)
            self.boss.setPosition((x * TILE_SIZE, y * TILE_SIZE))
            self.enemyGroup.add(self.boss)

        #Dynamic group creation for Player, Enemy and proyectiles
        self.dynamicSpritesGroup = pygame.sprite.Group(self.player, self.enemyGroup.sprites())

        #Group with all sprites
        self.spriteGroup = pygame.sprite.Group(self.player, self.enemyGroup.sprites(),
                            self.platformGroup.sprites())
                            
        self.playerGroup = pygame.sprite.Group(self.player)
        
        #Player controls
        self.control = ControlKeyboard()

        #Hud creation
        if self.director.game_level == 4:
            self.hud = Hud(self.player.hp, 300)
        else:
            self.hud = Hud(self.player.hp, 100)
        self.counter = 1
        self.global_counter = 1
        self.hud.stage = self.director.game_level

        #Event controller
        self.spawn_controller = 0

        self.playmusic2 = False


    def spawn_enemy(self, x, y, scroll, t_enemy):
        if (t_enemy == 'skeleton'):
            enemy = self.__get_enemy('32x32_enemy.png')
        elif (t_enemy == 'golem'):
            enemy = self.__get_enemy('golem.png')
        elif (t_enemy == 'hound'):
            enemy = self.__get_enemy('hound')
        elif (t_enemy == 'spectre'):
            enemy = self.__get_enemy('spectre')
        elif (t_enemy == 'sprout'):
            enemy = self.__get_enemy('sprout')
        
        enemy.setPosition((x,y))
        enemy.setScreenPosition((scroll, 0))
        self.enemyGroup.add(enemy)
        self.dynamicSpritesGroup.add(enemy)
        self.spriteGroup.add(enemy)

    def __get_enemy(self, name):
        #Returns the enemy desired by name
        enemy = None
        if name == '32x32_enemy.png':
            enemy = Skeleton()
        if name == 'golem.png':
            enemy = Golem(FireballSpell(self.playerGroup), self.dynamicSpritesGroup, self.spriteGroup, self.scrollX)
        if name == 'guardian.png':
            enemy = Guardian()
        if name == 'hound': 
            enemy = Hound()
            enemy.bark.set_volume(0.2)
            enemy.bark.play()
        if name == 'spectre': 
            enemy = Spectre()
            enemy.soul.set_volume(0.2)
            enemy.soul.play()
        if name == 'sprout':
            enemy = Sprout(SpikeSpell(self.playerGroup), self.dynamicSpritesGroup, self.spriteGroup, self.scrollX)

        return enemy


    def updateOrderedScroll(self, player):

        #Check if the player is outside left border
        if (player.rect.left < MIN_X_PLAYER):
            offSet = MIN_X_PLAYER - player.rect.left

            #If we are on the left border we can't move the scroll
            if self.scrollX <= 0:
                self.scrollX = 0

                #Check if the player is on the window limit, if he does we don't move the player
                if (player.rect.left <= 0):
                    player.setPosition((0, player.position[1]))

                return False #Scroll didn't update

            #If you can scroll to the left side
            else:
                #New scroll: last - offSet
                self.scrollX = self.scrollX - offSet
                return True #Scroll changed

        #Check if player is outside right border
        elif (player.rect.right > MAX_X_PLAYER):
            #Check how many pixels outside the border the player is
            offSet = player.rect.right  - MAX_X_PLAYER

            #If the scene is on the right border we don't move it
            if (self.scrollX + ANCHO_PANTALLA >= self.scenary.rect.right):
                self.scrollX = self.scenary.rect.right - ANCHO_PANTALLA

                if (player.rect.right >= ANCHO_PANTALLA):
                    player.setPosition((self.scrollX + ANCHO_PANTALLA - PLAYER_SIZE, player.position[1]))

                return False #Scroll not updated

            #If you can scroll 
            else:
                #New scroll value
                self.scrollX = self.scrollX + offSet
                return True #Scroll updated


    def updateScroll(self, player):

        scrollState = self.updateOrderedScroll(player)

        if scrollState:
            for sprite in iter(self.spriteGroup):
                sprite.setScreenPosition((self.scrollX, 0))

            self.scenary.update(self.scrollX)

    
    def eventHandler(self, lum):
        self.global_counter += 1
        if self.global_counter == 1000:
            self.spawn_enemy(SPAWN_1[0], SPAWN_1[1], self.scrollX, 'skeleton')
            self.global_counter = 0
        if (lum == 10 and self.spawn_controller == 0):
            self.spawn_controller += 1
            self.spawn_enemy(SPAWN_1[0], SPAWN_1[1], self.scrollX, 'skeleton')
        if (lum == 15 and self.spawn_controller>=1 and self.spawn_controller<3):
            self.spawn_controller += 2
            self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN_3[0], SPAWN_3[1], self.scrollX, 'skeleton')
        if (lum >= 25 and self.spawn_controller<12):
            self.counter += 1
            if (self.counter==250):
                self.counter = 0
                self.spawn_controller += 1
                spawn = random.choice([SPAWN_1, SPAWN_2, SPAWN_3, SPAWN_4])
                self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'skeleton')
        if (lum == 70 and self.spawn_controller == 12):
            self.spawn_controller += 1
            self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'hound')
        if (lum >= 75 and lum <100):
            if (self.spawn_controller == 13):
                self.spawn_controller += 2
                self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'hound')
                self.spawn_enemy(SPAWN_5[0], SPAWN_5[1], self.scrollX, 'hound')
            else:
                self.counter += 1
                if (self.counter==100):
                    self.counter = 0
                    self.spawn_controller += 1
                    spawn = random.choice([SPAWN_1, SPAWN_2, SPAWN_3, SPAWN_4, SPAWN_5, SPAWN_6, SPAWN_7])
                    self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'skeleton')
        if (lum == 100):
            self.director.exitScene()
            self.director.stackScene(LevelCompletedMenu(self.director))

    def eventHandler_2(self, lum):
        self.global_counter += 1
        if self.global_counter == 1000:
            self.spawn_enemy(SPAWN2_9[0], SPAWN2_9[1], self.scrollX, 'skeleton')
            self.global_counter = 0
        if (lum >= 15 and self.spawn_controller == 0):
            self.spawn_controller += 3
            self.spawn_enemy(SPAWN2_1[0], SPAWN2_1[1], self.scrollX, 'hound')
            self.spawn_enemy(SPAWN2_2[0], SPAWN2_2[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN2_3[0], SPAWN2_3[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN2_9[0], SPAWN2_9[1], self.scrollX, 'sprout')
        if (lum >= 35 and self.spawn_controller <= 3):
            self.spawn_controller += 1
            self.spawn_enemy(SPAWN2_4[0], SPAWN2_4[1], self.scrollX, 'skeleton')
        if (lum >= 40 and self.spawn_controller <= 4):
            self.spawn_controller += 5
            self.spawn_enemy(SPAWN2_5[0], SPAWN2_5[1], self.scrollX, 'spectre')
            self.spawn_enemy(SPAWN2_6[0], SPAWN2_6[1], self.scrollX, 'spectre')
            self.spawn_enemy(SPAWN2_7[0], SPAWN2_7[1], self.scrollX, 'hound')
            self.spawn_enemy(SPAWN2_2[0], SPAWN2_2[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN2_3[0], SPAWN2_3[1], self.scrollX, 'skeleton')
            self.counter = 0
        if (lum == 65 and self.spawn_controller == 9):
            self.spawn_controller += 1
            self.spawn_enemy(SPAWN2_8[0], SPAWN2_8[1], self.scrollX, 'golem')
        if (lum >= 65 and self.spawn_controller > 9 and self.spawn_controller <= 35):
            self.counter += 1
            if self.counter == 150:
                self.spawn_controller += 1
                self.spawn_enemy(SPAWN2_4[0], SPAWN2_4[1], self.scrollX, 'hound')
            if self.counter == 200:
                self.spawn_controller += 1
                self.spawn_enemy(SPAWN2_5[0], SPAWN2_5[1], self.scrollX, 'spectre')
            if self.counter == 300:
                self.spawn_controller += 1
                self.counter = 0
                spawn = random.choice([SPAWN2_1, SPAWN2_2, SPAWN2_3, SPAWN2_4])
                self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'skeleton')
        if (lum == 100):
            self.director.exitScene()
            self.director.stackScene(LevelCompletedMenu(self.director))

    def eventHandler_3(self, lum):
        self.global_counter +=1
        if self.global_counter == 1000:
            self.spawn_enemy(SPAWN3_7[0], SPAWN3_7[1], self.scrollX, 'hound')
            self.global_counter = 0
        if (lum == 0 and self.spawn_controller == 0):
            self.spawn_controller += 1
            self.spawn_enemy(SPAWN3_5[0], SPAWN3_5[1], self.scrollX, 'spectre')
            self.spawn_enemy(SPAWN3_6[0], SPAWN3_6[1], self.scrollX, 'spectre')
            self.spawn_enemy(SPAWN3_7[0], SPAWN3_7[1], self.scrollX, 'hound')
            self.spawn_enemy(SPAWN3_4[0], SPAWN3_4[1], self.scrollX, 'sprout')
        if (lum >= 20 and lum <= 75):
            if (self.spawn_controller == 1):
                self.spawn_controller += 1
                self.spawn_enemy(SPAWN3_3[0], SPAWN3_3[1], self.scrollX, 'sprout')
                self.spawn_enemy(SPAWN3_1[0], SPAWN3_1[1], self.scrollX, 'skeleton')
            if (self.spawn_controller >= 2 and self.spawn_controller <= 7):
                self.counter += 1
                if (self.counter == 75):
                    self.spawn_controller += 1
                    self.spawn_enemy(SPAWN3_1[0], SPAWN3_1[1], self.scrollX, 'skeleton')
                    self.spawn_enemy(SPAWN3_7[0], SPAWN3_7[1], self.scrollX, 'skeleton')
                if (self.counter == 125):
                    self.spawn_controller += 1
                    self.counter = 0
                    self.spawn_enemy(SPAWN3_6[0], SPAWN3_6[1], self.scrollX, 'spectre')
        if (lum >= 75):
            enemigo_tierra = random.choice(['skeleton', 'hound', 'sprout'])
            spawn_tierra = random.choice([SPAWN3_1, SPAWN3_7, SPAWN3_2, SPAWN3_3, SPAWN3_4])
            spawn_aire = random.choice([SPAWN3_5, SPAWN3_6])

            if (self.spawn_controller == 8):
                self.spawn_controller += 1
                self.spawn_enemy(SPAWN3_3[0], SPAWN3_3[1], self.scrollX, 'sprout')
            if (self.spawn_controller >= 9):
                self.counter += 1
                if (self.counter == 75):
                    self.spawn_enemy(spawn_tierra[0], spawn_tierra[1], self.scrollX, enemigo_tierra)
                if (self.counter == 125):
                    self.counter = 0
                    self.spawn_enemy(spawn_aire[0], spawn_aire[1], self.scrollX, 'spectre')
        if (lum >= 100):
            self.director.exitScene()
            self.director.stackScene(LevelCompletedMenu(self.director))

    def eventHandler_4(self, lum):
        if (lum >= 5 and self.spawn_controller == 0):
            self.spawn_controller += 3
            self.spawn_enemy(SPAWN_3[0], SPAWN_3[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN_1[0], SPAWN_1[1], self.scrollX, 'hound')
            self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'hound')
        if (lum >= 20 and self.spawn_controller >= 3 and self.spawn_controller<5):
            self.spawn_controller += 2
            self.spawn_enemy(SPAWN_3[0], SPAWN_3[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN_5[0], SPAWN_5[1], self.scrollX, 'skeleton')
        if (lum >=35 and self.spawn_controller < 15):
            self.counter += 1
            if self.counter == 100:
                self.counter = 0
                self.spawn_controller += 1
                spawn = random.choice([SPAWN_3, SPAWN_2, SPAWN_5])
                self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'skeleton')
        if (lum >= 66 and self.spawn_controller == 15):
            self.spawn_controller += 2
            self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'skeleton')
            self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'hound')
        if (lum > 75 and lum <100):
            self.counter += 1
            if self.counter == 100:
                self.counter = 0
                self.spawn_controller += 1
                self.spawn_enemy(SPAWN_2[0], SPAWN_2[1], self.scrollX, 'hound')
        if (lum >= 100 and self.spawn_controller <= 40):
            self.counter += 1
            if self.counter == 150:
                self.counter = 0
                self.spawn_controller += 1
                spawn = random.choice([SPAWN_3, SPAWN_2, SPAWN_5])
                self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'skeleton')
        if (lum >= 200):
            self.counter += 1
            if self.counter == 100:
                self.spawn_controller += 1
                spawn = random.choice([SPAWN_3, SPAWN_2, SPAWN_5])
                self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'skeleton')
            if self.counter == 700:
                self.spawn_controller += 1
                spawn = random.choice([SPAWN2_5, SPAWN_8])
                self.spawn_enemy(spawn[0], spawn[1], self.scrollX, 'spectre')
                self.counter = 0
        if (lum >= 300):
            self.director.exitScene()
            self.director.stackScene(GameCompletedMenu(self.director))

    def update(self, time):
        #First of all we move the NPC with the move_cpu method
        for enemy in iter(self.enemyGroup):
            enemy.move_cpu(self.player)

        #Dynamic sprite update, this way seems like all update at the same time
        self.dynamicSpritesGroup.update(self.platformGroup, self.enemyGroup, time)

        if self.player.orbs_picked == True:
            if self.director.game_level == 4:
                self.player.damage += 0.2
                self.player.orbs_picked = False
            else:
                self.hud.luminosity += 5
                self.player.orbs_picked = False

        if not self.player.alive:
            #If we die we exit the scene
            self.director.exitScene()
            self.director.stackScene(GameoverMenu(self.director))

        #game events

        
        #test spawn
        #self.counter += 1
        #if (self.counter == 50):
            #self.counter = 0
            #self.spawn_enemy(SPAWN2_1[0], SPAWN2_1[1], self.scrollX, 'sprout')

        if self.director.game_level == 1:
            self.eventHandler(self.hud.luminosity)
        elif self.director.game_level == 2:
            self.eventHandler_2(self.hud.luminosity)
        elif self.director.game_level == 3:
            self.eventHandler_3(self.hud.luminosity)
        elif self.director.game_level == 4:
            self.eventHandler_4(self.hud.luminosity)

        if self.director.game_level == 4:
            self.hud.luminosity = self.hud.maxLum - self.boss.hp

        #Update scroll
        self.updateScroll(self.player)

        #Update HUD
        self.hud.actualPlayerHp = self.player.hp
        self.hud.update(self.player)

    
    def paint(self, screen):
        #Draw the decoration
        self.scenary.paint(screen)
        #Sprite drawing
        self.spriteGroup.draw(screen)
        #Hud drawing
        self.hud.paint(screen)


    def events(self, event_list):
        #Check if there is any event that exists the game
        for event in event_list:
            #Exit event
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            if event.type == pygame.KEYDOWN:
                self.control.atack(self.player, self.dynamicSpritesGroup, self.spriteGroup, self.scrollX, event)
                #If want to pause the game
                if event.key == pygame.K_p:
                    pause = PauseMenu(self.director)
                    self.director.stackScene(pause)

        #Move action for players
        self.player.move(self.control)



#Platform class
class Platform(MySprite):

    def __init__(self, image, rect, subimage_rectangle = None):
        #Parent constructor method
        MySprite.__init__(self)
        #Rectangle with the coords in the screen
        self.rect = rect
        #Position with those coords
        self.setPosition((self.rect.left, self.rect.top))

        #Load images 
        if image is not None:
            self.image = ResourceManager.LoadImage('Images', image, -1)
            if subimage_rectangle is not None:
                #If the image has many blocks and only want to draw one
                self.image = self.image.subsurface(subimage_rectangle)
        else:
            self.image = pygame.Surface((0, 0))


#Scenary class
class Scenary:

    def __init__(self, image):
        self.image = ResourceManager.LoadImage('Images', image)
                
        self.rect = self.image.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        #Subimage we are looking at
        self.rectSubimage = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimage.left = 0 #Horizontal scroll starts at 0

    def update(self, scrollX):
        self.rectSubimage.left = scrollX

    def paint(self, screen):
        screen.blit(self.image, self.rect, self.rectSubimage)




#HUD class

#TODO Hud class with images and methods
class Hud:

    def __init__(self, fullPlayerHp, lum):
        self.luminosity = 0
        self.maxLum = lum
        self.stage = None
        #Starting luminosity
        font = pygame.font.Font('font1.ttf', 100)
        luminosityText = (str(self.luminosity) + '/' + str(self.maxLum))
        self.text = font.render(luminosityText, True, (75,0,130), None)
        
        self.fullPlayerHp =  fullPlayerHp
        self.actualPlayerHp = fullPlayerHp
        self.hpBar = pygame.Rect(30, 40, 300, 20)



    def update(self, scrollX):
        None

    def paint(self, screen):

        font = pygame.font.Font('font1.ttf', 100)
        luminosityText = (str(round(self.luminosity, 1)) + '/' + str(self.maxLum))
        self.text = font.render(luminosityText, True, (75,0,130), None)
        screen.blit(self.text, pygame.Rect(900, 0, 10, 10))

        hpBarSize = ((100*self.actualPlayerHp) / self.fullPlayerHp) * LIFE_MAGNITUDE
        pygame.draw.rect(screen, (138, 3, 3), pygame.Rect(30, 45, hpBarSize, 30))

        if self.stage >= 2:
            coraza = ResourceManager.LoadImage('Images', 'coraza.png', -1)
            coraza = pygame.transform.scale(coraza, (30, 26))
            screen.blit(coraza, (30, 15))
        if self.stage >= 3:
            guantes = ResourceManager.LoadImage('Images', 'guantes.png', -1)
            guantes = pygame.transform.scale(guantes, (22, 26))
            screen.blit(guantes, (65, 15))
        if self.stage == 4:
            farolillo = ResourceManager.LoadImage('Images', 'farolillo.png', -1)
            farolillo = pygame.transform.scale(farolillo, (12, 30))
            screen.blit(farolillo, (95, 12))
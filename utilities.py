import pygame
from scene import *
from MySprite import *
from resourceManager import ResourceManager


DMG_BOW = 7
QUIVER_BOW = 1
RELOAD_BOW = 500
SPEED_BOW = 0.5

ENEMY_DMG_SPIKE = 7
ENEMY_QUIVER_SPIKE = 1
ENEMY_RELOAD_SPIKE = 2000
ENEMY_SPEED_SPIKE = 0.5

ENEMY_DMG_FIREBALL = 15
ENEMY_QUIVER_FIREBALL = 1
ENEMY_RELOAD_FIREBALL = 2000
ENEMY_SPEED_FIREBALL = 0.5

DMG_SWORD = 15
QUIVER_SWORD = 1
RELOAD_SWORD = 1
SPEED_SWORD = 0.5

class Arrow(MySprite):
    
    #Las coordenadas x e y son para spawnear la bala donde esta el personaje
    #habria que anhadirle hitsound y sonido de salida
    def __init__(self, player, speed, scrollX, damage_level):
        MySprite.__init__(self)
        self.damage_level = damage_level

        #self.image = pygame.image.load(path.join("test", "ally_test.png")).convert()
        self.image = ResourceManager.LoadImage('Images', 'arrow.png', -1)
        self.rect = self.image.get_rect()
        
        self.arrowhit = ResourceManager.LoadSound("arrowimpact.wav")
        self.arrowfail = ResourceManager.LoadSound("failhit.wav")
        self.arrowshoot = ResourceManager.LoadSound("archerywhizz.wav")

        (playerposx, playerposy) = player.position
        if player.looking == RIGHT:
            self.setPosition((playerposx+self.rect.width-20, player.rect.centery+3))
        else:
            self.setPosition((playerposx+self.rect.width+5, player.rect.centery+3))

        self.setScreenPosition((scrollX, 0))

        #We must check if we must flip the sprite
        self.looking = player.looking
        if self.looking == LEFT:
            self.image = pygame.transform.flip(self.image, 1, 0)
            speed = -speed

        #PROBAR
        #Para que tenga caida y vaya mas rapido al salir y vaya frenandose poner mucha velocidad inicial y bajarla aqui += -speed, -ejey
        self.speed = (speed, 0)

    def update(self, platformGroup, enemyGroup, time):

        #la bala desaparece si se sale de la pantalla
        if self.looking == LEFT and self.rect.right < 0:
            self.kill()
        elif self.looking == RIGHT and self.rect.left > ANCHO_PANTALLA:
            self.kill()
        else:
            enemyhited = pygame.sprite.spritecollideany(self, enemyGroup)
            if (enemyhited is not None) and (enemyhited.alive == True) :
                self.arrowhit.set_volume(0.05)
                self.arrowhit.play()
                self.kill()
                enemyhited.hp -= self.damage_level
            elif pygame.sprite.spritecollideany(self, platformGroup):
                self.arrowfail.set_volume(0.1)
                self.arrowfail.play()
                self.kill()
            else:
                MySprite.update(self, time)

class Weapon(MySprite):

    def __init__(self, name, dmg, reloadSpeed, quiver,speed):

        MySprite.__init__(self)

        self.dmg= dmg
        self.arrowSpeed = speed
        self.quiver = quiver
        self.maxArrow = quiver
        self.reloadSpeed = reloadSpeed
        self.lastArrow = pygame.time.get_ticks()
        #self.rect = self.image.get_rect()
    
    def shoot(self, player, scrollX, dynamicSpritesGroup, spritesGroup, dmg):
        
        if (self.quiver > 0):    
            #self.soudn.play()
            #falta el sonido de dar y fallar
            self.quiver -= 1
            arrow = Arrow(player, self.arrowSpeed, scrollX, dmg)
            arrow.arrowshoot.set_volume(0.2)
            arrow.arrowshoot.play()
            dynamicSpritesGroup.add(arrow)
            spritesGroup.add(arrow)
            #no se si hace falta
            self.lastArrow = pygame.time.get_ticks()

    #A LO MEJOR HACE FALTA Y SE PARA ALGO O NO NO SABEMOS xD
    def update(self,player,time):
        MySprite.update(self, time)

class Bow(Weapon):

    def __init__(self, damage = DMG_BOW):
        #self.shootSound = ResourcesManager.LoadSound("handgun.ogg")
        #self.shootSound.set_volume(0.4)
        #self.impactSound = ResourcesManager.LoadSound("hitdefault.ogg")
        #elf.failHit = ResourcesManager.LoadSound("failhit.ogg")
        
        #CONSTRUCTOR ORIGINAL
        #Weapon.__init__(self,'Handgun', 'handgun.png', DMG_HG, RELOAD_HG, MAGAZINE_HG, SPEED_HG)
        Weapon.__init__(self,'Bow', damage, RELOAD_BOW, QUIVER_BOW, SPEED_BOW)


class Meleehit(MySprite):
    
    #Las coordenadas x e y son para spawnear la bala donde esta el personaje
    #habria que anhadirle hef events(self, events_list):itsound y sonido de salida
    def __init__(self, player, speed, scrollX, damage_level):
        MySprite.__init__(self)
        self.damage_level = damage_level

        #self.image = pygame.image.load(path.join("test", "ally_test.png")).convert()
        self.image = pygame.Surface((30,17))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        
        self.meleehitsound = ResourceManager.LoadSound("meelehit.wav")

        (playerposx, playerposy) = player.position
        if player.looking == RIGHT:
            #o 17 en right
            # self.setPosition((playerposx+self.rect.width-11, player.rect.centery+7))
            self.setPosition((playerposx + player.rect.width, player.rect.centery+7))
        else:
            # self.setPosition((playerposx+self.rect.width-62, player.rect.centery+7))
            self.setPosition((playerposx - self.rect.width, player.rect.centery+7))

        self.setScreenPosition((scrollX, 0))

        #We must check if we must flip the sprite
        self.looking = player.looking
        if self.looking == LEFT:
            self.image = pygame.transform.flip(self.image, 1, 0)
            speed = -speed

        self.speed = (0, 0)

    def update(self, platformGroup, enemyGroup, time):

        
        enemyhited = pygame.sprite.spritecollideany(self, enemyGroup)
        
        if enemyhited is not None:
            rect = pygame.sprite.collide_mask(self, enemyhited)
            if rect:
                self.meleehitsound.set_volume(0.2)
                self.meleehitsound.play()
                self.kill()
                enemyhited.hp -= self.damage_level                 
            if pygame.sprite.spritecollideany(self, platformGroup):
                #soundfail.play()
                self.kill()
            else:
                MySprite.update(self, time)
        else:
            self.kill()

class Sword(Weapon):

    def __init__(self, damage = DMG_SWORD):
        
        Weapon.__init__(self,'Sword', damage, RELOAD_SWORD, QUIVER_SWORD, SPEED_SWORD)

    def shoot(self, player, scrollX, dynamicSpritesGroup, spritesGroup, dmg):
        
        meleehit = Meleehit(player, self.arrowSpeed, scrollX, dmg)
        dynamicSpritesGroup.add(meleehit)
        spritesGroup.add(meleehit)

        self.lastArrow = pygame.time.get_ticks()

    def update(self,player,time):
        MySprite.update(self, time)

class Spike(MySprite):
    
    #Las coordenadas x e y son para spawnear la bala donde esta el personaje
    #habria que anhadirle hitsound y sonido de salida
    def __init__(self, enemy, speed, scrollX, damage_level, playerGroup):
        MySprite.__init__(self)
        self.damage_level = damage_level

        self.playerGroup = playerGroup
        self.image = ResourceManager.LoadImage('Images', 'sprout_hit.png', -1)
        self.rect = self.image.get_rect()
        
        self.spikehit = ResourceManager.LoadSound("stonehit.wav")
        self.spikefail = ResourceManager.LoadSound("stonefail.wav")
        self.spikeshoot = ResourceManager.LoadSound("archerywhizz.wav")

        (enemyposx, enemyposy) = enemy.position
        if enemy.looking == RIGHT:
            self.setPosition((enemyposx+self.rect.width-20, enemy.rect.centery+3))
        else:
            self.setPosition((enemyposx+self.rect.width+5, enemy.rect.centery+3))

        self.setScreenPosition((scrollX, 0))

        #We must check if we must flip the sprite
        self.looking = enemy.looking
        if self.looking == LEFT:
            self.image = pygame.transform.flip(self.image, 1, 0)
            speed = -speed

        #Para que tenga caida y vaya mas rapido al salir y vaya frenandose poner mucha velocidad inicial y bajarla aqui += -speed, -ejey
        self.speed = (speed, 0)

    def update(self, platformGroup, enemyGroup, time):

        #la bala desaparece si se sale de la pantalla
        if self.looking == LEFT and self.rect.right < 0:
            self.kill()
        elif self.looking == RIGHT and self.rect.left > ANCHO_PANTALLA:
            self.kill()
        else:
            enemyhited = pygame.sprite.spritecollideany(self, self.playerGroup)
            if enemyhited is not None:
                self.spikehit.set_volume(0.1)
                self.spikehit.play()
                self.kill()
                enemyhited.hp -= self.damage_level
            elif pygame.sprite.spritecollideany(self, platformGroup):
                self.spikefail.set_volume(0.2)
                self.spikefail.play()
                self.kill()
            else:
                MySprite.update(self, time)

class WeaponEnemy(MySprite):

    def __init__(self, name, dmg, reloadSpeed, quiver,speed, playerGroup):

        MySprite.__init__(self)

        self.playerGroup = playerGroup
        self.dmg= dmg
        self.spikeSpeed = speed
        self.quiver = quiver
        self.maxArrow = quiver
        self.reloadSpeed = reloadSpeed
        self.lastArrow = pygame.time.get_ticks()
    
    def shoot(self, enemy, scrollX, dynamicSpritesGroup, spritesGroup, dmg):
        
        if (self.quiver > 0):    
            self.quiver -= 1
            spike = Spike(enemy, self.spikeSpeed, scrollX, dmg, self.playerGroup)
            spike.spikeshoot.set_volume(0.3)
            spike.spikeshoot.play()
            dynamicSpritesGroup.add(spike)
            spritesGroup.add(spike)

            self.lastArrow = pygame.time.get_ticks()

    def update(self,enemy,time):
        MySprite.update(self, time)

class SpikeSpell(WeaponEnemy):

    def __init__(self, playerGroup, damage = ENEMY_DMG_SPIKE):

        WeaponEnemy.__init__(self,'Spike', damage, ENEMY_RELOAD_SPIKE, ENEMY_QUIVER_SPIKE, ENEMY_SPEED_SPIKE, playerGroup)

class Fireball(MySprite):
    
    #Las coordenadas x e y son para spawnear la bala donde esta el personaje
    #habria que anhadirle hitsound y sonido de salida
    def __init__(self, enemy, speed, scrollX, damage_level, playerGroup):
        MySprite.__init__(self)
        self.damage_level = damage_level

        self.playerGroup = playerGroup
        self.image = ResourceManager.LoadImage('Images', 'golem_hit.png', -1)
        self.rect = self.image.get_rect()
        
        self.fireballhit = ResourceManager.LoadSound("fireball_hit.wav")
        self.fireballfail = ResourceManager.LoadSound("fireball_hit.wav")
        self.fireballshoot = ResourceManager.LoadSound("fireball_launch.wav")

        (enemyposx, enemyposy) = enemy.position
        if enemy.looking == RIGHT:
            self.setPosition((enemyposx+self.rect.width-20, enemy.rect.centery+30))
        else:
            self.setPosition((enemyposx+self.rect.width+5, enemy.rect.centery+30))

        self.setScreenPosition((scrollX, 0))

        #We must check if we must flip the sprite
        self.looking = enemy.looking
        if self.looking == LEFT:
            self.image = pygame.transform.flip(self.image, 1, 0)
            speed = -speed

        #Para que tenga caida y vaya mas rapido al salir y vaya frenandose poner mucha velocidad inicial y bajarla aqui += -speed, -ejey
        self.speed = (speed, 0)

    def update(self, platformGroup, enemyGroup, time):

        #la bala desaparece si se sale de la pantalla
        if self.looking == LEFT and self.rect.right < 0:
            self.kill()
        elif self.looking == RIGHT and self.rect.left > ANCHO_PANTALLA:
            self.kill()
        else:
            enemyhited = pygame.sprite.spritecollideany(self, self.playerGroup)
            if enemyhited is not None:
                self.fireballhit.set_volume(0.1)
                self.fireballhit.play()
                self.kill()
                enemyhited.hp -= self.damage_level
            elif pygame.sprite.spritecollideany(self, platformGroup):
                self.fireballfail.set_volume(0.2)
                self.fireballfail.play()
                self.kill()
            else:
                MySprite.update(self, time)

class GolemWeapon(MySprite):

    def __init__(self, name, dmg, reloadSpeed, quiver,speed, playerGroup):

        MySprite.__init__(self)

        self.playerGroup = playerGroup
        self.dmg= dmg
        self.fireballSpeed = speed
        self.quiver = quiver
        self.maxArrow = quiver
        self.reloadSpeed = reloadSpeed
        self.lastBullet = pygame.time.get_ticks()
    
    def shoot(self, enemy, scrollX, dynamicSpritesGroup, spritesGroup, dmg):
        
        if (self.quiver > 0):    
            self.quiver -= 1
            fireball = Fireball(enemy, self.fireballSpeed, scrollX, dmg, self.playerGroup)
            fireball.fireballshoot.set_volume(0.3)
            fireball.fireballshoot.play()
            dynamicSpritesGroup.add(fireball)
            spritesGroup.add(fireball)
            self.lastBullet = pygame.time.get_ticks()

    def update(self,enemy,time):
        MySprite.update(self, time)

class FireballSpell(GolemWeapon):

    def __init__(self, playerGroup, damage = ENEMY_DMG_FIREBALL):

        GolemWeapon.__init__(self,'Fireball', damage, ENEMY_RELOAD_FIREBALL, ENEMY_QUIVER_FIREBALL, ENEMY_SPEED_FIREBALL, playerGroup)
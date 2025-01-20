import pygame
import sys
from scene import *
from pygame.locals import *
from resourceManager import ResourceManager



class Director():

    def __init__(self):
        #Inizialice the screen in graphic mode
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Namtar's Wrath")
        
        pygame.mixer.music.load("Assets/Sounds/inicio1.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        
        #Scene stack
        self.stack = []

        #Exit flag
        self.exit_scene = False

        #Clock
        self.clock = pygame.time.Clock()

        #Stage we are executing
        self.game_level = 1

        #Char we picked
        self.character = None

        #self.musicInit = ResourceManager.LoadSound("inicio1.wav")
        #self.musicInit.set_volume(0.2)
        #self.musicInit.play()

    def loop(self, scene):

        self.exit_scene = False

        #Removal of events before loop
        pygame.event.clear()

        while not self.exit_scene:
            #60 fps sync
            time = self.clock.tick(60)
            #Events to scene
            scene.events(pygame.event.get())
            #Scene update
            scene.update(time)
            #Screen drawing
            scene.paint(self.screen)
            pygame.display.flip()


    def execute(self):
        
        #While scenes in the stack, keep executing the top one
        while (len(self.stack) > 0):
            #Top scene in the stack
            scene = self.stack[len(self.stack) - 1]
            #Event loop execution until scene is over
            self.loop(scene)

    
    def exitScene(self):
        #Scene flag turn on
        self.exit_scene = True
        #Scene removal
        if (len(self.stack) > 0):
            self.stack.pop()


    def exitProgram(self):
        #Remove all scenes in the stack
        self.stack = []
        self.exit_scene = True


    def changeScene(self, scene):
        self.exitScene()
        #Param scene goes on top
        self.stack.append(scene)

    def stackScene(self, scene):
        self.exit_scene = True
        #New scene goes on top of current scene but current scene does not disappear
        self.stack.append(scene)
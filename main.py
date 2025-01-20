import pygame
from pygame.locals import *
import stage
from stage import *
import director
from director import *
from resourceManager import ResourceManager

if __name__ == '__main__':

	# Inicializar pygame
    pygame.init()


    #Director initialization
    director = Director()

    #Stage initialization
    scene = MainMenu(director)


    #Scene goes on top of the stack
    director.stackScene(scene)
    director.execute()


    pygame.quit()
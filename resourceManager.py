# -*- coding: utf-8 -*-

# IMPORTS

import pygame,sys,os
from pygame.locals import *
from pytmx.pytmx import TiledMap


# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class ResourceManager(object):
    
    resources = {}

    @classmethod
    def LoadImage(cls, path, name, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            current_path = os.path.dirname(__file__) 
            specific_path = os.path.join(current_path, 'Assets', path)
            fullname = os.path.join(specific_path, name)
            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print ('Cannot load image:', fullname)
                raise SystemExit (message)
            image = image.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.resources[name] = image
            # Se devuelve
            return image


    @classmethod
    def LoadCoordsFile(cls,path, name):
        # Si el nombre de archivo está entre los recursos ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            current_path = os.path.dirname(__file__) 
            specific_path = os.path.join(current_path, 'Assets', path)
            fullname = os.path.join(specific_path, name)
            pfile=open(fullname,'r')
            data=pfile.read()
            pfile.close()
            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data

    @classmethod
    def LoadConfigFile(cls, path, name):

        # Si el nombre de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el fichero de configuración indicando la carpeta en la que está
            current_path = os.path.dirname(__file__) 
            specific_path = os.path.join(current_path, 'Assets', path)
            fullname = os.path.join(specific_path, name)
            try:
                data = TiledMap(fullname)
            except:
                print('Cannot load configuration file:', fullname)
                raise SystemExit()

            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data

    @classmethod
    def LoadSound(cls, name):
        # Se carga el recurso indicando el nombre de su carpeta
        current_path = os.path.dirname(__file__)
        fullname_path = os.path.join(current_path, 'Assets', 'Sounds')
        fullname = os.path.join(fullname_path, name)

        # Devolvemos un objeto de la clase Sound
        try:
            sound = pygame.mixer.Sound(fullname)
        except:
            print('Cannot load the sound file:', fullname)
            raise SystemExit()

        return sound
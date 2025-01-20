ALTO_PANTALLA = 793
ANCHO_PANTALLA = 1200
LEVEL_NUMBERS = 1
TILE_SIZE = 32
PLAYER_SIZE = 32


#Abstract class
class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplementedError("It must implement update method.")

    def events(self, *args):
        raise NotImplementedError("It must implement events method.")

    def paint(self, screen):
        raise NotImplementedError("It must implement paint method.")
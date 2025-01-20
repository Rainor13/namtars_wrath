import pygame
from pygame.locals import *
from scene import *
from resourceManager import *
import stage


#Abstract class GUIElement
class GUIElement:
    #Uses the screen and screen rectangle to check if it's been clicked
    def __init__(self, screen, rect):
        self.screen = screen
        self.rect = rect

    #Sets the rect in the screen
    def setPosition(self, position):
        (positionX, positionY) = position
        self.rect.left = positionX
        self.rect.top = positionY

    #Tells us if it's been clicked
    def elementPosition(self, position):
        (positionX, positionY) =  position
        if (positionX >= self.rect.left) and (positionX <= self.rect.right) and \
            (positionY >= self.rect.top) and (positionY <= self.rect.bottom):
            return True
        else:
            return False

    #Abstract methods subclases will implement
    #Paints element in the screen
    def paint(self):
        raise NotImplemented("Must implement paint method.")

    #Action will execute when element is clicked
    def action(self):
        raise NotImplemented("Must implement action method.")


#Static elements in the screen, they don't do anything 
class GUIStaticElement(GUIElement):

    def __init__(self, screen, image, position):
        #Static element image load
        self.image = ResourceManager.LoadImage(image, -1)
        #Parent init method with rect size
        GUIElement.__init__(self, screen, self.image.get_rect())
        #Set the rect in the desired position
        self.setPosition(position)

    def paint(self, screen):
        screen.blit(self.image, self.rect)

    #Static elements don't do anything
    def action(self):
        pass


#Class button and specific buttons
class Button(GUIElement):

    def __init__(self, screen, image, position):
        #Button image load
        self.image = ResourceManager.LoadImage("Images", image, -1)
        #Parent init method with button rect size
        GUIElement.__init__(self, screen, self.image.get_rect())
        #Set the rectangle in the desired position
        self.setPosition(position)

    def paint(self, screen):
        screen.blit(self.image, self.rect)


class PlayButton(Button):
    
    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.showStory()

class ExitButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.exitProgram()

class NextLevelButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.nextLevel()

class ContinueButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.nextScreen()

class MeeleButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.meelePicked()

class RangedButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.rangedPicked()


class ResumeButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.continueGame()


class BackButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.previousScreen()

class TryAgainButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.tryAgain()


class NextLevelButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.nextLevel()

class PlayAgainButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.playAgain()

class CreditsButton(Button):

    def __init__(self, screen, image, position):
        Button.__init__(self, screen, image, position)

    def action(self):
        self.screen.menu.nextScreen()

#GUIScreen and screens in the game
class GUIScreen:

    def __init__(self, menu, image):
        self.menu = menu
        #Background image load
        self.image = ResourceManager.LoadImage("Images", image)
        self.image = pygame.transform.scale(self.image, (ANCHO_PANTALLA, ALTO_PANTALLA))
        #GUI elements list
        self.GUIelements = []


    def events(self, event_list):
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                self.clickElement = None
                for element in self.GUIelements:
                    if element.elementPosition(event.pos):
                        self.clickElement = element
            if event.type == MOUSEBUTTONUP:
                for element in self.GUIelements:
                    if element.elementPosition(event.pos):
                        if element == self.clickElement:
                            element.action()


    def paint(self, screen):
        #Background screen drawing
        screen.blit(self.image, self.image.get_rect())
        #Button drawing
        for element in self.GUIelements:
            element.paint(screen)


class MainScreen(GUIScreen):

    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'main_background.png')
        #Button creation and append to the element list
        playButton = PlayButton(self, 'play.png', (477, 390))
        exitButton = ExitButton(self, 'exit.png', (532, 500))
        self.GUIelements.append(playButton)
        self.GUIelements.append(exitButton)


class StoryScreen(GUIScreen):

    def __init__(self, menu, story_num):
        filename = 'story' + str(story_num) + '.png'
        GUIScreen.__init__(self, menu, filename)
        backButton = BackButton(self, 'back.png', (730, 540))
        continueButton = ContinueButton(self, 'continue.png', (850, 532))
        self.GUIelements.append(backButton)
        self.GUIelements.append(continueButton)


class StoryScreen1(StoryScreen):
    
    def __init__(self, menu):
        StoryScreen.__init__(self, menu, 1)

class StoryScreen2(StoryScreen):
    
    def __init__(self, menu):
        StoryScreen.__init__(self, menu, 2)


class ControlsScreen(GUIScreen):

    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'controls_screen.png')
        #Button creation and append to the element list
        continueButton = ContinueButton(self, 'continue.png', (477, 600))
        exitButton = ExitButton(self, 'exit.png', (527, 703))
        self.GUIelements.append(continueButton)
        self.GUIelements.append(exitButton)

class CharacterSelection(GUIScreen):

    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'char_select.png')
        meele = MeeleButton(self, 'meele_pick_char.png', (300, 370))
        ranged = RangedButton(self, 'archer_pick_char.png', (750, 325))
        self.GUIelements.append(meele)
        self.GUIelements.append(ranged)

class PauseScreen(GUIScreen):

    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'controls_screen.png')
        #Button creation and append to the element list
        resumeButton = ResumeButton(self, 'continue.png', (477, 600))
        exitButton = ExitButton(self, 'exit.png', (527, 703))
        self.GUIelements.append(resumeButton)
        self.GUIelements.append(exitButton)

class GameoverScreen(GUIScreen):

    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'game_over.png')
        tryAgainButton = TryAgainButton(self, 'si.png', (486, 550))
        exitButton = ExitButton(self, 'no.png', (650, 552))
        self.GUIelements.append(tryAgainButton)
        self.GUIelements.append(exitButton)


class LevelCompleteScreen(GUIScreen):

    def __init__(self, menu, level):
        GUIScreen.__init__(self, menu, 'level_completed' + str(level) + '.png')
        nextLevelButton = NextLevelButton(self, 'next_level.png', (670,540))
        tryAgainButton = TryAgainButton(self, 'reintentar.png', (210, 550))
        exitButton = ExitButton(self, 'exit.png', (529, 630))
        self.GUIelements.append(nextLevelButton)
        self.GUIelements.append(tryAgainButton)
        self.GUIelements.append(exitButton)

class GameCompletedScreen(GUIScreen):

    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'level_completed4.png')
        creditsButton = CreditsButton(self, 'creditos.png', (750, 630)) 
        self.GUIelements.append(creditsButton)

class CreditsScreen(GUIScreen):
    
    def __init__(self, menu):
        GUIScreen.__init__(self, menu, 'credits.png')
        mainMenuButton = PlayAgainButton(self, 'main_menu.png', (700, 630))
        self.GUIelements.append(mainMenuButton)

#Class Menu, it'll be use for the menus in the game, like main menu, pause menu, game over, etc...
class Menu(Scene):

    def __init__(self, director, screens):
        #Parent init method
        Scene.__init__(self, director)
        #Screen list
        self.screen_list = []
        #Creation of screens and append to the list
        for screen in screens:
            self.screen_list.append(screen)
        #Main screen as actual screen
        self.showMainScreen()

    def update(self, *args):
        return

    def events(self, event_list):
        #Check if you want to exit the scene
        for event in event_list:
            #Comunicate to director if you want to exit the scene
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exitProgram()
            elif event.type == pygame.QUIT:
                self.exitProgram()

        #Actual screen recieves event list
        self.screen_list[self.actualScreen].events(event_list)

    def paint(self, screen):
        self.screen_list[self.actualScreen].paint(screen)


    #Generic methods for all menus
    def exitProgram(self):
        self.director.exitProgram()

    def showMainScreen(self):
        self.actualScreen = 0


class MainMenu(Menu):

    def __init__(self, director):
        screens = [MainScreen(self), StoryScreen1(self), 
                    StoryScreen2(self), ControlsScreen(self), CharacterSelection(self)]
        Menu.__init__(self, director, screens)

    def showStory(self):
        self.actualScreen = 1

    def executeGame(self, char):
        self.director.game_level = 1
        self.director.char_select = char
        level = stage.Stage(self.director, self.director.game_level, self.director.char_select)
        self.director.stackScene(level)

    def previousScreen(self):
        self.actualScreen -= 1

    def nextScreen(self):
        self.actualScreen += 1

    def meelePicked(self):
        self.executeGame(1)
    
    def rangedPicked(self):
        self.executeGame(2)

class PauseMenu(Menu):

    def __init__(self, director):
        screens = [PauseScreen(self)]
        Menu.__init__(self, director, screens)

    def events(self, event_list):
        #Check if want to exit the scene
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    self.exitProgram()
                elif event.key == pygame.K_p:
                    self.continueGame()
            elif event.type == pygame.QUIT:
                self.director.exitProgram()

        self.screen_list[self.actualScreen].events(event_list)

    def continueGame(self):
        self.director.exitScene()


class GameoverMenu(Menu):

    def __init__(self, director):
        screens = [GameoverScreen(self)]
        Menu.__init__(self, director, screens)

    #Game over methods
    def tryAgain(self):
        self.director.exitScene()
        self.director.stackScene(stage.Stage(self.director, self.director.game_level, self.director.char_select))



class LevelCompletedMenu(Menu):

    def __init__(self, director):
        screens = [LevelCompleteScreen(self, director.game_level)]
        Menu.__init__(self, director, screens)

    #Level completed methods
    def tryAgain(self):
        self.director.exitScene()
        self.director.stackScene(stage.Stage(self.director, self.director.game_level, self.director.char_select))


    def nextLevel(self):
        self.director.exitScene()
        self.director.game_level += 1
        self.director.stackScene(stage.Stage(self.director, self.director.game_level, self.director.char_select))

class GameCompletedMenu(Menu):

    def __init__(self, director):
        screens = [GameCompletedScreen(self), CreditsScreen(self)]
        Menu.__init__(self, director, screens)

    def nextScreen(self):
        self.actualScreen += 1

    def playAgain(self):
        self.director.exitScene()
        self.director.stackScene(MainMenu(self.director))
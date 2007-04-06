import qgl
import pygame
from pygame.locals import *

from menu import Menu
from scene import Scene
import levels

class MainMenu(Scene):
    
    def __init__(self, world, initial_option=0):
        Scene.__init__(self, world)

        items = [
                 ("Start new game", self.on_new_game),
                 ("Option", self.on_options),
                 ("Credits", self.on_credits),
                 ("Quit", self.on_quit),
                 ]

        self.menu = Menu(self, items, initial_option)


    def update(self, dt):
        self.menu.update()

    def update_event(self, event):
        self.menu.update_event(event)


    # Handlers 

    def on_new_game(self):        
        self.game.change_scene(levels.LevelOne(self.game))

    def on_credits(self):
        print "Ha seleccionado 'credits'"

    def on_quit(self):
        self.game.quit = True

    def on_options(self):
        from options import Options
        self.game.change_scene(Options(self.game, self.menu.index))

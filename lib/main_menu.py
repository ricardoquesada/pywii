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
        self.game.change_scene(LevelsMenu(self.game)) #

    def on_credits(self):
        print "Ha seleccionado 'credits'"

    def on_quit(self):
        self.game.quit = True

    def on_options(self):
        from options import Options
        self.game.change_scene(Options(self.game, self.menu.index))



def runner(g, level):
    def f( ) :
        g.change_scene(level(g))
    return f

class LevelsMenu(Scene):
    def __init__(self, world, initial_option=0):
        Scene.__init__(self, world)
        items=[]
        for name,level in levels.levels:
            items.append( (name, runner(self.game, level) ) )
        items.append( ("back", self.on_back) )
        self.menu = Menu(self, items, initial_option)
        
    def update(self, dt):
        self.menu.update()

    def update_event(self, event):
        self.menu.update_event(event)

    # Handlers 
    def on_back(self):
        self.game.quit = True

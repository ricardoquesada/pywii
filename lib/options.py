from scene import Scene
from menu import Menu
from common import *
from main_menu import MainMenu

class Options(Scene):

    def __init__(self, game, last_option_in_main):
        Scene.__init__(self, game)
        items = [
                ("Fullscreen", self.game.fullscreen),
                ("Return", self.on_return)
                ]

        self.menu = Menu(self, items)
        self.last_option_in_main = last_option_in_main
    
    def update(self, dt):
        self.menu.update()

    def update_event(self, event):
        self.menu.update_event(event)
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.game.change_scene(MainMenu(self.game, self.last_option_in_main))

    def on_return(self):
        self.game.change_scene(MainMenu(self.game, self.last_option_in_main))

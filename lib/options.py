from scene import Scene
from menu import Menu

class Options(Scene):

    def __init__(self, game):
        Scene.__init__(self, game)
        items = [
                ("Fullscreen", self.game.fullscreen),
                ("Return", self.on_return)
                ]

        self.menu = Menu(self, items)
    
    def update(self):
        self.menu.update()

    def update_event(self, event):
        self.menu.update_event(event)

    def on_return(self):
        from main_menu import MainMenu
        self.game.change_scene(MainMenu(self.game))

import qgl
from common import *

class NotImplementedError(Exception):
    pass

class Scene:

    def __init__(self, game):
        self.game = game
        self.compiler = qgl.render.Compiler()
        self.renderer = qgl.render.Render()
        self.root_node = qgl.scene.Root()
        
        self.picker = qgl.render.Picker()
        self.group = qgl.scene.Group()
        
        #self.viewport = qgl.scene.PerspectiveViewport()
        #self.group.translate = ( 0.0, 0.0, -250 )
        #light = qgl.scene.state.Light(position=(0,10,20))
        #light.diffuse = ( 1.0, 1.0, 1.0, 0.0 )

        self.viewport = qgl.scene.OrthoViewport()
        self.viewport.screen_dimensions = (0,0) + WINDOW_SIZE
       
        self.root_node.add(self.viewport)
        self.viewport.add(self.group)
        self.root_node.accept(self.compiler)

    def render(self):
        self.root_node.accept(self.renderer)

    def update(self):
        raise NotImplementedError("You must overwrite this method.")

    def update_event(self, event):
        raise NotImplementedError("You must overwrite this method.")

    def add(self, object):
        self.group.add(object)

    def add_group(self, group):
        self.viewport.add(group)

    def accept(self):
        self.root_node.accept(self.compiler)

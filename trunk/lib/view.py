'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''

import data
import qgl
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WINDOW_SIZE=(800,600)

class View:
    def init(self):
        #Create the visitors.
        #The compiler visitor is used to change a Node object into a set of OpenGL draw commands. More on nodes later.
        self.compiler = qgl.render.Compiler()
        #The render visitor is used to execute compiled commands.
        self.renderer = qgl.render.Render()
        #the picker visitor can check which attributes are clicked by a mouse
        self.picker = qgl.render.Picker()

        #the root node is the root of the tree structure (also called a scene graph). Branches get added to the root. 
        self.root_node = qgl.scene.Root()

        #every root node must have a viewport branch, which specifies which area of the screen to draw to.
        #the PersepctiveViewport renders all its children in a 3d view.
        #self.viewport = qgl.scene.PerspectiveViewport()
        self.viewport = qgl.scene.OrthoViewport()
        self.viewport.screen_dimensions = (0,0) + WINDOW_SIZE

        #a group node can translate, rotate and scale its children. it can also contain leaves, which are drawable things.
        self.gameGroup = qgl.scene.Group()
        #because this group will be displayed in 3d, using a PerspectiveViewport, it makes sense to move it into the screen
        #using the group.translate attribute. Any objects drawn at a depth (z) of 0.0 in a perspective viewport will not be show.
        #self.gameGroup.translate = ( 0.0, 0.0, -50 )

        #the group node has attributes that can be changed to manipulate the position of its children.
        #self.gameGroup.axis = (0,1,0)
        #self.gameGroup.angle = 45

        #a Light leaf will control the lighting of any leaves rendered after it.
        #light = qgl.scene.state.Light(position=(0,10,20))

        #lets give the light a red hue
        #light.diffuse = ( 1.0, 1.0, 1.0, 0.0 )

        #if the light leaf is added to the same group as the children it is going
        #to light, it would move, and rotate with its children.
        #this is not the effect we want in this case, so we add the light to its
        #own group, which we will call environment.
        environment = qgl.scene.Group()

        #Now we add the different nodes and leaves into a tree structure using the .add method. 
        self.root_node.add(self.viewport)
        self.viewport.add(environment)
        #environment.add(light)
        environment.add(self.gameGroup)

        #leaves are added to the group. The texture leaf loads a texture image ready for drawing. Any quads leaves, which are drawn 
        #after a texture leaf will be rendered with the texture image.
        texture = qgl.scene.state.Texture(data.filepath("bola2.png"))
        quad = qgl.scene.state.Quad((64,64))
        #Now we add the different nodes and leaves into a tree structure using the .add method.
        self.gameGroup.add(texture)
        self.gameGroup.add(quad)

        self.root_node.accept(self.compiler)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type is QUIT:
                raise SystemExit
            elif event.type is KEYDOWN and event.key is K_ESCAPE:
                raise SystemExit

    def render(self):
        self.root_node.accept(self.renderer)

    def test(self):
        pygame.init()
        flags =  OPENGL|DOUBLEBUF|HWSURFACE
        pygame.display.set_mode(WINDOW_SIZE, flags)
        clock = pygame.time.Clock()
        self.init()
        while 1:
            clock.tick(30)
            self.handleEvents()
            self.render()
            self.gameGroup.angle += 2
            pygame.display.flip()

def main():
    bola= data.filepath('bola.png')
    view=View()
    view.test()

import pygame
import qgl
import euclid
import world
import data

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WINDOW_SIZE=(800,600)

class View:
    def init(self):
        self.compiler = qgl.render.Compiler()
        self.renderer = qgl.render.Render()
        self.picker = qgl.render.Picker()
        self.root_node = qgl.scene.Root()

        self.viewport = qgl.scene.PerspectiveViewport()
        #self.viewport = qgl.scene.OrthoViewport()
        self.viewport.screen_dimensions = (0,0) + WINDOW_SIZE

        self.gameGroup = qgl.scene.Group()
        self.gameGroup.translate = ( 0.0, -15.0, -50 )
        #self.gameGroup.axis = (0,1,0)
        #self.gameGroup.angle = 45

        #light = qgl.scene.state.Light(position=(0,10,20))
        #light.diffuse = ( 1.0, 1.0, 1.0, 0.0 )

        environment = qgl.scene.Group()
        self.root_node.add(self.viewport)
        self.viewport.add(environment)
        #environment.add(light)
        environment.add(self.gameGroup)

        self.world = world.World()
        self.gameGroup.add(self.addBall(1, 10))
        self.gameGroup.add(self.addFloor(0))

        self.root_node.accept(self.compiler)

    def addBall(self, x, y):
        ball = world.Ball(euclid.Vector2(1, 10) )
        self.world.add_ball(ball)
        ballGroup = qgl.scene.Group()
        ballTexture = qgl.scene.state.Texture(data.filepath("bola3.png"))
        ballQuad = qgl.scene.state.Quad((3,3))
        ballGroup.add(ballTexture)
        ballGroup.add(ballQuad)
        ball.group = ballGroup
        return ballGroup

    def addFloor(self, y):
        floor = world.Floor(y)
        self.world.add_passive( floor )
        floorGroup = qgl.scene.Group()
        floorGroup.translate = ( 0, y, 0 )
        floorTexture = qgl.scene.state.Texture(data.filepath("piso.png"))
        floorQuad = qgl.scene.state.Quad((200,1))
        floorGroup.add(floorTexture)
        floorGroup.add(floorQuad)
        floor.group = floorGroup
        return floorGroup

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type is QUIT:
                raise SystemExit
            elif event.type is KEYDOWN and event.key is K_ESCAPE:
                raise SystemExit

    def render(self):
        for ball in self.world.balls:
            position = ball.position
            ball.group.translate = (position.x, position.y, 0)
            pass
        self.root_node.accept(self.renderer)

    def test(self):
        pygame.init()
        flags =  OPENGL|DOUBLEBUF|HWSURFACE
        pygame.display.set_mode(WINDOW_SIZE, flags)
        clock = pygame.time.Clock()
        self.init()
        while 1:
            dt = clock.tick(30)/1000.0
            self.handleEvents()
            self.world.loop(dt)
            self.render()
            #floorGroup.translate = ( 0, y, 0 )
            #self.ballGroup.angle += 2
            pygame.display.flip()

def main():
    bola= data.filepath('bola.png')
    view=View()
    view.test()

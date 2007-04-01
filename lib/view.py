import pygame
import qgl
import euclid
import world
import data
import random
import math

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

        light = qgl.scene.state.Light(position=(0,10,20))
        light.diffuse = ( 1.0, 1.0, 1.0, 0.0 )

        environment = qgl.scene.Group()
        self.root_node.add(self.viewport)
        self.viewport.add(environment)
        environment.add(light)
        environment.add(self.gameGroup)

    def compile(self):
        self.root_node.accept(self.compiler)

    def addBall(self, x, y):
        ball = world.Ball(euclid.Point2(x, y) )
        self.world.add_ball(ball)
        ballGroup = qgl.scene.Group()

        textureFile=random.choice("calisto.jpg europe.jpg ganimedes.jpg i.jpg jupite.jpg luna.jpg marte.jpg mercurio.jpg tierra.jpg tierraloca.jpg venu.jpg".split())

        ballTexture = qgl.scene.state.Texture(data.filepath(textureFile))
        #ballQuad = qgl.scene.state.Quad((3,3))
        SEGS=16
        ballQuad = qgl.scene.state.Sphere(1, x_segments=SEGS, y_segments=SEGS)
        ballGroup.add(ballTexture)
        ballGroup.add(ballQuad)
        ballGroup.axis = (0,1,0)
        ball.group = ballGroup
        return ballGroup

    def addSegment(self, x1, y1, x2, y2):
        segment = world.Segment(x1, y1, x2, y2)
        self.world.add_passive( segment )
        segmentGroup = qgl.scene.Group()
        dy = y2-y1
        dx = x2-x1
        segmentGroup.angle = math.degrees(math.atan2(dy, dx))
        segmentGroup.translate = ( x1 + dx/2, y1 + dy/2, 0.0 )
        segmentTexture = qgl.scene.state.Texture(data.filepath("piso.png"))
        segmentQuad = qgl.scene.state.Quad((math.hypot(dx,dy),1))
        segmentGroup.add(segmentTexture)
        segmentGroup.add(segmentQuad)
        segment.group = segmentGroup
        return segmentGroup

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
            ball.group.angle += 4
        self.root_node.accept(self.renderer)

    def test(self):
        pygame.init()
        flags =  OPENGL|DOUBLEBUF|HWSURFACE
        pygame.display.set_mode(WINDOW_SIZE, flags)
        

        self.init()

        self.world = world.World()
        for n in range(-25,25,2):
            self.gameGroup.add( self.addBall(n, 5) )
            
        #self.gameGroup.add( self.addBall(1, 10) )
        #self.gameGroup.add( self.addBall(5, 10) )

        #self.gameGroup.add(self.addFloor(0))
        self.gameGroup.add( self.addSegment(0, 0, 2, 0) )
        self.gameGroup.add( self.addSegment(30, 3, -30, 3) )

        self.compile()
        clock = pygame.time.Clock()
        while 1:
            dt = clock.tick(30)/1000.0
            self.handleEvents()
            self.world.loop(dt)
            #for e in self.world.get_events(): print e
            #print self.world.balls[0]
            self.render()
            #self.ballGroup.angle += 2
            pygame.display.flip()

def main():
    view=View()
    view.test()


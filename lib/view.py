import qgl
import world
from scene import Scene
import leafs
import pygame
import qgl
import euclid
import world
import data
import random
import math
from main_menu import MainMenu

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from common import *
from zza import xmenu

WINDOW_SIZE=(800,600)



class View(Scene):
    
    def __init__(self, game):
        Scene.__init__(self, game, PERSPECTIVE)
        self.world = world.World()

        if 0:
            for n in range(-25,25,2):
                self.group.add( self.addBall(n, 5) )
                
            self.group.add( self.addSegment(0, 0, 2, 0, bounce=2) )
            self.group.add( self.addSegment(0, 6, 6, 0) )
            self.group.add( self.addSegment(30, 6, -30, 0) )
            self.group.add( self.addGoal(1,30, 3.0) )
        else:
            self.group.add( self.addFloor(0,0,2,0) )

            self.group.add( self.addBall(1, 10) )
            self.group.add( self.addSegment(0,3,2,3, bounce=2) )

            self.group.add( self.addBall(5, 10) )
            self.group.add( self.addSegment(4,4,6,3) )

            self.group.add( self.addGoal(1,30, 3.0) )


        self.menu = xmenu(qgl.scene, self.root_node, "hola", "que", "tal", "alecu", "como", "esta", "phil?")    
        porcion = qgl.scene.Group()
        v = [ (0,0), (0,10), (10,10) ]
        porcion.add( leafs.Triangle(v) )
        v = [ (0,0), (10,10), (10,0), (15,15), (15,0) ]
        porcion.add( leafs.PorcionMuzza(v) )
        porcion.translate = -5,0,10
        self.group.add( porcion )

        textureFile=random.choice("calisto.jpg europe.jpg ganimedes.jpg i.jpg jupite.jpg luna.jpg marte.jpg mercurio.jpg tierra.jpg tierraloca.jpg venu.jpg".split())
        ballTexture = qgl.scene.state.Texture(data.filepath(textureFile))
        v = [ (15,15), (10,0), (0,10) ]
        self.group.add( ballTexture, leafs.Triangle(v) )
        self.accept()


    def update(self, dt):
        self.world.loop(dt/1000.0)


    def update_event(self, event):

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.game.change_scene(MainMenu(self.game))
        elif event.type is MOUSEMOTION:
            self.picker.set_position(event.pos)
            self.root_node.accept(self.picker)
            self.menu.moves(self.picker.hits)
                                
        elif event.type is MOUSEBUTTONDOWN:
            #tell the picker we are interested in the area clicked by the mouse
            self.picker.set_position(event.pos)
            #ask the root node to accept the picker.
            self.root_node.accept(self.picker)
            #picker.hits will be a list of nodes which were rendered at the position.
            #to visualise which node was clicked, lets adjust its angle by 10 degrees.
            for hit in self.picker.hits:
                print self.menu.get(hit)

    def render(self):
        for ball in self.world.balls:
            position = ball.position
            ball.group.translate = (position.x, position.y, 0)
            ball.group.angle += 4
        self.root_node.accept(self.renderer)
        

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

    def addFloor(self, *a, **kw):
        return self.addSegment(*a, **kw)

    def addSegment(self, x1, y1, x2, y2, **kw):
        segment = world.Segment(x1, y1, x2, y2, **kw)
        self.world.add_passive( segment )
        segmentGroup = qgl.scene.Group()
        dy = y2-y1
        dx = x2-x1
        segmentGroup.angle = math.degrees(math.atan2(dy, dx))
        segmentGroup.translate = ( x1 + dx/2, y1 + dy/2, 0.0 )
        segmentTexture = qgl.scene.state.Texture(data.filepath("piso.png"))
        segmentQuad = qgl.scene.state.Quad((math.hypot(dx,dy)+1,1))
        segmentGroup.add(segmentTexture)
        segmentGroup.add(segmentQuad)
        segment.group = segmentGroup
        return segmentGroup

    def addGoal(self, x, y, r):
        goal = world.Goal(x, y, r)
        self.world.add_passive( goal )
        goalGroup = qgl.scene.Group()
        goalGroup.translate = (x, y, 0.0)
        goalTexture = qgl.scene.state.Texture(data.filepath("bola2.png"))
        goalQuad = qgl.scene.state.Quad((r*2,r*2))
        goalGroup.add(goalTexture)
        goalGroup.add(goalQuad)
        goal.group = goalGroup
        return goalGroup



if __name__ == '__main__':
    import game
    g = game.Game()
    g.change_scene(View(g))
    g.main_loop()

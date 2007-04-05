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

import scene 
import zza

def addBall(theView):
    class AddBall(scene.doNothingHandler):
        view = theView
        def run(self):
            self.view.addBallEv(self.lastClick.pos)
    return AddBall

def rectaHandler(theView):
    class RectaHandler(scene.twoClicks):
        view=theView
        def run(self):
            print 'recta coord',self.click1.event.pos,'to',self.click2.event.pos
            x1p, y1p = self.click1.event.pos
            x2p, y2p = self.click2.event.pos
            self.view.addLineEv(x1p,y1p,x2p,y2p, self.click1.matrix, self.click2.matrix)
    return RectaHandler

        
def GroupAdd(f):
    def bigF(self, *args, **kwargs):
        ng = f(self, *args,**kwargs)
        ng.accept(self.compiler)
        self.group.add(ng)
        return ng
    return bigF

class View(Scene):
    def setup_level(self):
        self.group.add( self.addFloor(0,0,2,0) )
        return
##        self.group.add( self.addBall(1, 10) )
##        self.group.add( self.addSegment(0,3,2,3, bounce=1.1) )
##        self.group.add( self.addBall(5, 10) )
##        self.group.add( self.addSegment(4,4,6,3) )
##        self.group.add( self.addGoal(1,30, 3.0) )
            
    def __init__(self, game):
        Scene.__init__(self, game, ORTHOGONAL)
        self.world = world.World()
        
        self.setup_level()
        self.camera_x = 0
        self.camera_y = -200
        self._move_camera(self.camera_x, self.camera_y)
            
        self.menu = xmenu(self,
            {"hola":addBall(self), 
             "line":rectaHandler(self), 
             "que":zza.exitMenu, 
             "tal":zza.exitMenu, 
             "alecu":zza.exitMenu, 
             "phil?":zza.exitMenu})
             
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

    def saveState(self, event):
        Scene.saveState(self, event)
        self.lastClickMatrix = self.getViewMatrix()

    def addLineEv(self, x1p,y1p,x2p,y2p,matrix1=None, matrix2=None):
        a,b = self.screenToAmbient(x1p,y1p)             
        c,d = self.screenToAmbient(x2p,y2p)
        if matrix1==None: matrix1=self.getViewMatrix()
        if matrix2==None: matrix1=self.getViewMatrix()
        x1,y1,z1 = matrix1 * euclid.Point3(a,b,0)
        x2,y2,z2 = matrix2 * euclid.Point3(c,d,0)
        self.addSegment(x1,y1,x2,y2) 
                
    def addBallEv(self, npos):
        a,b = self.screenToAmbient(*npos)
        x2,y2,z2 = self.getViewMatrix() * euclid.Point3(a,b,0)
        ball = world.Ball(euclid.Point2(x2, y2) )
        self.addBall(ball)
        
    def update(self, dt):
        import sound
        self.world.loop(dt/500.0)
        for evt in self.world.get_events():
            print evt
            if isinstance(evt, world.Collision):
                print evt.ball.velocity.magnitude(), evt
                n = evt.ball.velocity.magnitude()/50
                if (n>1.0):
                    n = 1.0
                vol = 1.0
                sound.playSound(n, vol)
                
            if isinstance(evt, world.NewObject):
                if isinstance(evt.object, world.Ball):
                    self.addBall(evt.object)
                
        self._update_camera(pygame.mouse.get_pos())

    def _update_camera(self, pos):
        left, up = 0, 0
        right, down = WINDOW_SIZE
        velocity = 200.0
        delta = 200
        x, y = pos
        initial_x, initial_y = x, y
        x = max(x, 1)
        y = max(y, 1)

        if x < delta:
            x += velocity / (left - x)
        elif x > right - delta:
            x += velocity / (right - x)

        if y < delta:
            y -= velocity / (up - y)
        elif y > down - delta:
            y -= velocity / (down - y)

        if x != initial_x or y != initial_y:
            self._move_camera(initial_x - x, initial_y - y)
            return False
        else:
            # Permite que el metodo superior acceda a este evento
            return True


    def _move_camera(self, dx, dy):
        dx=dy=0 #XXX REMOVE SCROLL
        max_delta = 10
        self.camera_x += dx / 5
        self.camera_y += dy / 5
        bound_up, bound_down, bound_left, bound_right = CAMERA_AREA

        if self.camera_x > bound_left:
            self.camera_x = bound_left
        elif self.camera_x < bound_right:
            self.camera_x = bound_right
    
        if self.camera_y < bound_up:
            self.camera_y = bound_up
        elif self.camera_y > bound_down:
            self.camera_y = bound_down

        self.group.scale = (10.0,10.0,0.0)
        self.group.translate = (self.camera_x, self.camera_y,0)

    def getViewMatrix(self):
        translate = -1*euclid.Point3(*self.group.translate)
        scale = euclid.Point3(1.0/self.group.scale[0], 1.0/self.group.scale[1], 0)
        return euclid.Matrix4.new_scale(*scale).translate(*translate)

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.game.change_scene(MainMenu(self.game))
        elif event.type is MOUSEMOTION:
            pass
        elif event.type is MOUSEBUTTONDOWN:
            self.picker.set_position(event.pos)
            self.root_node.accept(self.picker)
            if len(self.picker.hits)>0:
                for hit in self.picker.hits:
                    return
            else:
                self.push_handler(self.menu)

    def render(self):
        for ball in self.world.balls:
            position = ball.position
            ball.group.translate = (position.x, position.y, 0)
            ball.group.angle += 4
        self.root_node.accept(self.renderer)
        
    @GroupAdd
    def addBall(self,ball):
        print 2,repr(ball)
        #self.world.add_ball(ball)
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

    @GroupAdd
    def addFloor(self, *a, **kw):
        return self.addSegment(*a, **kw)

    @GroupAdd
    def addSegment(self, x1, y1, x2, y2, **kw):
        segment = world.Segment(x1, y1, x2, y2, **kw)
        self.world.add_passive( segment )
        segmentGroup = qgl.scene.Group()
        dy = y2-y1
        dx = x2-x1
        segmentGroup.angle = math.degrees(math.atan2(dy, dx))
        segmentGroup.translate = ( x1 + dx/2, y1 + dy/2, 0.0 )
        segmentTexture = qgl.scene.state.Texture(data.filepath("rebotador.png"))
        segmentQuad = qgl.scene.state.Quad((math.hypot(dx,dy)+1,1))
        segmentGroup.add(segmentTexture)
        segmentGroup.add(segmentQuad)
        segment.group = segmentGroup
        return segmentGroup
        
    @GroupAdd
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

    @GroupAdd
    def addGenerator(self, pos, r=1):
        x,y=pos
        gen = world.Generator(pos,view=self)
        self.world.add_active( gen )
        genGroup = qgl.scene.Group()
        genGroup.translate = (x, y, 0.0)
        genTexture = qgl.scene.state.Texture(data.filepath("bola2.png"))
        genQuad = qgl.scene.state.Quad((r*2,r*2))
        genGroup.add(genTexture)
        genGroup.add(genQuad)
        gen.group = genGroup
        return genGroup



if __name__ == '__main__':
    import game
    g = game.Game()
    g.change_scene(View(g))
    g.main_loop()

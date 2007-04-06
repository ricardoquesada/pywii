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

QUAD_HEIGHT=4
CELESTE_CIELO = (0.09, 0.27, 0.64, 0)

def addBall(theView):
    class AddBall(scene.doNothingHandler):
        view = theView
        def __init__(self, popupPosition, *a):
            scene.doNothingHandler.__init__(self, *a)
            self.popupPosition = popupPosition
            print "adding ball...", a, popupPosition
        def run(self):
            self.view.addBallEv(self.popupPosition)
    return AddBall

def rectaHandler(theView):
    class RectaHandler(scene.twoClicks):
        view=theView
        def __init__(self, popupPosition, *a):
            scene.twoClicks.__init__(self, *a)
            self.popupPosition = popupPosition
        def run(self):
            self.view.hideLineGhost()
            self.view.addLineEv(self.popupPosition, self.click2.position)
        def motion(self, position):
            self.view.showLineGhost(self.popupPosition, position)
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
##        self.group.add( self.addFloor(0,0,2,0) )
        return
            
    def __init__(self, game):
        Scene.__init__(self, game, ORTHOGONAL)
        self.world = world.World()
        self.root_node.background_color = CELESTE_CIELO
        
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
             
        if 0:
            porcion = qgl.scene.Group()
            v = [ (0,0), (0,10), (10,10) ]
            porcion.add( leafs.Triangle(v) )
            v = [ (0,0), (10,10), (10,0), (15,15), (15,0) ]
            porcion.add( leafs.PorcionMuzza(v) )
            porcion.translate = -5,0,10
            self.group.add( porcion )

            #textureFile=random.choice("calisto.jpg europe.jpg ganimedes.jpg i.jpg jupite.jpg luna.jpg marte.jpg mercurio.jpg tierra.jpg tierraloca.jpg venu.jpg".split())
            ballTexture = qgl.scene.state.Texture(data.filepath("dad.gif"))
            v = [ (15,15), (10,0), (0,10) ]
            self.group.add( ballTexture, leafs.Triangle(v) )
        self.initLineGhost()
        mountainsGroup = qgl.scene.Group()
        mountainsTexture = qgl.scene.state.Texture(data.filepath("montagnas.png"))
        FACTOR= 8
        mountainsQuad = qgl.scene.state.Quad((2403/FACTOR,427/FACTOR))
        mountainsGroup.translate = (0,-53,0)
        mountainsGroup.add(mountainsTexture, mountainsQuad)
        self.group.add(mountainsGroup)
        self.accept()

    def addLineEv(self, (x1,y1), (x2,y2)):
        self.addSegment(x1,y1,x2,y2) 
                
    def addBallEv(self, worldPos):
        ball = world.Ball(euclid.Point2(*worldPos) )
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
        #dx=dy=0 #XXX REMOVE SCROLL
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

        #self.group.scale = (15.0,15.0,0.0)
        self.group.scale = (5.0,5.0,0.0)
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
                self.menu.popup(event.pos)

    def worldPosFromMouse(self, mousePos):
        a,b = self.screenToAmbient(*mousePos)             
        x1,y1,z1 = self.getViewMatrix() * euclid.Point3(a,b,0)
        return x1, y1

    def render(self):
        for ball in self.world.balls:
            position = ball.position
            ball.group.translate = (position.x, position.y, 0)
            #ball.group.axis = (1,.5,.7)
            ball.group.angle += 4
        self.root_node.accept(self.renderer)
        
    @GroupAdd
    def addBall(self,ball):
        ballGroup = qgl.scene.Group()
        #textureFile=random.choice("calisto.jpg europe.jpg ganimedes.jpg i.jpg jupite.jpg luna.jpg marte.jpg mercurio.jpg tierra.jpg tierraloca.jpg venu.jpg".split())
        #ballTexture = qgl.scene.state.Texture(data.filepath(textureFile))
        ballTexture = qgl.scene.state.Texture(data.filepath("dad.gif"))
        #ballQuad = qgl.scene.state.Quad((3,3))
        #SEGS=16
        #ballQuad = qgl.scene.state.Sphere(1, x_segments=SEGS, y_segments=SEGS)
        ballQuad = qgl.scene.state.Quad((3,6))
        ballGroup.add(ballTexture)
        ballGroup.add(ballQuad)
        ballGroup.axis = (0,0,1)
        position = ball.position
        ballGroup.translate = (position.x, position.y, 0)
        ball.group = ballGroup
        return ballGroup

    @GroupAdd
    def addFloor(self, *a, **kw):
        return self.addSegment(*a, **kw)

    def initLineGhost(self):
        self.ghostGroup = qgl.scene.Group()
        self.ghostGroup.scale = (0,0,0)
        segmentTexture = qgl.scene.state.Texture(data.filepath("rebotador-ghost.png"))
        segmentQuad = qgl.scene.state.Quad((1,QUAD_HEIGHT))
        self.ghostGroup.add(segmentTexture)
        self.ghostGroup.add(segmentQuad)
        self.group.add(self.ghostGroup)

    def showLineGhost(self, (x1, y1), (x2, y2)):
        dy = y2-y1
        dx = x2-x1
        self.ghostGroup.angle = math.degrees(math.atan2(dy, dx))
        self.ghostGroup.translate = ( x1 + dx/2, y1 + dy/2, 0.0 )
        self.ghostGroup.scale = (math.hypot(dx,dy)+1, 1.0, 0.0)

    def hideLineGhost(self):
        self.ghostGroup.scale = (0,0,0)

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
        segmentQuad = qgl.scene.state.Quad((math.hypot(dx,dy)+1,QUAD_HEIGHT))
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
        genTexture = qgl.scene.state.Texture(data.filepath("generador.png"))
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

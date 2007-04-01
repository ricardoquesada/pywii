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


BEGINLINE, ENDLINE = range(2)

class View(Scene):
    
    def __init__(self, game):
        Scene.__init__(self, game, ORTHOGONAL) #PERSPECTIVE)
        self.world = world.World()

        if 1:
            #for n in range(-25,25,2):
            #    self.group.add( self.addBall(n, 5) )
            self.group.add( self.addBall( 5,5 ) )    
            
            self.group.add( self.addSegment(0, 0, 10, 0) )
            self.group.add( self.addSegment(10, 0, 10, 10) )
            self.group.add( self.addSegment(0, 10, 0, 0) )
            
            self.group.add( self.addGoal( 13, 6, 2.) )
            self.group.add( self.addGoal( -3, 6, 2.) )

            self.world.add_attractor( world.Attractor( 11, 11, 0.5 ) )
        else:
            self.group.add( self.addFloor(0,0,2,0) )

            self.group.add( self.addBall(1, 10) )
            self.group.add( self.addSegment(0,3,2,3, bounce=2) )

            self.group.add( self.addBall(5, 10) )
            self.group.add( self.addSegment(4,4,6,3) )

            self.group.add( self.addGoal(1,30, 3.0) )

        self.camera_x = 0
        self.camera_y = -200
        self._move_camera(self.camera_x, self.camera_y)
            

        def F(ev, npos):
            pass #print ev
        self.menu = xmenu(self, self.root_node, 
            {"hola":self.addBallEv, "line":self.selLine, "que":F, "tal":F, "alecu":F, 
             "como":F, "esta":F, "phil?":F})
             
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
        self.lineStat = BEGINLINE

    def selLine(self, ev, npos):
        if self.lineStat == BEGINLINE:
            self.beginLine(ev,npos)
        elif self.lineStat==ENDLINE:
            self.endLine(ev,npos)

    def beginLine(self, ev, npos):
        self.lineFrom = npos
        self.lineStat = ENDLINE
        print 'begin line from:',npos
        
    def endLine(self, ev, npos):
        self.lineStat = BEGINLINE
        print 'end line:',self.lineFrom, 'to:',npos
        x1,y1,_ = self.lineFrom
        x2,y2,_ = npos
        self.addLineEv(x1,y1,x2,y2)
        
    def addLineEv(self, x1p,y1p,x2p,y2p):
        x1,y1,z1 = self.theMatrix * euclid.Point3(x1p,y1p,0)
        x2,y2,z2 = self.theMatrix * euclid.Point3(x2p,y2p,0)
        print x1,y1,x2,y2
        ng = self.addSegment(x1,y1,x2,y2) 
        ng.accept(self.compiler)
        self.group.add( ng )
                
    def addBallEv(self, ev, npos):
        ng = self.addBall(1, 10)
        ng.accept(self.compiler)
        self.group.add( ng )
        
    def update(self, dt):
        self.world.loop(dt/1000.0)
        for evt in self.world.get_events():
            print evt

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

        self.SCALE =  (20,20,0)
        self.TRANS = (self.camera_x, self.camera_y,0)
        self.group.scale= self.SCALE
        self.group.translate=self.TRANS
        s = 1.0/self.SCALE[0], 1.0/self.SCALE[1], self.SCALE[2]
        t = -1*euclid.Point3(*self.TRANS)
        self.theMatrix = euclid.Matrix4.new_scale(*s).translate(*t)


    def update_event(self, event):
        if self.menu.updateEvent(event):
            #skip other handlers
            return
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.game.change_scene(MainMenu(self.game))
        elif event.type is MOUSEMOTION:
            self.picker.set_position(event.pos)
            self.root_node.accept(self.picker)
            self.menu.moves(self.picker.hits)
                                
        elif event.type is MOUSEBUTTONDOWN:
            #if event.button==1:
            if not self.menu.shown:
                self.menu.switch(event.pos)
                return    
            #tell the picker we are interested in the area clicked by the mouse
            self.picker.set_position(event.pos)
            #ask the root node to accept the picker.
            self.root_node.accept(self.picker)
            #picker.hits will be a list of nodes which were rendered at the position.
            #to visualise which node was clicked, lets adjust its angle by 10 degrees.
            for hit in self.picker.hits:
                self.menu.select(hit, event)

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

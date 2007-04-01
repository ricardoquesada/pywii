import pygame
from pygame.locals import *

import qgl
import math
import leafs

class xmenu:
    def __init__(self, scene, root_node, options):
        self.d={}
        self.options = options.keys()
        self.callbacks = options
        self.scene = scene 
        self.rootnode = root_node
        self.viewport = qgl.scene.OrthoViewport()
        self.viewport.screen_dimensions = (0,0,800,600)
        root_node.add(self.viewport)
        self.shown=False
        self.selected=[]
        
    def select(self, group, ev):
        if group in self.groups:
            elemento = self.options[self.d[group]]
            
            ax,ay,bx,by=self.viewport.screen_dimensions 
            dx=(bx-ax)/2
            dy=(by-ay)/2
            npos = ev.pos[0]-dx,dy-ev.pos[1],0
            self.callbacks[elemento](ev, npos)
            self.hide()
            
    def calc(self, pos):
        #def r1(coef, r, k):
        #    """returns 2 puntos"""
        #    return [(r*math.sin(coef*k), r*math.cos(coef*k)),
        #            (r*math.sin(coef*(k+1)), r*math.cos(coef*(k+1)))]
        def r2(startAng, coef2, r, k):
            """returns 2 puntos"""
            return [(r*math.sin(startAng), r*math.cos(startAng)),
                    (r*math.sin(startAng+coef2), r*math.cos(startAng+coef2))]

        #make it's group
        #texture = self.ss.Texture("land.jpg")
        #sphere = self.ss.Quad((40,40))
        count = len(self.options)
        groups=[]
        
        r=80.0
        coef = math.pi*2 / count
        coef2 = coef*0.95
        cc = coef*0.025
        bandRatio=7.0/8
        ax,ay,bx,by=self.viewport.screen_dimensions 
        dx=(bx-ax)/2
        dy=(by-ay)/2
        for k in range(count):
            g=qgl.scene.Group()
            v = [(0,0)]+ r2(coef*k+cc,coef2,r*bandRatio,k)+r2(coef*k+cc,coef2,r,k)
            ##groups[k].add(texture, sphere)
            ##groups[k].translate = (r*math.sin(c), r*math.cos(c), 0) 
            ##groups[k].scale = (1, 1, 1)
            #v = [(0,0)]+ r1(coef,r*bandRatio,k)+r1(coef,r,k)
            #groups[k].add( texture, leafs.Triangle(v) )
            g.add( leafs.PorcionMuzza(v) )
            g.selectable = True
            g.translate= pos[0]-dx,dy-pos[1],0
            self.d[g]=k
            groups.append(g)
        self.groups = groups

    def updateEvent(self, event):
        picker = self.scene.picker
        if event.type is MOUSEMOTION:
            picker.set_position(event.pos)
            self.rootnode.accept (picker)
            if picker.hits:
                self.moves(picker.hits)
                return True
            return False
                
        elif event.type is MOUSEBUTTONDOWN:
            if not self.shown:
                self.switch(event.pos)
                return True   
                
            picker.set_position(event.pos)
            self.rootnode.accept(picker)
            if picker.hits:
                for hit in picker.hits:
                    self.select(hit, event)
            else:
                self.switch()
        else:
            return False
        return True

    def mouseIn(self, group):
        t = group.scale
        if t[0]<1.5:
            group.scale=t[0]+0.1,t[1]+0.1,t[2]
                        
    def mouseOut(self, group):
        t = group.scale
        if t[0]>1:
            group.scale=1,1,t[2]
            
    def moves(self, groups):
        oldselected = self.selected
        groups = filter(lambda g:g in self.groups, groups)
        self.selected = groups
        for hit in groups:
            self.mouseIn(hit)
        for oldg in oldselected:
            if oldg not in groups:
                self.mouseOut(oldg)
    
    def show(self, pos):
        self.calc(pos)
        self.viewport.add( *self.groups )
        self.viewport.accept(self.scene.compiler)
        self.shown=True
        
    def hide(self):
        self.viewport.remove( *self.groups )    
        self.shown=False
        
    def switch(self, pos=None):
        if self.shown:
            self.hide()
        else:
            if pos is None:
                raise ValueError('Invalid position')
            self.show(pos)
                
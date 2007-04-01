#How do I display a picture on the screen?


import pygame
from pygame.locals import *

import qgl
#import qgle
import math
import leafs

class xmenu:
    def __init__(self, ss, *options):
        self.d={}
        self.options = options
        self.ss = ss #scene state
        
    def get(self, group):
        if group in self.groups:
            return self.options[self.d[group]]
    def release(self, group):
        pass #print self.options[self.d[group]]
        
    def calc(self):
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
        for k in range(count):
            groups.append(qgl.scene.Group())
            v = [(0,0)]+ r2(coef*k+cc,coef2,r*bandRatio,k)+r2(coef*k+cc,coef2,r,k)
            ##groups[k].add(texture, sphere)
            ##groups[k].translate = (r*math.sin(c), r*math.cos(c), 0) 
            ##groups[k].scale = (1, 1, 1)
            #v = [(0,0)]+ r1(coef,r*bandRatio,k)+r1(coef,r,k)
            #groups[k].add( texture, leafs.Triangle(v) )
            groups[k].add( leafs.PorcionMuzza(v) )
            groups[k].selectable = True
            self.d[groups[k]]=k
            
        self.groups = groups
        
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

    def keydown(self, event):
        pass
    def keyup (self, event):
        pass
    
    def addTo(self, viewport):
        self.selected=[]
        self.calc()
        viewport.add( *self.groups )
        
    def delFrom(self, viewport):
        viewport.remove( *self.groups )    
    
    

def main():
    #setup pygame as normal, making sure to include the OPENGL flag in the init function arguments.
    pygame.init()
    flags =  OPENGL|DOUBLEBUF|HWSURFACE
    pygame.display.set_mode((800,600), flags)
    
    
    #Create two visitors.
    #The compiler visitor is used to change a Node object into a set of OpenGL draw commands. More on nodes later.
    compiler = qgl.render.Compiler()
    #The render visitor is used to execute compiled commands.
    render = qgl.render.Render()
    #the picker visitor can check which attributes are clicked by a mouse
    picker = qgl.render.Picker()
    
    #the root node is the root of the tree structure (also called a scene graph). Branches get added to the root. 
    root_node = qgl.scene.Root()
    
    #every root node must have a viewport branch, which specified which area of the screen to draw to.
    #the OrthoViewport renders all its children in a flat, orthographic view.
    viewport = qgl.scene.OrthoViewport()
    viewport.screen_dimensions = (0,0,800,600)

    #leaves are added to the group. The texture leaf loads a texture image ready for drawing. Any quads leaves, which are drawn 
    #after a texture leaf will be rendered with the texture image.
    #texture = qgl.scene.state.Texture("land.jpg")
    #quad = qgl.scene.state.Quad((100,100))


    viewport2 = qgl.scene.OrthoViewport()
    viewport2.screen_dimensions = (0,0,800,600)
    root_node.add(viewport2)
    menu = xmenu(qgl.scene.state, "hola", "que", "tal", "alecu", "como", "esta", "phil?")    
    menu.addTo(viewport2)
            
    #a group node can translate, rotate and scale its children. it can also contain leaves, which are drawable things.
    groups = [qgl.scene.Group(),qgl.scene.Group()]
    #leaves are added to the group. The texture leaf loads a texture image ready for drawing. Any quads leaves, which are drawn 
    #after a texture leaf will be rendered with the texture image.
    #texture = qgl.scene.state.Texture("land.jpg")
    #quad = qgl.scene.state.Quad((100,100))
    #Now we add the different nodes and leaves into a tree structure using the .add method.
    root_node.add(viewport)
    viewport.add(*groups)
    #groups[0].add(texture, quad)
    #groups[1].add(texture, quad)
    #seperate the groups visually.
    #groups[0].translate = (-200,0,-50)
    #groups[1].translate = (200,0,0)    
    #If we want a group to be picked up by the picker visitor, it must have its selectable flag set.
    #groups[0].selectable = True
    #groups[1].selectable = True
    
    #Before the structure can be drawn, it needs to be compiled. To do this, we ask the root node to accept the compiler visitor.
    #If any new nodes are added later in the program, they must also accept the compiler visitor before they can be drawn.
    root_node.accept(compiler)
    
    #the main render loop
    while True:
        #process pygame events.
        selected=[]
        for event in pygame.event.get():
            if event.type is QUIT:
                return
            elif event.type is KEYDOWN:
                menu.keydown(event)                    
            elif event.type is KEYUP:
                menu.keyup(event)
            elif event.type is MOUSEMOTION:
                picker.set_position(event.pos)
                root_node.accept(picker)
                menu.moves(picker.hits)
                        
            elif event.type is MOUSEBUTTONDOWN:
                #tell the picker we are interested in the area clicked by the mouse
                picker.set_position(event.pos)
                #ask the root node to accept the picker.
                root_node.accept(picker)
                #picker.hits will be a list of nodes which were rendered at the position.
                #to visualise which node was clicked, lets adjust its angle by 10 degrees.
                for hit in picker.hits:
                    print menu.get(hit)
            elif event.type is MOUSEBUTTONUP:
                #tell the picker we are interested in the area clicked by the mouse
                picker.set_position(event.pos)
                #ask the root node to accept the picker.
                root_node.accept(picker)
                #picker.hits will be a list of nodes which were rendered at the position.
                #to visualise which node was clicked, lets adjust its angle by 10 degrees.
                for hit in picker.hits:
                    menu.release(hit)
        
        #ask the root node to accept the render visitor. This will draw the structure onto the screen.
        #notice that QGL draws everything from the centre, and that the 0,0 point in a QGL screen is the center of the screen.
        root_node.accept(render)
        
        #flip the display
        pygame.display.flip()


main()


import engine, pygame
from pygame.locals import *
from world import *

def getpos(what):
    return (what.position.x, what.position.y)
    
BAR_START = 0
BAR_END = 1

class Simulator(engine.Scene):
    def init(self, *args, **kwargs):
        self.world = World()
        self.view = engine.View(self.game, 0,0, 1)
        self.setup_level(*args, **kwargs)
        self.state = BAR_START
        self.stack = []
        
    def setup_level(self):
        self.world.add_active( Generator((0,10)) )
        self.world.add_passive( Segment(-10,20,10,20) )
        self.world.add_passive( Goal(0,60,15.) )
        self.world.add_passive( Floor(-200) )
        
    def event(self, evt):
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                self.end()
            if evt.key == K_z:
                self.view.scale(1.0/1.1)
            if evt.key == K_x:
                self.view.scale(1.1)
        elif evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                if self.state == BAR_START:
                    self.stack.append( evt.pos )
                    self.state = BAR_END
                elif self.state == BAR_END:
                    start = self.view.from_screen(self.stack.pop())
                    end = self.view.from_screen(evt.pos)
                    if not start==end:
                        self.world.add_passive( 
                            Segment( start[0], start[1], end[0], end[1] )
                            )
                    self.state = BAR_START
                
    def loop(self, dt):
        self.world.loop(dt/100.0)
        for evt in self.world.get_events():
            pass
            
    def update(self):
        self.game.screen.blit( self.background, (0,0) ) 
        for b in self.world.balls:
            pygame.draw.circle( 
                self.game.screen,
                (255,255,255),
                self.view.to_screen( getpos(b) ) ,
                self.view.scale_to_screen( 3 ) , 
                )
        for s in self.world.passive:
            if isinstance(s, Segment):
                pygame.draw.line( 
                    self.game.screen,
                    (255,255,255),
                    self.view.to_screen( s.segment.p1 ) ,
                    self.view.to_screen( s.segment.p2 ) ,
                    )
            if isinstance(s, Goal):
                pygame.draw.circle( 
                    self.game.screen,
                    (0,0,255),
                    self.view.to_screen( s.segment.c ) ,
                    self.view.scale_to_screen( s.segment.r ) , 
                    )
                
        if self.state == BAR_END:
            pygame.draw.line( 
                    self.game.screen,
                    (255,255,255),
                    self.stack[-1] ,
                    pygame.mouse.get_pos() ,
                    )
                    
            
def main():
    g = engine.Game(800, 600, framerate = 20, title = "simulator")
    g.run( Simulator(g) ) 
    
if __name__ == "__main__":
    main()    
import engine, pygame
from pygame.locals import *
from world import *

def getpos(what):
    return (what.position.x, what.position.y)
    
BAR_START = 0
BAR_END = 1
class LevelEnd:
    def __init__(self, win, score):
        self.win = win
        self.score = score
        
        
class Simulator(engine.Scene):
    lives = 100
    name = "Level One"
    target = 20
    
    def init(self, *args, **kwargs):
        self.world = World()
        self.view = engine.View(self.game, 0,0, 1)
        self.setup_level(*args, **kwargs)
        self.state = BAR_START
        self.goal = 0
        self.lost = 0
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
                    start, end = self.new_segment( 
                        self.view.from_screen(self.stack.pop()),
                        self.view.from_screen(evt.pos)
                        )
                    if not start==end:
                        self.world.add_passive( 
                            Segment( start[0], start[1], end[0], end[1] )
                            )
                    self.state = BAR_START
                
    def loop(self, dt):
        self.world.loop(dt/100.0)
        for evt in self.world.get_events():
            if isinstance(evt, BallAtGoal):
                self.goal += 1
            if isinstance(evt, BallLost):
                self.lost += 1                
        if self.lost > self.lives:
            self.end( LevelEnd(False, 0) )
        if self.goal > self.target:
            self.end( LevelEnd(True, self.goal * 2 - self.lost) )
            
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
            start, end = self.new_segment( 
                    self.view.from_screen( self.stack[-1] ),
                    self.view.from_screen( pygame.mouse.get_pos() ),
                   )
            start = self.view.to_screen( start )
            end = self.view.to_screen( end )            
            pygame.draw.line( 
                    self.game.screen,
                    (255,255,255),
                    start ,
                    end ,
                    )
        self.log("goal:   "+str(self.goal))
        self.log("lost:   "+str(self.lost))
        self.log("alive:  "+str(len(self.world.balls)))
        self.log("fps:    "+str( self.game.clock.get_fps() ))
    
    
    def new_segment(self, start, end):
        if start == end: return start, start+Vector2(100,0)
        s = LineSegment2( Point2(*start), Point2(*end) )
        v = s.v.normalized()
        v *= 100
        return s.p1, s.p1+v
    
    
class LevelOne(Simulator):
    lives = 100
    name = "Level One"
    target = 20
    
    def setup_level(self):
        self.world.add_active( Generator((0,10)) )
        self.world.add_passive( Segment(-10,20,10,20) )
        self.world.add_passive( Goal(0,60,15.) )
        self.world.add_passive( Floor(-200) )

class LevelTwo(Simulator):
    lives = 100
    name = "Level Two"
    target = 20
    
    def setup_level(self):
        self.world.add_active( Generator((0,10)) )
        self.world.add_passive( Segment(-100,20,100,20) )
        self.world.add_passive( Goal(0,60,15.) )
        self.world.add_passive( Floor(-200) )

class Runner(engine.Scene):
    log_font_size = 40
    PRE_LEVEL = 0
    POST_LEVEL = 1
    LOST = 2
    WON  = 3
    
    levels = [
            LevelOne,
            LevelTwo,
        ]
    def init(self):
        self.state = self.PRE_LEVEL
        self.current_level = 0
        self.score = 0
        
    def event(self, evt):
        if self.state == self.PRE_LEVEL:
            if evt.type == KEYDOWN:
                self.result = self.runScene( self.levels[self.current_level](self.game) )
                if self.result.win:
                    self.score += self.result.score
                    self.current_level += 1
                    if len(self.levels) <= self.current_level:
                        self.state = self.WON
                    else:
                        self.state = self.POST_LEVEL
                else:
                    self.state = self.LOST
                
                
        elif self.state == self.POST_LEVEL:
            if evt.type == KEYDOWN:
                self.state = self.PRE_LEVEL
                
        elif self.state == self.LOST:
            if evt.type == KEYDOWN:
                self.end()
                
        elif self.state == self.WON:
            if evt.type == KEYDOWN:
                self.end()
                
    def update(self):
        self.game.screen.blit(self.background, (0,0) )
        if self.state == self.PRE_LEVEL:
            self.log("next level")
            self.log( "level: "+self.levels[self.current_level].name )
            self.log( "score: "+str(self.score))
        if self.state == self.POST_LEVEL:
            self.log("level finished")
            self.log( "score: "+str(self.score))
        if self.state == self.LOST:
            self.log("you lost")
            self.log( "score: "+str(self.score))
        if self.state == self.WON:
            self.log("you won")
            self.log( "score: "+str(self.score))
                
def main():
    g = engine.Game(800, 600, framerate = 20, title = "simulator")
    g.run( Runner(g) ) 
    
if __name__ == "__main__":
    main()    
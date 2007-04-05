import view
from world import *

class LevelOne(view.View):
    lives = 100
    name = "Level One"
    target = 20
    
    def setup_level(self):
        self.addGenerator((0,10))
        self.addSegment(-10,20,10,20) 
        self.addGoal(0,60,15.) 
        #self.addFloor(-200)
        view.View.setup_level()

class LevelTwo(view.View):
    lives = 100
    name = "Level Two"
    target = 20
    
    def setup_level(self):
        self.addGenerator((0,10))
        self.addSegment(-100,20,100,20)
        self.addGoal(0,60,15.) )
        view.View.setup_level()

class LevelThree(view.View):
    lives = 100
    name = "Level Three"
    target = 20
    
    def setup_level(self):
        self.world.add_active( Generator((0,10)) )
        self.world.add_passive( Segment(-100,20,100,20) )
        self.world.add_passive( LimitedLifeSegment(-100,20,0,100, life=5) )
        self.world.add_passive( LimitedLifeSegment(0,100,100,20, life=5) )
        self.world.add_passive( Goal(0,60,15.) )
        view.View.setup_level()

class LevelFour(view.View):
    lives = 100
    name = "Level Four"
    target = 20
    
    def setup_level(self):
        self.world.add_active( Generator((0,10)) )
        self.world.add_passive( Segment(-100,20,100,20) )
        self.world.add_passive( LimitedLifeSegment(-100,20,0,100, life=5) )
        self.world.add_passive( LimitedLifeSegment(0,100,100,20, life=5) )
        self.world.add_attractor( Attractor(-100,20, force=-50) )
        self.world.add_attractor( Attractor(5,-50, force=50) )
        self.world.add_attractor( Attractor(100,20, force=-50) )
        self.world.add_passive( Goal(0,60,15.) )
        self.world.add_passive( Floor(-200) )
        

import euclid
import time

gravity = euclid.Vector2(0,-9.81/10) # m/s**2

class Ball:
    def __init__(self, world, position, velocity=euclid.Vector2(0,0)):
        self.world = world
        self.position = position
        self.velocity = velocity
        
    def loop(self, delta):
        self.velocity += gravity*delta
        start = self.position
        movement = self.velocity*delta
        
        collision = True
        last = None
        while collision:
            collision = self.world.collide(self.position, movement, last)

            if not collision:
                self.position = start + movement
            else:
                start = collision.where
                last = collision.who
                movement = collision.movement_left
                self.velocity = collision.reflect(self.velocity)
                
    def __repr__(self):
        return "<ball: p=%s v=%s>"%(str(self.position), str(self.velocity))
            
class Collision:
    where = None
    movement_left = None
    def reflect(self, what):
        raise NotImplementedError()
        
class FloorCollision(Collision):
    def __init__(self, who, where, position, movement):
        self.who = who
        self.where = where
        self.movement_left = self.reflect((position+movement)-where)
        
    def reflect(self, vector):
        return euclid.Vector2(
                vector.x, -vector.y
            )
    
class Object:
    def set_world(self, world):
        self.world = world
                
class Floor(Object):
    def __init__(self, height = 0):
        self.height = height

    
    def collide(self, position, movement):
        if  (
                position.y >= self.height 
                and (position+movement).y < self.height
            ) or (
                position.y < self.height 
                and (position+movement).y >= self.height
            ):
            print "collide"
            where = euclid.Vector2(self.height, position.y)
            return FloorCollision(self, where, position, movement)
            
class World:
    def __init__(self):
        self.balls = []
        self.active = []
        self.passive = []
        
        self.init()
        
    def init(self): pass
    
    def add_ball(self, x, y):
        ball = Ball(self, euclid.Vector2(x, y) )
        self.balls.append( ball )

    def add_passive(self, what):
        what.set_world( self )
        self.passive.append( what )
        
        
    def loop(self, delta):
        for o in self.balls: o.loop(delta)
        for o in self.active: o.loop(delta)
        
    def collide(self, position, movement, last=None):
        colls = []
        for l in [self.active, self.passive]:
            for o in l:
                if not o == last:
                    c = o.collide(position, movement)
                    if c:
                        colls.append( c )
        if colls:
            return colls[0]                
        return None
        
    
if __name__ == "__main__":
    w = World()
    w.add_ball( 1, 10 )
    w.add_passive( Floor(0) )
    dt = 1
    print "Start..."
    while True:
        time.sleep(dt)
        w.loop(dt)
        print ">>", w.balls
         
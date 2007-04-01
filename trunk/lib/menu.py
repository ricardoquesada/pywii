import qgl
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import menu_item

class Menu:
    
    def __init__(self, scene, items):
        
        self.items = items
        self.index = 0
        self._create_items_text(scene, items)

    def update(self):
        for x in self.instances:
            x.update()
    
    def update_event(self, event):
        
        if event.type == MOUSEMOTION:
            self.on_mouse_motion(event)
        elif event.type == MOUSEBUTTONDOWN:
            self.on_mouse_click(event)
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.move_down()
            elif event.key == K_UP:
                self.move_up()

    def on_mouse_motion(self, event):
        pass

    def on_mouse_click(self, event):
        pass

    def move_down(self):
        self._move(1)

    def move_up(self):
        self._move(-1)

    def _move(self, dy):

        self.instances[self.index].leave()
        self.index += dy
        max = len(self.items) - 1

        if self.index < 0:
            self.index = max
        elif self.index > max:
            self.index = 0

        self.instances[self.index].enter()


    def _create_items_text(self, scene, items):
        
        dy = 0
        self.instances = []
        for (i, _) in items:
            new = menu_item.MenuItem(i, 0.0, -dy)
            scene.add_group(new.group)
            dy += 60
            self.instances.append(new)
        scene.accept()


if __name__ == '__main__':
    
    m = Menu([('uno', None), ('dos', None)])
    m.move_up()
    print m.index

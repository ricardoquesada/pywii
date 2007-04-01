import qgl
from OpenGL.GL import *
from OpenGL.GLU import *

class Triangle(qgl.scene.Leaf):
    def __init__(self, v):
        self.vertices = v

    def compile(self):
        lst = qgl.render.GLDisplayList()
        glNewList(lst.id, GL_COMPILE)

        v = self.vertices
        glBegin(GL_TRIANGLES)
        glColor4f(1,1,1,1)
        glVertex2f(v[0][0],v[0][1])
        glVertex2f(v[1][0],v[1][1])
        glVertex2f(v[2][0],v[2][1])
        glEnd()

        glEndList()
        self.list = lst

    def execute(self):
        glCallList(self.list.id)

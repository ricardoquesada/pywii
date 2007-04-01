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
        glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        glEnable ( GL_COLOR_MATERIAL )
        glBegin(GL_TRIANGLES)
        glColor4f(1.0, 0.6, 0.0, 0.2)
        glVertex2f(v[0][0],v[0][1])
        glVertex2f(v[1][0],v[1][1])
        glVertex2f(v[2][0],v[2][1])
        glEnd()
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glDisable ( GL_COLOR_MATERIAL )

        glEndList()
        self.list = lst

    def execute(self):
        glCallList(self.list.id)

class PorcionMuzza(qgl.scene.Leaf):
    def __init__(self, v):
        self.vertices = v

    def compile(self):
        lst = qgl.render.GLDisplayList()
        glNewList(lst.id, GL_COMPILE)

        v = self.vertices
        glColorMaterial ( GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        glEnable ( GL_COLOR_MATERIAL )
        glBegin(GL_TRIANGLE_STRIP)
        glColor4f(1.0, 0.6, 0.0, 0.2)
        glVertex2f(v[0][0],v[0][1])
        glColor4f(1.0, 0.6, 0.0, 0.6)
        glVertex2f(v[1][0],v[1][1])
        glVertex2f(v[2][0],v[2][1])
        glVertex2f(v[3][0],v[3][1])
        glVertex2f(v[4][0],v[4][1])
        glEnd()
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glDisable ( GL_COLOR_MATERIAL )

        glEndList()
        self.list = lst

    def execute(self):
        glCallList(self.list.id)

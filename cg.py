#viewer3d_triangle.py
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from CGAL.CGAL_Kernel import Point_3
from CGAL import Point_generators_3
import random
def drawPoint(x, y, z):
     glBegin(GL_QUADS)
     glVertex3f(x-0.1,y-0.1,z)
     glVertex3f(x-0.1,y+0.1,z)
     glVertex3f(x+0.1,y+0.1,z)
     glVertex3f(x+0.1,y-0.1,z)
     glEnd()
def genereatePointsInCube(vertexes):
    for i in range(1,random.randint(10,20)):
        vertexes.append((random.uniform(-1, 1),random.uniform(-1, 1),random.uniform(-1, 1)))
def genereatePointsInSphere():
    Point_generators_3.Random_points_in_sphere_3()
class Viewer(QGLViewer):
    vertexes = [(1,1,1),(1,1,-0.5),
    (1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1,-1)]
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
    def draw(self):
        for i in self.vertexes:
            drawPoint(*i)
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if (e.nativeVirtualKey()==Qt.Key_W):
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif (e.nativeVirtualKey()==Qt.Key_F):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif(e.nativeVirtualKey()==Qt.Key_E):
            self.vertexes = []
        elif(e.nativeVirtualKey()==Qt.Key_Q):
            self.vertexes = [(1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1, 1,-1)]
        elif(e.nativeVirtualKey()==Qt.Key_R):
            genereatePointsInCube(self.vertexes)
        elif(e.nativeVirtualKey()==Qt.Key_S):
           genereatePointsInSphere()
        self.updateGL()


 
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()



from __future__ import print_function
from CGAL.CGAL_Kernel import Point_2
from CGAL import CGAL_Convex_hull_2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *
from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Kernel import Plane_3
from CGAL import CGAL_Convex_hull_3
from CGAL.CGAL_Polyhedron_3 import Polyhedron_3
import random
def genereatePointsInSphere(vertexes):
    R = 5
    for i in range(1,100):
        vertexes.append(Point_3(R*random.uniform(0,1)*random.uniform(-1,1), R*random.uniform(0,1)*random.uniform(-1,1), R*random.uniform(0,1)))
def showFigure(vertexes):
    glPointSize(12)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_LINE_LOOP)
    glColor3d(1,0,0);
    for i in vertexes:
        glVertex2d(i.x(), i.y())
    glEnd()
def showPoints(vertexes):
    glPointSize(12)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_POINTS)
    glColor3d(1,1,0);
    for i in vertexes:
        glVertex2d(i.x(), i.y())
    glEnd()
def showPoints3d(vertexes):
    glPointSize(12)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_POINTS)
    glColor3d(1,1,0);
    for i in vertexes:
        glVertex3d(i.x(), i.y(), i.z())
    glEnd()

def showFigure3d(vertexes):
    glPointSize(12)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_LINE_LOOP)
    glColor3d(1,0,0);
    for i in vertexes.facets():
        j = i.halfedge().next()
        while(j.vertex().point() != i.halfedge().vertex().point()):
            glVertex3d(j.vertex().point().x(), j.vertex().point().y(), j.vertex().point().z())
            j = j.next()
    glEnd()
class Viewer(QGLViewer):
    vertexes = []
    result = []
    pts = []
    show2dPoints = True
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
        self.vertexes = []
        self.vertexes.append(Point_2(0, 0))
        self.vertexes.append(Point_2(1, 0))
        self.vertexes.append(Point_2(0, 1))
        self.vertexes.append(Point_2(1, 1))
        self.vertexes.append(Point_2(0.5, 0.5))
        self.vertexes.append(Point_2(0.25, 0.25))
        genereatePointsInSphere(self.pts)
    def draw(self):
        if(self.show2dPoints):
            showPoints(self.vertexes)
            showFigure(self.result)
        else:
            showPoints3d(self.pts)
            showFigure3d(self.result)
            
    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if(e.nativeVirtualKey()==Qt.Key_A):
            self.res = []
            CGAL_Convex_hull_2.convex_hull_2(self.vertexes, self.result)
            self.show2dPoints = True
        elif(e.nativeVirtualKey()==Qt.Key_E):
            self.result = Polyhedron_3()
            CGAL_Convex_hull_3.convex_hull_3(self.pts, self.result)
            self.show2dPoints = False
        self.updateGL()


 
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()



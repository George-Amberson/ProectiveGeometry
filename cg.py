#viewer3d_triangle.py
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *

import random
def drawPoint(x, y, z):
     glPointSize(12)
     glEnable(GL_POINT_SMOOTH)
     glBegin(GL_POINTS)
     glVertex3f(x,y,z)
     glEnd()
def genereatePointsInCube(vertexes):
    for i in range(1,random.randint(10,20)):
        vertexes.append((random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)))
def genereatePointsInSphere(vertexes):
    
    R = 5
    for i in range(1,100):
        vertexes.append((R*random.uniform(0,1)*random.uniform(-1,1), R*random.uniform(0,1)*random.uniform(-1,1), R*random.uniform(0,1)))
class Viewer(QGLViewer):
    vertexes = [
        (0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)
    ]
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
    def draw(self):
        print(self.vertexes)
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
            self.vertexes = [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]
        elif(e.nativeVirtualKey()==Qt.Key_R):
            genereatePointsInCube(self.vertexes)
        elif(e.nativeVirtualKey()==Qt.Key_S):
           self.vertexes = []
           genereatePointsInSphere(self.vertexes)
        self.updateGL()


 
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()


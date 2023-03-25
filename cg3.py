from __future__ import print_function
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQGLViewer import *
from OpenGL.GL import *

def clamp(value, minval, maxval):
    return max(minval, min(value, maxval))

class BSpline:
    pointNum = 0
    def __init__(self, reference_points, discrete_num = 10, closed = False):
        self.points = reference_points
        self.d_num = int(discrete_num)
        self.closed = closed
        self.pointNum = 0
        # Генерация коэффициентов для сгенеренных вершин B-сплайна 3 порядка
        self.coefs = [];
        for i in range(self.d_num):
            spline_segm_coef = self.calc_spline3_coef(i/self.d_num)
            self.coefs.append(spline_segm_coef)
    def leftPoint(self):
        self.pointNum = (self.pointNum + 1) % len(points)
    def rightPoint(self):
        if(self.pointNum <0): self.pointNum = len(points)
        self.pointNum = self.pointNum - 1

    def upgradeValue(self):
        self.points = self.points[0:self.pointNum]+tuple([self.points[self.pointNum][0] + 0.1, self.points[self.pointNum][1] +0.1, self.points[self.pointNum][2] +0.1])+ self.points[self.pointNum+1:]
        
    def downgradeValue(self):
        self.points = self.points[0:self.pointNum]+tuple([self.points[self.pointNum][0] - 0.1, self.points[self.pointNum][1] -0.1, self.points[self.pointNum][2] -0.1])+ self.points[self.pointNum+1:]
    def calc_spline3_coef(self, t):
        coefs = [0,0,0]
        coefs[0] = (1.0-t)*(1.0-t)/2.0;
        coefs[1] = (-2*t**2+2*t+1)/2.0;
        coefs[2] = (t**2)/2.0;
        return coefs
    
    def draw_spline_curve(self):
        if not self.closed:     
            segmentsCount = len(self.points) - 1
            glBegin(GL_LINE_STRIP)
        else:
            segmentsCount = len(self.points) #Сегмент между первой и последней вершиной
            glBegin(GL_LINE_LOOP)  
        glColor3f(1.0, 1.0, 0.0)
        for i in range(segmentsCount):
            self.draw_glvertex_for_one_segment_of_spline(i);
        glEnd()

    def draw_glvertex_for_one_segment_of_spline(self, segment_id):
        pNum = len(self.points)
        # Вычисление номеров вершин в списке вершин для построения сплайна
        if not self.closed:
            p0 = clamp(segment_id - 1, 0, pNum - 1)
            p1 = clamp(segment_id, 0, pNum - 1)
            p2 = clamp(segment_id + 1, 0, pNum - 1)
        else:
            p0 = (segment_id - 1 + pNum) % pNum
            p1 = (segment_id + pNum) % pNum
            p2 = (segment_id + 1 + pNum) % pNum
        # По заранее вычисленным коэффициентам 
        # вычисляем промежуточные точки сплайна
        # и выводим их в OpenGL
        for i in range(self.d_num):
            x = self.coefs[i][0] * self.points[p0][0] \
                + self.coefs[i][1] * self.points[p1][0] \
                + self.coefs[i][2] * self.points[p2][0] 
            y = self.coefs[i][0] * self.points[p0][1] \
                + self.coefs[i][1] * self.points[p1][1] \
                + self.coefs[i][2] * self.points[p2][1] 
            z = self.coefs[i][0] * self.points[p0][2] \
            + self.coefs[i][1] * self.points[p1][2] \
            + self.coefs[i][2] * self.points[p2][2] 
 
            glVertex3f(x, y, z)

# Make spline
points = ((0,0,0),(0,3,0),(1,3,0),(1,1,0),(2,1,0),(3,2,0),(3,0,0))
spline =  BSpline(points, 10, False)

class Viewer(QGLViewer):
    
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)

    def keyPressEvent(self,e):
        modifiers = e.modifiers()
        if(e.nativeVirtualKey()==Qt.Key_W):
            spline.upgradeValue()
        elif(e.nativeVirtualKey()==Qt.Key_S):
            spline.downgradeValue()
        elif(e.nativeVirtualKey()==Qt.Key_A):
            spline.leftPoint()
        elif(e.nativeVirtualKey()==Qt.Key_D):
            spline.rightPoint()
        self.updateGL()
        
    def draw(self):
        spline.draw_spline_curve()
        
  
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()

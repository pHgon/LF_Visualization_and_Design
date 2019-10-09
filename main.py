from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys
from lf import Ui_MainWindow 

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.angulo_horizontal = 7
        self.angulo_vertical = 7
        self.pathToPpms = ""
        self.grid_x = 20
        self.grid_y = 60
        self.grid_w = 150
        self.grid_h = 150
        self.setupUi(self)
        self.l_ang_hoz.setText("x: " + "{0:0>3}".format(str(self.angulo_horizontal)))
        self.l_ang_vert.setText("y: " + "{0:0>3}".format(str(self.angulo_vertical)))
        self.actionOpen.triggered.connect(self.openFile)
    

    def openFile(self):
        s = QFileDialog.getExistingDirectory(self, "Open a folder", "./")
        self.pathToPpms = str(s)
        self.openppm()
    
    def get_vert_ang(self):
        return self.angulo_vertical  

    def get_horz_ang(self):
        return self.angulo_horizontal

    def openppm(self):
        self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/00" + str(self.get_vert_ang()) + "_00" + str(self.get_horz_ang()) + ".ppm"))
    
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        # self.drawRectangles(qp)
        self.drawGrid(qp)
        qp.end()

    def drawGrid(self, qp):   
        qp.setBrush(QColor(255 , 255, 255))
        qp.drawRect(self.grid_x, self.grid_y, self.grid_w, self.grid_h)

        for i in range(self.grid_x, self.grid_x + self.grid_w + int(self.grid_h/15), int(self.grid_w/15)):
            qp.setPen(QColor(0, 0, 0))
            qp.drawLine(i, self.grid_y, i, self.grid_y + self.grid_h)
        for i in range(self.grid_y, self.grid_y + self.grid_h + int(self.grid_h/15), int(self.grid_h/15)):
            qp.setPen(QColor(0, 0, 0))
            qp.drawLine(self.grid_x, i, self.grid_x + self.grid_w, i)
        qp.setBrush(QColor(255, 0, 0))
        qp.drawRect(self.grid_x + int(self.grid_w/15)*self.angulo_horizontal, self.grid_y + int(self.grid_h/15)*self.angulo_vertical, int(self.grid_w/15), int(self.grid_h/15))
            


    # def drawRectangles(self, qp):
      
    #     col = QColor(0, 0, 0)
    #     col.setNamedColor('#d4d4d4')
    #     qp.setPen(col)

    #     qp.setBrush(QColor(200, 0, 0))
    #     qp.drawRect(10, 15, 90, 60)

    #     qp.setBrush(QColor(255, 80, 0, 160))
    #     qp.drawRect(130, 15, 90, 60)

    #     qp.setBrush(QColor(25, 0, 90, 200))
    #     qp.drawRect(250, 15, 90, 60)
    
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Left:
            if(self.angulo_horizontal > 0):
                self.angulo_horizontal -= 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm").scaled(625,434,aspectRatioMode =1))

            

        if event.key() == QtCore.Qt.Key_Right:
            if(self.angulo_horizontal < 14):
                self.angulo_horizontal += 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm").scaled(625,434,aspectRatioMode =1))
           

        if event.key() == QtCore.Qt.Key_Up:
            if(self.angulo_vertical > 0):
                self.angulo_vertical -= 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm").scaled(625,434,aspectRatioMode =1))
            
            

        if event.key() == QtCore.Qt.Key_Down:
            if(self.angulo_vertical  < 14):
                self.angulo_vertical += 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm").scaled(625,434,aspectRatioMode =1))
        self.l_ang_hoz.setText("x: " + "{0:0>3}".format(str(self.angulo_horizontal)))
        self.l_ang_vert.setText("y: " + "{0:0>3}".format(str(self.angulo_vertical)))
        self.update()
     

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    #form.open_ppm()

if __name__ == '__main__':
    main()
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
        self.pathToPpms = "/home/paulo/Downloads/Bikes/Bikes"
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
            
    
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Left:
            if(self.angulo_horizontal > 0):
                self.angulo_horizontal -= 1
            self.loadppm() 

        if event.key() == QtCore.Qt.Key_Right:
            if(self.angulo_horizontal < 14):
                self.angulo_horizontal += 1
            self.loadppm()

        if event.key() == QtCore.Qt.Key_Up:
            if(self.angulo_vertical > 0):
                self.angulo_vertical -= 1
            self.loadppm()

        if event.key() == QtCore.Qt.Key_Down:
            if(self.angulo_vertical  < 14):
                self.angulo_vertical += 1
            self.loadppm()

        self.l_ang_hoz.setText("x: " + "{0:0>3}".format(str(self.angulo_horizontal)))
        self.l_ang_vert.setText("y: " + "{0:0>3}".format(str(self.angulo_vertical)))
        self.update()


    def loadppm(self):
        act_img = QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm")
        n_width  = int(act_img.width() * (self.label.width() / act_img.width()))       # Scaling para o tamanho maximo 
        n_height  = int(act_img.height() * (self.label.height() / act_img.height()))   # permitido dentro do label
        self.label.setPixmap(act_img.scaled(n_width,n_height,aspectRatioMode =1))
     

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    #form.open_ppm()

if __name__ == '__main__':
    main()
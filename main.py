#!/usr/local/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys
import os
from lf import Ui_MainWindow
import qimage2ndarray
import img_manipulation as im
import utils
import numpy as np

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.angulo_horizontal = 0
        self.angulo_vertical = 0
        self.pathToPpms = "/home/paulo/Downloads/Bikes/Bikes"  # Caminho so para testes, default=""
        self.pathToPpms = ""

        if self.pathToPpms:
            self.angulo_horizontal = 7
            self.angulo_vertical = 7
            self.loadppm()

        self.grid_x = 240
        self.grid_y = 65
        self.grid_w = 150
        self.grid_h = 150
        self.setScreenText()
        self.actionOpen.triggered.connect(self.openFile)
        # Sinais
        self.pushButton_3.clicked.connect(self.buttonUpscaling2x)
        self.pushButton_4.clicked.connect(self.buttonUpscaling4x)
        self.horizontalSlider.valueChanged.connect(self.loadppm)
        self.horizontalSlider_2.valueChanged.connect(self.loadppm)
        self.horizontalSlider_3.valueChanged.connect(self.loadppm)
    

    def setScreenText (self):
        self.l_ang_hoz.setText("x: " + "{0:0>2}".format(str(self.angulo_horizontal)))
        self.l_ang_ver.setText("y: " + "{0:0>2}".format(str(self.angulo_vertical)))


    def openFile(self):
        s = QFileDialog.getExistingDirectory(self, "Open a folder", "./")
        self.pathToPpms = str(s)
        self.angulo_horizontal = 7
        self.angulo_vertical = 7
        self.setScreenText()
        self.loadppm()
        self.update()

    
    # Carrega o ppm e ajusta para o tamanho da label
    def loadppm(self):
        act_img = QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm")
        n_width   = int(act_img.width()  * (self.label.width()  / act_img.width()))       # Scaling para o tamanho maximo 
        n_height  = int(act_img.height() * (self.label.height() / act_img.height()))      # permitido dentro do label

        temp_img = qimage2ndarray.rgb_view(act_img.toImage())

        temp_img = im.brightness(temp_img, 1, -50 + self.spinBox_brilho.value())
        temp_img = im.exposure(temp_img, self.spinBox_saturacao.value()/100.)

        temp_img = qimage2ndarray.array2qimage(temp_img)
        act_img = QtGui.QPixmap.fromImage(temp_img)

        self.label.setPixmap(act_img.scaled(n_width,n_height,aspectRatioMode =1))


    def drawGrid(self, qp):   
        qp.setBrush(QColor(170, 170, 170))
        qp.drawRect(self.grid_x, self.grid_y, self.grid_w, self.grid_h)
        for i in range(self.grid_x, self.grid_x + self.grid_w + int(self.grid_h/15), int(self.grid_w/15)):
            qp.setPen(QColor(0, 0, 0))
            qp.drawLine(i, self.grid_y, i, self.grid_y + self.grid_h)
        for i in range(self.grid_y, self.grid_y + self.grid_h + int(self.grid_h/15), int(self.grid_h/15)):
            qp.setPen(QColor(0, 0, 0))
            qp.drawLine(self.grid_x, i, self.grid_x + self.grid_w, i)
        qp.setBrush(QColor(255, 0, 0))
        if self.pathToPpms:
            qp.drawRect(self.grid_x + int(self.grid_w/15)*self.angulo_horizontal, self.grid_y + int(self.grid_h/15)*self.angulo_vertical, int(self.grid_w/15), int(self.grid_h/15))
    
    
# ******************************************* EVENTOS ******************************************* #
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        qp.end()


    def keyPressEvent(self,event):
        if self.pathToPpms:
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

            self.setScreenText()
        self.update()


    def mousePressEvent(self, event):
        pass


    def mouseReleaseEvent(self, event):
        pass


    def mouseMoveEvent(self, event):
        pass


# ********************************************************************************************* #

    def buttonUpscaling2x(self):
        self.upscaling(2)

    
    def buttonUpscaling4x(self):
        self.upscaling(4)


    def upscaling(self, x):
        if utils.isValidSAI(self.angulo_horizontal, self.angulo_vertical):
            os.system('rm -R _tempSAIs; mkdir _tempSAIs')
            sai_it = 0
            for y in range (self.angulo_vertical-1, self.angulo_vertical+2):
                for x in range (self.angulo_horizontal-1, self.angulo_horizontal+2):
                    act_img = QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(x))) + "_" + ("{0:0>3}".format(str(y))) + ".ppm")
                    act_img.save("_tempSAIs/" + str(sai_it) + ".png", "PNG")
                    sai_it = sai_it + 1
            # Chama Funcao Upscaling
            #os.system('rm -R _tempSAIs')
        

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
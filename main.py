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
import mosca_window

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.angulo_horizontal = 0
        self.angulo_vertical = 0
        #self.pathToPpms = "/home/stormtrooper/Thiago/Mestrado/Bikes/Bikes"
        # Caminho so para testes, default=""
        self.pathToPpms = ""

        if self.pathToPpms:
            self.angulo_horizontal = 7
            self.angulo_vertical = 7
            self.loadppm()

        self.grid_x = 261
        self.grid_y = 62
        self.grid_w = 150
        self.grid_h = 150
        self.setScreenText()
        self.actionOpen.triggered.connect(self.openFile)
        # Sinais
        self.pushButton.clicked.connect(self.buttonDepthMap)
        self.pushButton_3.clicked.connect(self.buttonUpscaling2x)
        self.pushButton_4.clicked.connect(self.buttonUpscaling4x)
        self.pushButton_5.clicked.connect(self.mosca)
        self.slider_brilho.valueChanged.connect(self.loadppm)
        self.slider_contraste.valueChanged.connect(self.loadppm)
        self.slider_saturacao.valueChanged.connect(self.loadppm)
        self.slider_nitidez.valueChanged.connect(self.loadppm)
        self.radioButton_red.clicked.connect(self.loadppm)
        self.radioButton_green.clicked.connect(self.loadppm)
        self.radioButton_blue.clicked.connect(self.loadppm)
        self.radioButton_maximizar.clicked.connect(self.loadppm)
        self.radioButton_original.clicked.connect(self.loadppm)


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
        # form = mosca_window.MoscaWindow()
        # form.show()
        act_img = QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm")
        act_img, act_hist = self.applyTransformations(act_img)

        img_width  = act_img.width()
        img_height = act_img.height()
        if self.radioButton_maximizar.isChecked():
            img_width    = int(img_width  * (self.label.width()  / img_width))       # Scaling para o tamanho maximo 
            img_height   = int(img_height * (self.label.height() / img_height))      # permitido dentro do label
        hist_width   = int(act_hist.width()  * (self.label_hist.width()  / act_hist.width()))       # Scaling para o tamanho maximo 
        hist_height  = int(act_hist.height() * (self.label_hist.height() / act_hist.height()))      # permitido dentro do label
        
        self.label.setPixmap(act_img.scaled(img_width,img_height,aspectRatioMode =1))
        self.label_hist.setPixmap(act_hist.scaled(hist_width-10, hist_height-10))


    
    def applyTransformations(self, img_pixmap):
        img = qimage2ndarray.rgb_view(img_pixmap.toImage())
        # Valores dos Fatores
        f_br = (self.spinBox_brilho.value()+100)/100.
        f_co = (self.spinBox_contraste.value()+100)/100.
        f_sh = (self.spinBox_nitidez.value()+100)/100.
        f_sa = (self.spinBox_saturacao.value()+100)/100.
        img, hist = im.transformations(img, f_br, f_co, f_sh, f_sa, self.radioButton_red.isChecked(), self.radioButton_green.isChecked(), self.radioButton_blue.isChecked())
        img  = qimage2ndarray.array2qimage(img)
        hist = qimage2ndarray.array2qimage(hist)
        hist = hist.copy(80, 58, 496, 370)
        return QtGui.QPixmap.fromImage(img), QtGui.QPixmap.fromImage(hist)


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
    def buttonDepthMap(self):
        img1 = QtGui.QPixmap(self.pathToPpms + "/002_007.ppm")
        img2 = QtGui.QPixmap(self.pathToPpms + "/009_007.ppm")
        im.depthmap(qimage2ndarray.rgb_view(img1.toImage()), qimage2ndarray.rgb_view(img2.toImage()))

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
    
    def mosca(self):
        m = mosca_window.MoscaWindow()
        m.loadMV(self.pathToPpms, 0.5)

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
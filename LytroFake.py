#!/usr/local/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QBrush

import sys
import os
import qimage2ndarray
import numpy as np

# My GUI frames
from frames.mainframe import Ui_MainWindow
# My Functions
import functions.utils
import functions.img_manipulation as im
import functions.upsampling as us
import functions.mosca_window



def main():
    app = QApplication(sys.argv)
    form = MainFrame()
    form.show()
    sys.exit(app.exec_())


class Janela(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Janela, self).__init__(parent)
        self.setupUi(self)


class MainFrame(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)
        self.setupUi(self)

        self.matrix_rgb = [[0 for x in range(15)]for y in range(15)]  # Matriz que guarda todos os ppms em rgb_view
        self.ang_hor = 0
        self.ang_ver = 0
        self.pathToPpms = "/home/paulo/Downloads/lf_datasets/Fountain_Vincent2/Fountain_Vincent2"
        # Caminho so para testes, default=""
        #self.pathToPpms = ""

        if self.pathToPpms:
            self.ang_hor = 7
            self.ang_ver = 7
            self.openppms()

        self.grid_x = 261
        self.grid_y = 62
        self.grid_w = 150
        self.grid_h = 150
        
        self.resetUi()

        #self.dialog = Janela(self)
    

    def resetUi(self):
        self.setupUi(self)
        self.setScreenText()
        self.actionOpen.triggered.connect(self.openFile)
        # Sinais
        self.pushButton_reset.clicked.connect(self.resetUi)
        self.pushButton_depthmap.clicked.connect(self.buttonDepthMap)
        #self.pushButton_up2x.clicked.connect(self.buttonUpscaling2x)
        #self.pushButton_up4x.clicked.connect(self.buttonUpscaling4x)
        self.slider_brilho.valueChanged.connect(self.loadppm)
        self.slider_contraste.valueChanged.connect(self.loadppm)
        self.slider_saturacao.valueChanged.connect(self.loadppm)
        self.slider_nitidez.valueChanged.connect(self.loadppm)
        self.radioButton_red.clicked.connect(self.loadppm)
        self.radioButton_green.clicked.connect(self.loadppm)
        self.radioButton_blue.clicked.connect(self.loadppm)
        self.radioButton_maximizar.clicked.connect(self.loadppm)
        self.radioButton_original.clicked.connect(self.loadppm)
        #self.pushButton_roi_zigzag.clicked.connect(self.teste_janela)
        self.loadppm()


    def openFile(self):
        s = QFileDialog.getExistingDirectory(self, "Open a folder", "./")
        self.pathToPpms = str(s)
        self.resetUi()
        self.ang_hor = 7
        self.ang_ver = 7
        self.setScreenText()
        self.openppms()
        self.update()


    # Carrega todos os ppms e indexa na matriz
    def openppms(self):
        for y in range(0,15):
            for x in range (0,15):
                self.matrix_rgb[x][y] = qimage2ndarray.rgb_view(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(x))) + "_" + ("{0:0>3}".format(str(y))) + ".ppm").toImage())
        self.loadppm()


    # Carrega o ppm e ajusta para o tamanho da label
    def loadppm(self):
        act_img, act_hist = self.applyTransformations()

        img_width  = act_img.width()
        img_height = act_img.height()
        if self.radioButton_maximizar.isChecked():
            img_width    = int(img_width  * (self.label_tela.width()  / img_width))                 # Scaling para o tamanho maximo 
            img_height   = int(img_height * (self.label_tela.height() / img_height))                # permitido dentro do label
        hist_width   = int(act_hist.width()  * (self.label_hist.width()  / act_hist.width()))       # Scaling para o tamanho maximo 
        hist_height  = int(act_hist.height() * (self.label_hist.height() / act_hist.height()))      # permitido dentro do label

        self.label_tela.setPixmap(act_img.scaled(img_width,img_height,aspectRatioMode =1))
        self.label_hist.setPixmap(act_hist.scaled(hist_width-10, hist_height-10))


    
    def applyTransformations(self):
        img = self.matrix_rgb[self.ang_hor][self.ang_ver]
        # Valores dos Fatores
        f_br = (self.spinBox_brilho.value()+100)/100.
        f_co = (self.spinBox_contraste.value()+100)/100.
        f_sh = (self.spinBox_nitidez.value()+100)/100.
        f_sa = (self.spinBox_saturacao.value()+100)/100.
        img, hist = im.transformations(img, f_br, f_co, f_sh, f_sa, self.radioButton_red.isChecked(), self.radioButton_green.isChecked(), self.radioButton_blue.isChecked())
        #self.matrix_rgb[self.ang_hor][self.ang_ver] = img
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
            qp.drawRect(self.grid_x + int(self.grid_w/15)*self.ang_hor, self.grid_y + int(self.grid_h/15)*self.ang_ver, int(self.grid_w/15), int(self.grid_h/15))
    
    
# ******************************************* EVENTOS ******************************************* #
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        qp.end()


    def keyPressEvent(self,event):
        if self.pathToPpms:
            if event.key() == QtCore.Qt.Key_Left:
                if(self.ang_hor > 0):
                    self.ang_hor -= 1
                self.loadppm() 

            if event.key() == QtCore.Qt.Key_Right:
                if(self.ang_hor < 14):
                    self.ang_hor += 1
                self.loadppm()

            if event.key() == QtCore.Qt.Key_Up:
                if(self.ang_ver > 0):
                    self.ang_ver -= 1
                self.loadppm()

            if event.key() == QtCore.Qt.Key_Down:
                if(self.ang_ver  < 14):
                    self.ang_ver += 1
                self.loadppm()

            self.setScreenText()
        self.update()


    def mousePressEvent(self, event):
        pass


    def mouseReleaseEvent(self, event):
        pass


    def mouseMoveEvent(self, event):
        pass


# ****************************************** BOTÕES ******************************************* #
    def buttonDepthMap(self):
        img1 = QtGui.QPixmap(self.pathToPpms + "/002_007.ppm")
        img2 = QtGui.QPixmap(self.pathToPpms + "/009_007.ppm")
        im.depthmap(qimage2ndarray.rgb_view(img1.toImage()), qimage2ndarray.rgb_view(img2.toImage()))


    def buttonUpscaling2x(self):
        self.upscaling(2)

    
    def buttonUpscaling4x(self):
        self.upscaling(4)


    def upscaling(self, x):
        if utils.isValidSAI(self.ang_hor, self.ang_ver):
            #sai_it = 0
            l = []
            for y in range (self.ang_ver-1, self.ang_ver+2):
                for x in range (self.ang_hor-1, self.ang_hor+2):
                    img = QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(x))) + "_" + ("{0:0>3}".format(str(y))) + ".ppm")
                    l.append(qimage2ndarray.rgb_view(img.toImage()))
                    #sai_it = sai_it + 1
            # Chama Funcao Upscaling
            us.upsampling(l, 2)

    
    def mosca(self):
        m = mosca_window.MoscaWindow()
        m.loadMV(self.pathToPpms, 1.)


    def setScreenText (self):
        self.l_ang_hoz.setText("x: " + "{0:0>2}".format(str(self.ang_hor)))
        self.l_ang_ver.setText("y: " + "{0:0>2}".format(str(self.ang_ver)))


    def teste_janela(self):
        self.dialog.show()


if __name__ == '__main__':
    main()
#!/usr/local/bin/python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QBrush

import sys
import os
import qimage2ndarray
import numpy as np
import time

# My GUI frames
from frames.mainframe import Ui_MainWindow as Ui_MainWindow
from frames.viewframe1 import Ui_MainWindow as Ui_ViewWindow1
from frames.viewframe3 import Ui_MainWindow as Ui_ViewWindow3
# My Functions
import functions.utils as utils
import functions.img_manipulation as im
import functions.upsampling as us
import functions.mosca_window as mw
import functions.roi as roi



def main():
    app = QApplication(sys.argv)
    form = MainFrame()
    form.show()
    sys.exit(app.exec_())


class ViewFrame1(QtWidgets.QMainWindow, Ui_ViewWindow1):
    def __init__(self, parent=None):
        super(ViewFrame1, self).__init__(parent)
        self.setupUi(self)

    def show_image(self, img):
        self.label_tela.setPixmap(img.scaled(901,626,aspectRatioMode =1))
        self.update()


class ViewFrame3(QtWidgets.QMainWindow, Ui_ViewWindow3):
    def __init__(self, parent=None):
        super(ViewFrame3, self).__init__(parent)
        self.setupUi(self)
        self.img1 = []
        self.img2 = []
        self.img3 = []
        self.idx = 0
        self.pushButton_left.clicked.connect(self.buttonLeft)
        self.pushButton_right.clicked.connect(self.buttonRight)


    def initialize(self, img1, img_frames, img_diff):
        self.img1 = img1
        self.img2 = img_frames
        self.img3 = img_diff


    def show_image_roi(self, idx):
        self.label_tela_1.setPixmap(self.img1.scaled(441,321,aspectRatioMode =1))
        self.label_tela_2.setPixmap(self.img2[idx].scaled(441,321,aspectRatioMode =1))
        self.label_tela_3.setPixmap(self.img3[idx].scaled(441,321,aspectRatioMode =1))

    def buttonLeft(self):
        if self.idx > 0:
            self.idx -= 1
        else:
            self.idx = len(self.img2)-1
        self.show_image_roi(self.idx)

    def buttonRight(self):
        if self.idx < len(self.img2)-1:
            self.idx += 1
        else:
            self.idx = 0
        self.show_image_roi(self.idx)

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Left:
            self.buttonLeft()
        if event.key() == QtCore.Qt.Key_Right:
            self.buttonRight()
        self.update()



class MainFrame(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)
        self.setupUi(self)

        self.matrix_rgb = [[0 for x in range(15)]for y in range(15)]  # Matriz que guarda todos os ppms em rgb_view
        self.ang_hor = 0
        self.ang_ver = 0
        self.pathToPpms = "/home/paulo/Downloads/lf_datasets/Bikes"
        # Caminho so para testes, default=""
        self.pathToPpms = ""

        self.grid_x = 261
        self.grid_y = 62
        self.grid_w = 150
        self.grid_h = 150

        self.resetUi()

        if self.pathToPpms:
            self.ang_hor = 7
            self.ang_ver = 7
            self.openppms()


    

    def resetUi(self):
        self.setupUi(self)
        self.setScreenText()
        self.actionOpen.triggered.connect(self.openFile)
        # Sinais
        self.pushButton_reset.clicked.connect(self.buttonReset)
        self.pushButton_depthmap.clicked.connect(self.buttonDepthMap)
        self.pushButton_microimagens.clicked.connect(self.buttonFlyView)
        self.pushButton_upsampling.clicked.connect(self.buttonUpsampling)
        self.pushButton_roi.clicked.connect(self.buttonRoi)
        self.slider_brilho.valueChanged.connect(self.loadppm)
        self.slider_contraste.valueChanged.connect(self.loadppm)
        self.slider_saturacao.valueChanged.connect(self.loadppm)
        self.slider_nitidez.valueChanged.connect(self.loadppm)
        self.radioButton_red.clicked.connect(self.loadppm)
        self.radioButton_green.clicked.connect(self.loadppm)
        self.radioButton_blue.clicked.connect(self.loadppm)
        self.radioButton_maximizar.clicked.connect(self.loadppm)
        self.radioButton_original.clicked.connect(self.loadppm)


    def openFile(self):
        s = QFileDialog.getExistingDirectory(self, "Open a folder", "./")
        self.pathToPpms = str(s)
        self.ang_hor = 7
        self.ang_ver = 7
        self.setScreenText()
        self.openppms()
        self.resetUi()
        self.loadppm()
        self.update()


    # Carrega todos os ppms e indexa na matriz
    def openppms(self):
        for y in range(0,15):
            for x in range (0,15):
                self.matrix_rgb[x][y] = qimage2ndarray.rgb_view(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(x))) + "_" + ("{0:0>3}".format(str(y))) + ".ppm").toImage())
        self.loadppm()


    # Carrega o ppm e ajusta para o tamanho da label
    def loadppm(self):
        act_img, act_hist = self.apply_transformations()

        img_width  = act_img.width()
        img_height = act_img.height()
        if self.radioButton_maximizar.isChecked():
            img_width    = int(img_width  * (self.label_tela.width()  / img_width))                 # Scaling para o tamanho maximo 
            img_height   = int(img_height * (self.label_tela.height() / img_height))                # permitido dentro do label
        hist_width   = int(act_hist.width()  * (self.label_hist.width()  / act_hist.width()))       # Scaling para o tamanho maximo 
        hist_height  = int(act_hist.height() * (self.label_hist.height() / act_hist.height()))      # permitido dentro do label

        self.label_tela.setPixmap(act_img.scaled(img_width,img_height,aspectRatioMode =1))
        self.label_hist.setPixmap(act_hist.scaled(hist_width-10, hist_height-10))


    
    def apply_transformations(self):
        img = self.matrix_rgb[self.ang_hor][self.ang_ver]
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


    def apply_flyview(self):
        matrix_aux = [[0 for x in range(15)]for y in range(15)]
        for i in range(0, 15):
            for j in range (0, 15):
                img_aux = qimage2ndarray.array2qimage(self.matrix_rgb[i][j])
                img_aux = QtGui.QPixmap.fromImage(img_aux).scaled(123, 86, aspectRatioMode=1).toImage()
                matrix_aux[i][j] = qimage2ndarray.rgb_view(img_aux)

        img_mi = mw.mosca_window(matrix_aux, 0.5)
        img_mi = qimage2ndarray.array2qimage(img_mi)
        QtGui.QPixmap.fromImage(img_mi).save("visao_de_mosca.png", "PNG")
        print("TERMINOU")


    def apply_roi(self):
        img_diff, img_frames = roi.roi_espiral(self.matrix_rgb)
        img1 = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(self.matrix_rgb[self.ang_hor][self.ang_ver]))
        for i in range (len(img_diff)):
            img_diff[i] = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(img_diff[i]))
            img_frames[i] = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(img_frames[i]))

        viewframe = ViewFrame3(self)
        #c_time = time.clock()
        #idx = 0

        viewframe.initialize(img1, img_frames, img_diff)
        viewframe.show_image_roi(0)
        viewframe.show()

        # while True:
        #     if time.clock() - c_time > 1.:
        #         i = (i+1)%len(img_frames)
        #         c_time = time.clock()
                
        #     viewframe.show_image_roi(idx)
        #     viewframe.show()
        #     self.update()

        #     if time.clock() > 7.:
        #         break



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
    def buttonReset(self):
        self.resetUi()
        self.loadppm()


    def buttonDepthMap(self, flag):
        img2 = QtGui.QPixmap(self.pathToPpms + "/002_007.ppm")
        img1 = QtGui.QPixmap(self.pathToPpms + "/009_007.ppm")
        img3 = QtGui.QPixmap(self.pathToPpms + "/007_007.pgm")
        # img = qimage2ndarray.rgb_view(img3.toImage())
        img  = im.depthmap(qimage2ndarray.rgb_view(img1.toImage()), qimage2ndarray.rgb_view(img2.toImage()), qimage2ndarray.rgb_view(img3.toImage()), flag)
        self.to_viewframe(img)
        #QtGui.QPixmap.fromImage(img).save("depth.png", "PNG")


    def buttonUpsampling(self):
        if utils.isValidSAI(self.ang_hor, self.ang_ver):
            if self.radioButton_up2x.isChecked():
                img = us.upsampling(self.matrix_rgb, (self.ang_hor, self.ang_ver), 2)
                self.to_viewframe(img)
            if self.radioButton_up4x.isChecked():
                pass # NOT IMPLEMENTED

    
    def buttonFlyView(self):
        self.apply_flyview()


    def buttonRoi(self):
        self.apply_roi()


    def setScreenText (self):
        self.l_ang_hoz.setText("x: " + "{0:0>2}".format(str(self.ang_hor)))
        self.l_ang_ver.setText("y: " + "{0:0>2}".format(str(self.ang_ver)))


    def to_viewframe(self, img):
        viewframe = ViewFrame1(self)
        img = qimage2ndarray.array2qimage(img)
        img = QtGui.QPixmap.fromImage(img)
        viewframe.show_image(img)
        viewframe.show()


if __name__ == '__main__':
    main()
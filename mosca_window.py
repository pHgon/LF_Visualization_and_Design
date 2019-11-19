from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QBrush
import sys
import os
from moscaview import Ui_DmoscaView
import qimage2ndarray
import img_manipulation as im
import utils
import numpy as np

class MoscaWindow(QtWidgets.QDialog, Ui_DmoscaView):
    def __init__(self, parent=None):
        super(MoscaWindow, self).__init__(parent)
        self.setupUi(self)
        self.path = '/home/paulo/Downloads/Bikes/Bikes'
        self.loadMV()
    
    def loadMV(self):
        #np_mv = np.empty([271250])
        #print(len(np_mv))
        a = []
        # w = width -> largura
        # h = height -> altura
        #width = 625
        #height = 434
        width = 123
        height = 86
        for h in range(height):
            for w in range(width):
                a.append(np.empty([15,15,3]))    
            
        for i in range(15):
            for j in range(15):
                act_img = QtGui.QPixmap(self.path + "/" + ("{0:0>3}".format(i) + "_" + ("{0:0>3}".format(j)) + ".ppm")).scaled(123, 86, aspectRatioMode=1)
                img_a = qimage2ndarray.rgb_view(act_img.toImage())
                #print (img_a.shape)
                for h in range(height):
                    for w in range(width):
                        #a[h*3 + w][i][j] = img_a[h][w]
                        a[h*width + w][i][j] = img_a[h][w]
        # for h in range(height):
        #     for w in range(width):
        #         a.append(np.empty([15,15,3]))
            
        #         for i in range(15):
        #             for j in range(15):
        #                 act_img = QtGui.QPixmap(self.path + "/" + ("{0:0>3}".format(i) + "_" + ("{0:0>3}".format(j)) + ".ppm"))
        #                 img_a = qimage2ndarray.rgb_view(act_img.toImage())
        #                 a[h*3 + w][i][j] = img_a[h][w]
            
        # act_img = QtGui.QPixmap(self.path + "/" + ("{0:0>3}".format('7') + "_" + ("{0:0>3}".format('7')) + ".ppm"))
        # img = qimage2ndarray.rgb_view(act_img.toImage())
        # print(img[0][0])
        #np_mv = np.concatenate((np_mv0, np_mv1), axis=1)
        aux = 0
        for h in range(height):
            npa = a[h*width]
            for w in range(width):
                if w > 0:
                    npa = np.concatenate((npa, a[h*width + w]), axis=1)
            if aux == 0:
                img_mosca = npa 
                aux = 1
            else:    
                img_mosca = np.concatenate((img_mosca, npa))
        #
        # npa = a[0]
        # for i in range(1,3):
        #     npa = np.concatenate((npa,a[i]), axis=1)
        # for i in range(3,5):
        #     npa = np.concatenate((npa,a[i]))
        #npa.reshape((135,15,3))
        # print(len(npa))
        # print(len(npa[0]))
        # print(len(npa[0][0]))
        # print(npa.shape)
        #np.transpose(npa)
        img_m = qimage2ndarray.array2qimage(img_mosca)
        img_width  = int(act_img.width())
        img_height = int(act_img.height())
        #img_m.setRotation(10)
        QtGui.QPixmap.fromImage(img_m).save("teste.png", "PNG")
        #self.labelMosca.setPixmap(QtGui.QPixmap.fromImage(img_m).scaled(img_width, img_height, aspectRatioMode=1))
      


def main():
    app = QApplication(sys.argv)
    form = MoscaWindow()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
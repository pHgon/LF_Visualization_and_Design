# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QFileDialog
# from PyQt5.QtGui import QPainter, QColor, QBrush
# import sys
# import os
# from .frames.moscaview import Ui_DmoscaView
import qimage2ndarray
from . import img_manipulation as im
from . import utils
import numpy as np

# class MoscaWindow(QtWidgets.QDialog, Ui_DmoscaView):
#     def __init__(self, parent=None):
#         super(MoscaWindow, self).__init__(parent)
#         self.setupUi(self)
#         self.path = '/home/paulo/Downloads/Bikes/Bikes'
#         #self.loadMV('/home/vwdpinho/Documentos/Bikes/Bikes', 0.5)
    
#     def loadMV(self, path, scale):
#         #print('entrou')
#         #np_mv = np.empty([271250])
#         #print(len(np_mv))
#         a = []
#         # w = width -> largura
#         # h = height -> altura
#         width = 625
#         height = 434
#         if scale == 1:
#             width = 625
#             height = 434
#         if scale == 0.5:
#             width = 123
#             height = 86
#         for h in range(height):
#             for w in range(width):
#                 a.append(np.empty([15,15,3]))    
            
#         for i in range(15):
#             for j in range(15):
#                 act_img = QtGui.QPixmap(path + "/" + ("{0:0>3}".format(i) + "_" + ("{0:0>3}".format(j)) + ".ppm")).scaled(width, height, aspectRatioMode=1)
#                 img_a = qimage2ndarray.rgb_view(act_img.toImage())
#                 for h in range(height):
#                     for w in range(width):
                  
#                         a[h*width + w][i][j] = img_a[h][w]
       
#         aux = 0
#         for h in range(height):
#             npa = a[h*width]
#             for w in range(width):
#                 if w > 0:
#                     npa = np.concatenate((npa, a[h*width + w]), axis=1)
#             if aux == 0:
#                 img_mosca = npa 
#                 aux = 1
#             else:    
#                 img_mosca = np.concatenate((img_mosca, npa))
   
   
#         img_m = qimage2ndarray.array2qimage(img_mosca)
        
       
#         QtGui.QPixmap.fromImage(img_m).save("visao_de_mosca.png", "PNG")
#         #self.labelMosca.setPixmap(QtGui.QPixmap.fromImage(img_m).scaled(img_width, img_height, aspectRatioMode=1))
      


# def main():
#     app = QApplication(sys.argv)
#     form = MoscaWindow()
#     form.show()
#     app.exec_()


# if __name__ == '__main__':
#     main()



 
def loadMV(path, scale):
    a = []
    width = 625
    height = 434
    if scale == 1:
        width = 625
        height = 434
    if scale == 0.5:
        width = 123
        height = 86
    for h in range(height):
        for w in range(width):
            a.append(np.empty([15,15,3]))    
        
    for i in range(15):
        for j in range(15):
            act_img = QtGui.QPixmap(path + "/" + ("{0:0>3}".format(i) + "_" + ("{0:0>3}".format(j)) + ".ppm")).scaled(width, height, aspectRatioMode=1)
            img_a = qimage2ndarray.rgb_view(act_img.toImage())
            for h in range(height):
                for w in range(width):
              
                    a[h*width + w][i][j] = img_a[h][w]

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


    img_m = qimage2ndarray.array2qimage(img_mosca)
     
   
    QtGui.QPixmap.fromImage(img_m).save("visao_de_mosca.png", "PNG")
    #self.labelMosca.setPixmap(QtGui.QPixmap.fromImage(img_m).scaled(img_width, img_height, aspectRatioMode=1))

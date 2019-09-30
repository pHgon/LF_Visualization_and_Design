from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys
from lf import Ui_MainWindow 

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.angulo_horizontal = 7
        self.angulo_vertical = 7
        self.pathToPpms = ""
        self.setupUi(self)
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

    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Left:
            if(self.angulo_horizontal > 0):
                self.angulo_horizontal -= 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm"))

            

        if event.key() == QtCore.Qt.Key_Right:
            if(self.angulo_horizontal < 14):
                self.angulo_horizontal += 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm"))
           

        if event.key() == QtCore.Qt.Key_Up:
            if(self.angulo_vertical > 0):
                self.angulo_vertical -= 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm"))
            
            

        if event.key() == QtCore.Qt.Key_Down:
            if(self.angulo_vertical  < 14):
                self.angulo_vertical += 1
            self.label.setPixmap(QtGui.QPixmap(self.pathToPpms + "/" + ("{0:0>3}".format(str(self.angulo_horizontal))) + "_" + ("{0:0>3}".format(str(self.angulo_vertical))) + ".ppm"))
            
    

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
    #form.open_ppm()

if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'moscaview.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DmoscaView(object):
    def setupUi(self, DmoscaView):
        DmoscaView.setObjectName("DmoscaView")
        DmoscaView.resize(934, 650)
        self.labelMosca = QtWidgets.QLabel(DmoscaView)
        self.labelMosca.setGeometry(QtCore.QRect(10, 0, 901, 631))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.labelMosca.setPalette(palette)
        self.labelMosca.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.labelMosca.setMouseTracking(True)
        self.labelMosca.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.labelMosca.setAutoFillBackground(True)
        self.labelMosca.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelMosca.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelMosca.setLineWidth(5)
        self.labelMosca.setText("")
        self.labelMosca.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMosca.setIndent(0)
        self.labelMosca.setObjectName("labelMosca")

        self.retranslateUi(DmoscaView)
        QtCore.QMetaObject.connectSlotsByName(DmoscaView)

    def retranslateUi(self, DmoscaView):
        _translate = QtCore.QCoreApplication.translate
        DmoscaView.setWindowTitle(_translate("DmoscaView", "Dialog"))


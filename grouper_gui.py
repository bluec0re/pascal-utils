# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1927, 1121)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout.addWidget(self.lcdNumber)
        self.imageName = QtWidgets.QLabel(self.centralwidget)
        self.imageName.setObjectName("imageName")
        self.horizontalLayout.addWidget(self.imageName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.currentImage = QtWidgets.QLabel(self.centralwidget)
        self.currentImage.setScaledContents(True)
        self.currentImage.setObjectName("currentImage")
        self.verticalLayout.addWidget(self.currentImage)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        self.rightList = ImageList(self.centralwidget)
        self.rightList.setObjectName("rightList")
        self.gridLayout.addWidget(self.rightList, 1, 2, 1, 1)
        self.leftList = ImageList(self.centralwidget)
        self.leftList.setIconSize(QtCore.QSize(100, 100))
        self.leftList.setMovement(QtWidgets.QListView.Static)
        self.leftList.setViewMode(QtWidgets.QListView.IconMode)
        self.leftList.setObjectName("leftList")
        self.gridLayout.addWidget(self.leftList, 1, 0, 1, 1)
        self.topList = ImageList(self.centralwidget)
        self.topList.setIconSize(QtCore.QSize(100, 100))
        self.topList.setObjectName("topList")
        self.gridLayout.addWidget(self.topList, 0, 1, 1, 1)
        self.bottomList = ImageList(self.centralwidget)
        self.bottomList.setObjectName("bottomList")
        self.gridLayout.addWidget(self.bottomList, 3, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1927, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.imageName.setText(_translate("MainWindow", "TextLabel"))
        self.currentImage.setText(_translate("MainWindow", "IMAGE"))

from widgets import ImageList

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Life.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1920, 1050)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_field = QtWidgets.QHBoxLayout()
        self.horizontalLayout_field.setObjectName("horizontalLayout_field")
        spacerItem = QtWidgets.QSpacerItem(1800, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_field.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.horizontalLayout_field)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 800, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.formLayout_menu = QtWidgets.QFormLayout()
        self.formLayout_menu.setObjectName("formLayout_menu")
        self.label_Width = QtWidgets.QLabel(self.centralwidget)
        self.label_Width.setObjectName("label_Width")
        self.formLayout_menu.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Width)
        self.lineEdit_Width = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Width.setObjectName("lineEdit_Width")
        self.formLayout_menu.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Width)
        self.label_Height = QtWidgets.QLabel(self.centralwidget)
        self.label_Height.setObjectName("label_Height")
        self.formLayout_menu.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Height)
        self.lineEdit_Height = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Height.setObjectName("lineEdit_Height")
        self.formLayout_menu.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Height)
        self.pushButton_Accept = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Accept.setObjectName("pushButton_Accept")
        self.formLayout_menu.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pushButton_Accept)
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.formLayout_menu.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.pushButton_Start)
        self.pushButton_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.formLayout_menu.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.pushButton_Stop)
        self.lineEdit_Color = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Color.setObjectName("lineEdit_Color")
        self.formLayout_menu.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Color)
        self.label_Color = QtWidgets.QLabel(self.centralwidget)
        self.label_Color.setObjectName("label_Color")
        self.formLayout_menu.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_Color)
        self.pushButton_ChangeColor = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ChangeColor.setObjectName("pushButton_ChangeColor")
        self.formLayout_menu.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.pushButton_ChangeColor)
        self.verticalLayout.addLayout(self.formLayout_menu)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
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
        self.label_Width.setText(_translate("MainWindow", "            Width:"))
        self.label_Height.setText(_translate("MainWindow", "            Height:"))
        self.pushButton_Accept.setText(_translate("MainWindow", "Accept"))
        self.pushButton_Start.setText(_translate("MainWindow", "Start"))
        self.pushButton_Stop.setText(_translate("MainWindow", "Stop"))
        self.label_Color.setText(_translate("MainWindow", "            RGB:"))
        self.pushButton_ChangeColor.setText(_translate("MainWindow", "Change Color"))
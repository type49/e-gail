# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'queensettings.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

import configparser


config = configparser.ConfigParser()
config.read(r'data\settings.ini')
backgroundImage = config.get("Theme", "theme")


class Ui_SettingsWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(400, 200))
        MainWindow.setMaximumSize(QtCore.QSize(400, 200))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.themeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.themeComboBox.setGeometry(QtCore.QRect(200, 80, 191, 21))
        self.themeComboBox.setObjectName("comboBox")
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")
        self.themeComboBox.addItem("")

        self.centralwidget.setStyleSheet('''
                                    font: 8pt "Montserrat Alternates";
                                    background-color: #414547;
                                    color: #efe2cd;
                                    border: 1px solid #f39f18;
                                        ''')

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(220, 130, 75, 21))
        self.saveButton.setObjectName("saveButton")

        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(300, 130, 75, 21))
        self.cancelButton.setObjectName("cancelButton")


        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(300, 130, 75, 21))
        self.cancelButton.setObjectName("cancelButton")


        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        MainWindow.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool )

        self.themeComboBox.setItemText(0, _translate("MainWindow", "Голубая"))
        self.themeComboBox.setItemText(1, _translate("MainWindow", "Розовая"))

        self.saveButton.setText(_translate("MainWindow", "Применить"))
        self.cancelButton.setText(_translate("MainWindow", "Отменить"))

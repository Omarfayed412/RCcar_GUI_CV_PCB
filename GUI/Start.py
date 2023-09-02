# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Start.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_StartWindow(object):
    def setupUi(self, StartWindow):
        StartWindow.setObjectName("StartWindow")
        StartWindow.resize(1920, 1000)
        self.centralwidget = QtWidgets.QWidget(StartWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.manual_button = QtWidgets.QPushButton(self.centralwidget)
        self.manual_button.setGeometry(QtCore.QRect(400, 300, 300, 300))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.manual_button.setFont(font)
        self.manual_button.setObjectName("manual_button")
        self.auto_button = QtWidgets.QPushButton(self.centralwidget)
        self.auto_button.setGeometry(QtCore.QRect(1200, 300, 300, 300))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.auto_button.setFont(font)
        self.auto_button.setObjectName("auto_button")
        self.caption = QtWidgets.QLabel(self.centralwidget)
        self.caption.setGeometry(QtCore.QRect(800, 0, 280, 280))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.caption.setFont(font)
        self.caption.setAlignment(QtCore.Qt.AlignCenter)
        self.caption.setObjectName("caption")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(800, 700, 280, 280))
        self.logo.setText("")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.logopic = QPixmap('Aquaphoton.jpg')
        self.logo.setPixmap(self.logopic)
        StartWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(StartWindow)
        QtCore.QMetaObject.connectSlotsByName(StartWindow)

    def retranslateUi(self, StartWindow):
        _translate = QtCore.QCoreApplication.translate
        StartWindow.setWindowTitle(_translate("StartWindow", "MainWindow"))
        self.manual_button.setText(_translate("StartWindow", "Manual"))
        self.manual_button.setStyleSheet("QPushButton""{""background-color: #00ffff""}"
                                         "QPushButton::Pressed""{""background-color: green""}")
        self.auto_button.setText(_translate("StartWindow", "Autonomous"))
        self.auto_button.setStyleSheet("QPushButton""{""background-color: #00ffff""}"
                                       "QPushButton::Pressed""{""background-color: green""}")
        self.caption.setText(_translate("StartWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Training\'24</span></p><p><span style=\" font-weight:600;\">Team 1</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StartWindow = QtWidgets.QMainWindow()
    ui = Ui_StartWindow()
    ui.setupUi(StartWindow)
    StartWindow.show()
    sys.exit(app.exec_())

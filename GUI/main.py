from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtBluetooth
from Manual import Ui_ManualWindow
from Autonomous import Ui_AutoWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ManualWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Mode: Manual")


        self.window2 = QMainWindow()
        self.ui2 = Ui_AutoWindow()
        self.ui2.setupUi(self.window2)

        self.get_color_manual()
        self.get_icon_manual()
        self.ui.auto_button.clicked.connect(self.open_auto)
        self.uibuttons()


    def get_color_manual(self):
        self.setStyleSheet("background-color: white")

        self.ui.screenshot_button.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")
        self.ui.forward_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")
        self.ui.backward_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")
        self.ui.right_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")
        self.ui.left_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")
        self.ui.stitch_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")
        self.ui.stereo_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")
        self.ui.auto_button.setStyleSheet("background-color: #00ffff; border-radius: 30; border: 3px solid")

        self.ui.camera.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui.motion.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui.speed.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui.voltage.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui.current.setStyleSheet("background-color: white; border: 3px solid black")

    def get_color_auto(self):
        self.window2.setStyleSheet("background-color: white")

        self.ui2.screenshot_button.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")
        self.ui2.set_distance.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")
        self.ui2.set_speed.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")
        self.ui2.stitch_button.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")
        self.ui2.stereo_button.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")
        self.ui2.manual_button.setStyleSheet("background-color: #00ffff; border-radius: 40; border: 3px solid")

        self.ui2.view_distance.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.view_speed.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.ultrasonic.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.camera.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.motion.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.speed.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.voltage.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.current.setStyleSheet("background-color: white; border: 3px solid")

    def get_icon_manual(self):
        self.ui.forward_button.setIcon(QIcon('Forward.png'))
        self.ui.backward_button.setIcon(QIcon('Backward.png'))
        self.ui.right_button.setIcon(QIcon('Right.png'))
        self.ui.left_button.setIcon(QIcon('Left.png'))

        self.logopic = QPixmap('Aquaphoton.jpg')
        self.ui.logo.setPixmap(self.logopic)
        self.compasspic = QPixmap('Compass.jpg')
        self.ui.motion_pic.setPixmap(self.compasspic)
        self.speedpic = QPixmap('Speed.jpg')
        self.ui.speed_pic.setPixmap(self.speedpic)
        self.voltpic = QPixmap('Voltage.jpg')
        self.ui.volt_pic.setPixmap(self.voltpic)
        self.currentpic = QPixmap('Current.jpg')
        self.ui.current_pic.setPixmap(self.currentpic)

    def get_icon_auto(self):
        self.logopic = QPixmap('Aquaphoton.jpg')
        self.ui2.logo.setPixmap(self.logopic)
        self.compasspic = QPixmap('Compass.jpg')
        self.ui2.motion_pic.setPixmap(self.compasspic)
        self.speedpic = QPixmap('Speed.jpg')
        self.ui2.speed_pic.setPixmap(self.speedpic)
        self.voltpic = QPixmap('Voltage.jpg')
        self.ui2.volt_pic.setPixmap(self.voltpic)
        self.currentpic = QPixmap('Current.jpg')
        self.ui2.current_pic.setPixmap(self.currentpic)

    def open_manual(self):
        self.window2.close()
        self.showMaximized()
        self.ui.auto_button.clicked.connect(self.open_auto)



    def open_auto(self):
        self.close()
        self.window2.setWindowTitle("Mode: Autonomous")
        self.get_color_auto()
        self.get_icon_auto()
        self.ui2.manual_button.clicked.connect(self.open_manual)
        self.window2.showMaximized()

    def uibuttons(self):
        self.distance = 0
        self.speed = 0
        self.ui2.set_distance.clicked.connect(self.get_distance)
        self.ui2.set_speed.clicked.connect(self.get_speed)

    def get_distance(self):
        distance, done_dist = QInputDialog.getInt(self, "Distance To Wall", "Set Distance:")
        if done_dist:
            self.distance = distance
            self.ui2.view_distance.setText(str(distance))

    def get_speed(self):
        speed, done_speed = QInputDialog.getInt(self, "Speed Of Car", "Set Speed:")
        if done_speed:
            self.speed = speed
            self.ui2.view_speed.setText(str(speed))



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

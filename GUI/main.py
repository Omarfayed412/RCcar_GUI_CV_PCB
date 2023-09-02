from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QDialog
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5 import QtBluetooth, QtGui
from Start import Ui_StartWindow
from Manual import Ui_ManualWindow
from Autonomous import Ui_AutoWindow
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StartWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Start Window")

        self.window1 = QMainWindow()
        self.ui1 = Ui_ManualWindow()
        self.ui1.setupUi(self.window1)

        self.window2 = QMainWindow()
        self.ui2 = Ui_AutoWindow()
        self.ui2.setupUi(self.window2)

        self.ui.manual_button.clicked.connect(self.open_manual)
        self.ui.auto_button.clicked.connect(self.open_auto)
        self.ui.manual_button.setStyleSheet("QPushButton""{""background-color: #00ffff""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui.auto_button.setStyleSheet("QPushButton""{""background-color: #00ffff""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.logopic = QPixmap('Aquaphoton.jpg')
        self.ui.logo.setPixmap(self.logopic)

        self.uibuttons()

        self.mutex = QMutex()
        self.thread = WebcamThread()
        self.thread.frame_data.connect(self.update_feed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.thread.start()
        self.timer.start(30)
        #QtBluetooth.QBluetoothDeviceDiscoveryAgent.deviceDiscovered.connect()
        #QtBluetooth.QBluetoothDeviceDiscoveryAgent.deviceDiscovered.connect()

    def update_feed(self, image_Q):
        self.mutex.lock()
        pixmap = QPixmap.fromImage(image_Q)
        self.ui1.camera.setPixmap(pixmap)
        self.ui2.camera.setPixmap(pixmap)
        self.mutex.unlock()

    def update_frame(self):
        self.mutex.lock()
        #pixmap = self.ui1.camera.pixmap()
        #pixmap = self.ui2.camera.pixmap()
        self.mutex.unlock()

    def get_color_manual(self):
        self.window1.setStyleSheet("background-color: white")

        self.ui1.screenshot_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.forward_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.backward_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.right_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.left_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.stitch_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.stereo_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.auto_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.Drive.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 50; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.Park.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 50; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.RF.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.LF.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.RB.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui1.LB.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 30; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")

        self.ui1.camera.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui1.motion.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui1.speed.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui1.voltage.setStyleSheet("background-color: white; border: 3px solid black")
        self.ui1.current.setStyleSheet("background-color: white; border: 3px solid black")

    def get_color_auto(self):
        self.window2.setStyleSheet("background-color: white")

        self.ui2.screenshot_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.set_distance.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.set_speed.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.stitch_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.stereo_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.manual_button.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 40; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.Drive.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 50; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")
        self.ui2.Park.setStyleSheet("QPushButton""{""background-color: #00ffff; border-radius: 50; border: 3px solid""}"
                                     "QPushButton::Pressed""{""background-color: green""}")

        self.ui2.view_distance.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.view_speed.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.ultrasonic.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.camera.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.motion.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.speed.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.voltage.setStyleSheet("background-color: white; border: 3px solid")
        self.ui2.current.setStyleSheet("background-color: white; border: 3px solid")

    def get_icon_manual(self):
        self.ui1.forward_button.setIcon(QIcon('Forward.png'))
        self.ui1.backward_button.setIcon(QIcon('Backward.png'))
        self.ui1.right_button.setIcon(QIcon('Right.png'))
        self.ui1.left_button.setIcon(QIcon('Left.png'))

        self.logopic = QPixmap('Aquaphoton.jpg')
        self.ui1.logo.setPixmap(self.logopic)
        self.compasspic = QPixmap('Compass.jpg')
        self.ui1.motion_pic.setPixmap(self.compasspic)
        self.speedpic = QPixmap('Speed.jpg')
        self.ui1.speed_pic.setPixmap(self.speedpic)
        self.voltpic = QPixmap('Voltage.jpg')
        self.ui1.volt_pic.setPixmap(self.voltpic)
        self.currentpic = QPixmap('Current.jpg')
        self.ui1.current_pic.setPixmap(self.currentpic)

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
        self.close()
        self.window2.close()
        self.window1.setWindowTitle("Mode: Manual")
        self.get_color_manual()
        self.get_icon_manual()
        self.ui1.auto_button.clicked.connect(self.open_auto)
        #self.ui1.stitch_button.clicked.connect(self.get_stitch)
        self.window1.showMaximized()

    def open_auto(self):
        self.close()
        self.window1.close()
        self.window2.setWindowTitle("Mode: Autonomous")
        self.get_color_auto()
        self.get_icon_auto()
        self.ui2.manual_button.clicked.connect(self.open_manual)
        #self.ui2.stitch_button.clicked.connect(self.get_stitch)
        self.window2.showMaximized()

    #def get_stitch(self):
        #self.player = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        #self.ui1.stitch_button.clicked.connect(self.open_stitch)
        #self.ui2.stitch_button.clicked.connect(self.open_stitch)
        #self.player.setMedia('Right(Better Quality.mp4')
        #self.player.play()

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


class WebcamThread(QThread):
    frame_data = pyqtSignal(QImage)
    def run(self):
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            if not ret:
                break
            frame = cv2.resize(frame,(1920,500))
            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            height, width, channels = image.shape
            bytes_per_line = channels * width
            image_Q = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.frame_data.emit(image_Q)
        capture.release()



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

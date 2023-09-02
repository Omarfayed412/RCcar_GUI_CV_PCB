from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5 import QtBluetooth
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

    def update_feed(self, image_q):
        self.mutex.lock()
        pixmap = QPixmap.fromImage(image_q)
        self.ui1.camera.setPixmap(pixmap)
        self.ui2.camera.setPixmap(pixmap)
        self.mutex.unlock()

    def update_frame(self):
        self.mutex.lock()
        #pixmap = self.ui1.camera.pixmap()
        #pixmap = self.ui2.camera.pixmap()
        self.mutex.unlock()

    def open_manual(self):
        self.close()
        self.window2.close()
        self.window1.setWindowTitle("Mode: Manual")
        self.ui1.auto_button.clicked.connect(self.open_auto)
        #self.ui1.stitch_button.clicked.connect(self.get_stitch)
        self.window1.showMaximized()

    def open_auto(self):
        self.close()
        self.window1.close()
        self.window2.setWindowTitle("Mode: Autonomous")
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
            frame = cv2.resize(frame, (1920, 500))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = image.shape
            bytes_per_line = channels * width
            image_q = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.frame_data.emit(image_q)
        capture.release()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

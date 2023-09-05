"""
Importing necessary libraries and modules
"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex
from Start import Ui_StartWindow
from Manual import Ui_ManualWindow
from Autonomous import Ui_AutoWindow
from Bluetooth import Ui_Dialog
import cv2
import bluetooth


class MainWindow(QMainWindow):
    """
    This method initialize and set up our GUI windows by generating the Qt designs after generating
    a python class from the UI file
    """
    def __init__(self):
        super().__init__()
        # Loading the generated python class from the Start Window UI file
        self.ui_start = Ui_StartWindow()
        self.ui_start.setupUi(self)
        self.setWindowTitle("Start Window")

        # Loading the generated python class from the Manual Window UI file
        self.window_manual = QMainWindow()
        self.ui_manual = Ui_ManualWindow()
        self.ui_manual.setupUi(self.window_manual)

        # Loading the generated python class from the Autonomous Window UI file
        self.window_auto = QMainWindow()
        self.ui_auto = Ui_AutoWindow()
        self.ui_auto.setupUi(self.window_auto)

        # Loading the generated python class from the Bluetooth Sub Window UI file
        self.window_blue = QDialog()
        self.ui_blue = Ui_Dialog()
        self.ui_blue.setupUi(self.window_blue)
        self.window_blue.setWindowTitle("Bluetooth List")

        """
        Bluetooth Implementation
        """
        # Scanning for nearby Devices
        self.nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices = ''
        for address, name in self.nearby_devices:
            devices = devices + f"Address: {address}, Name: {name}\n"
        # Placing addresses and names inside label
        self.ui_blue.Bluetooth_list.setText(devices)
        # Calling Method for user to choose which bluetooth device to connect to
        self.ui_blue.Device_chosen.setMaximum(len(self.nearby_devices))
        self.ui_start.Bluetooth.clicked.connect(self.get_bluetooth)

        # Switching from Start Window to Manual or Autonomous Window according to push button clicked
        self.ui_start.manual_button.clicked.connect(self.open_manual)
        self.ui_start.auto_button.clicked.connect(self.open_auto)

        # Calling method that gives action to push buttons
        self.uibuttons()
        """
        Live Webcam Feed 
        PS. ( it might glitch )
        """
        """
        # QMutex is to protect an object of code so that only one thread can access it at a time
        self.mutex = QMutex()
        # Calling class that generates frames of the Webcam
        self.thread = WebcamThread()
        # Updating the feed
        self.thread.frame_data.connect(self.update_feed)
        # Providing repetitive and single-shot timers
        self.timer = QTimer()
        # Updating the frame
        self.timer.timeout.connect(self.update_frame)
        # Emiting the timeout signal at constant intervals
        self.thread.start()
        self.timer.start(30)

    # Updating the Webcam feed in Manual and Autonomous Windows
    def update_feed(self, image_q):
        self.mutex.lock()
        pixmap = QPixmap.fromImage(image_q)
        self.ui_manual.camera.setPixmap(pixmap)
        self.ui_auto.camera.setPixmap(pixmap)
        if self.ui_manual.screenshot_button.clicked() or self.ui_auto.screenshot_button.clicked():
            image_q.save("Screenshot.jpg")
        self.mutex.unlock()

    def update_frame(self):
        self.mutex.lock()
        self.ui_manual.camera.pixmap()
        self.ui_auto.camera.pixmap()
        self.mutex.unlock()

    
    # RFCOMM ( Radio Frequency Communication ) is a protocol that emulates a serial port connection
    # over the bluetooth wireless technology.
    # It enables the exchange of data between bluetooth devices as if they were connected through 
    # a physical serial cable. 
    
    """
    # Opening Manual Window
    def open_manual(self):
        # Closing all unused Windows
        self.close()
        self.window_auto.close()
        self.window_manual.setWindowTitle("Mode: Manual")
        # Switching between Manual Window and Autonomous Window
        self.ui_manual.auto_button.clicked.connect(self.open_auto)
        self.window_manual.showMaximized()

    # Opening Autonomous Window
    def open_auto(self):
        # Closing all unused Windows
        self.close()
        self.window_manual.close()
        self.window_auto.setWindowTitle("Mode: Autonomous")
        # Switching between Autonomous Window and Manual Window
        self.ui_auto.manual_button.clicked.connect(self.open_manual)
        self.window_auto.showMaximized()

    """
    Rest of Bluetooth implementation
    """
    def get_bluetooth(self):
        self.window_blue.show()
        self.ui_blue.buttonBox.clicked.connect(self.get_device_chosen)

    # Connecting to device chosen by user
    def get_device_chosen(self):
        num = self.ui_blue.Device_chosen.value()
        address, name = self.nearby_devices[num-1]

        self.server_socket = bluetooth.BluetoothSocket()
        self.server_socket.connect((address, 5))
        self.server_socket.listen(1)
        # Starting Communication
        self.client_socket, self.client_address = self.server_socket.accept()
        self.data_receive()
        self.data_send()

    # Communication laws with firmware
    # Received Data
    def data_receive(self):
        data = self.client_socket.recv(1024)
        if data:
            received_data = data.decode("utf-8")
            if received_data == "F":
                self.ui_manual.motion.setText("Forward")
                self.ui_auto.motion.setText("Forward")
            elif received_data == "B":
                self.ui_manual.motion.setText("Backward")
                self.ui_auto.motion.setText("Backward")
            elif received_data == "R":
                self.ui_manual.motion.setText("Right")
                self.ui_auto.motion.setText("Right")
            elif received_data == "L":
                self.ui_manual.motion.setText("Left")
                self.ui_auto.motion.setText("Left")
            # Speed sensor feedback ( Communication Law: S then value, ex: S20)
            elif received_data[0] == 'S':
                s = slice(1, len(received_data))
                # Applying reading to labels
                self.ui_manual.speed.setText(received_data[s] + ' m/s')
                self.ui_auto.speed.setText(received_data[s] + ' m/s')
            # Voltage sensor feedback ( Communication Law: V then value, ex: V3.3)
            elif received_data[0] == 'V':
                s = slice(1, len(received_data))
                # Applying reading to labels
                self.ui_manual.voltage.setText(received_data[s] + ' V')
                self.ui_auto.voltage.setText(received_data[s] + ' V')
            # Current sensor feedback ( Communication Law: C then value, ex: C4)
            elif received_data[0] == 'C':
                s = slice(1, len(received_data))
                # Applying reading to labels
                self.ui_manual.current.setText(received_data[s] + ' A')
                self.ui_auto.current.setText(received_data[s] + ' A')
            # Ultrasonic sensor feedback ( Communication Law: U then value, ex: U15)
            elif received_data[0] == 'U':
                s = slice(1, len(received_data))
                # Applying reading to labels
                self.ui_auto.ultrasonic.setText(received_data[s] + ' cm')

    # Sent Data
    def data_send(self):
        # Sending distance to wall in Autonomous Mode
        distance = self.ui_auto.set_distance.clicked.connect(self.get_distance)
        distance = 'D' + distance
        self.client_socket.send(distance.encode("utf-8"))
        # Sending speed chosen in Autonomous Mode
        speed = self.ui_auto.set_speed.clicked.connect(self.get_speed)
        speed = 'S' + speed
        self.client_socket.send(speed.encode("utf-8"))
        # Drive Mode
        if self.ui_manual.Drive.clicked():
            status = 'D'
            self.client_socket.send(status.encode("utf-8"))
        # Park Mode
        if self.ui_manual.Park.clicked():
            status = 'S'
            self.client_socket.send(status.encode("utf-8"))
        # Forward Motion
        if self.ui_manual.forward_button.clicked():
            status = 'F'
            self.client_socket.send(status.encode("utf-8"))
        # Backward Motion
        elif self.ui_manual.backward_button.clicked():
            status = 'B'
            self.client_socket.send(status.encode("utf-8"))
        # Right Motion
        elif self.ui_manual.right_button.clicked():
            status = 'R'
            self.client_socket.send(status.encode("utf-8"))
        # Left Motion
        elif self.ui_manual.left_button.clicked():
            status = 'L'
            self.client_socket.send(status.encode("utf-8"))

    # Giving Action to buttons
    def uibuttons(self):
        # Initializing Attributes
        self.distance_to_wall = 0
        self.speed_choose = 0
        # Setting distance to wall or speed choose according to push button clicked
        self.ui_auto.set_distance.clicked.connect(self.get_distance)
        self.ui_auto.set_speed.clicked.connect(self.get_speed)

    def get_distance(self):
        # Prompt user to enter distance to wall
        distance, done_distance = QInputDialog.getInt(self, "Distance To Wall", "Set Distance:")
        if done_distance:
            self.distance_to_wall = distance
            # Applying reading to label
            self.ui_auto.view_distance.setText(str(distance) + " cm")

        # Return distance to wall to be sent to ESP32 using Bluetooth
        return str(distance)

    def get_speed(self):
        # Prompt user to enter speed choose
        speed, done_speed = QInputDialog.getInt(self, "Speed Of Car", "Set Speed:")
        if done_speed:
            self.speed_choose = speed
            # Applying reading to labels
            self.ui_auto.view_speed.setText(str(speed) + " m/s")
        # Return speed choose to be sent to ESP32 using Bluetooth
        return str(speed)


"""
Rest of Live Web Cam feed implementation
"""


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

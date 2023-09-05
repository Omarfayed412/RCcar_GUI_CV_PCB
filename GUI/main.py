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

        self.window_blue = QDialog()
        self.ui_blue = Ui_Dialog()
        self.ui_blue.setupUi(self.window_blue)
        self.window_blue.setWindowTitle("Bluetooth List")

        self.nearby_devices = bluetooth.discover_devices(lookup_names=True)
        devices = ''
        for address, name in self.nearby_devices:
            devices = devices + f"Address: {address}, Name: {name}\n"
        self.ui_blue.Bluetooth_list.setText(devices)
        self.ui_blue.Device_chosen.setMaximum(len(self.nearby_devices))
        self.is_bluetooth = True

        # Switching from Start Window to Manual or Autonomous Window according to push button clicked
        self.ui_start.manual_button.clicked.connect(self.open_manual)
        self.ui_start.auto_button.clicked.connect(self.open_auto)

        # Calling method that gives action to push buttons
        self.uibuttons()

        self.mutex = QMutex()
        self.thread = WebcamThread()
        self.thread.frame_data.connect(self.update_feed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.thread.start()
        self.timer.start(30)

    def update_feed(self, image_q):
        self.mutex.lock()
        pixmap = QPixmap.fromImage(image_q)
        self.ui_manual.camera.setPixmap(pixmap)
        self.ui_auto.camera.setPixmap(pixmap)
        self.mutex.unlock()

    def update_frame(self):
        self.mutex.lock()
        self.ui_manual.camera.pixmap()
        self.ui_auto.camera.pixmap()
        self.mutex.unlock()


    """
    RFCOMM ( Radio Frequency Communication ) is a protocol that emulates a serial port connection
    over the bluetooth wireless technology.
    It enables the exchange of data between bluetooth devices as if they were connected through 
    a physical serial cable. 
    """

    """
    def microcontroller_connected(self):

        
        self.device_connectivity = QBluetoothDeviceInfo()
        rssi = self.device_connectivity.rssi()
        
        distance = self.ui_auto.set_distance.clicked.connect(self.get_distance)
        distance = 'D' + distance
        self.socket.write(distance.encode())
        speed = self.ui_auto.set_speed.clicked.connect(self.get_speed)
        speed = 'S' + speed
        self.socket.write(speed.encode())
        
        Drive
        
        if self.ui_manual.Park.clicked():
            status = 'S'
            self.socket.write(status.encode())
        if self.ui_manual.forward_button.clicked():
            status = 'F'
            self.socket.write(status.encode())
        elif self.ui_manual.backward_button.clicked():
            status = 'B'
            self.socket.write(status.encode())
        elif self.ui_manual.right_button.clicked():
            status = 'R'
            self.socket.write(status.encode())
        elif self.ui_manual.left_button.clicked():
            status = 'L'
            self.socket.write(status.encode())

    def data_received(self):
        data = self.socket.readAll().data().decode()
        if data == "F":
            self.ui_manual.motion.setText("Forward")
            self.ui_auto.motion.setText("Forward")
        elif data == "B":
            self.ui_manual.motion.setText("Backward")
            self.ui_auto.motion.setText("Backward")
        elif data == "R":
            self.ui_manual.motion.setText("Right")
            self.ui_auto.motion.setText("Right")
        elif data == "L":
            self.ui_manual.motion.setText("Left")
            self.ui_auto.motion.setText("Left")
        elif data[0] == 'S':
            s = slice(1, len(data))
            self.ui_manual.speed.setText(data[s] + ' m/s')
            self.ui_auto.speed.setText(data[s] + ' m/s')
        elif data[0] == 'V':
            s = slice(1, len(data))
            self.ui_manual.voltage.setText(data[s] + ' V')
            self.ui_auto.voltage.setText(data[s] + ' V')
        elif data[0] == 'C':
            s = slice(1, len(data))
            self.ui_manual.current.setText(data[s] + ' A')
            self.ui_auto.current.setText(data[s] + ' A')
        elif data[0] == 'U':
            s = slice(1, len(data))
            self.ui_auto.ultrasonic.setText(data[s] + ' cm')
    """

    # Opening Manual Window
    def open_manual(self):
        if self.is_bluetooth == True:
            self.get_bluetooth()
        # Closing all unused Windows
        self.close()
        self.window_auto.close()
        self.window_manual.setWindowTitle("Mode: Manual")
        # Switching between Manual Window and Autonomous Window
        self.ui_manual.auto_button.clicked.connect(self.open_auto)
        self.window_manual.showMaximized()

    # Opening Autonomous Window
    def open_auto(self):
        if self.is_bluetooth == True:
            self.get_bluetooth()
        # Closing all unused Windows
        self.close()
        self.window_manual.close()
        self.window_auto.setWindowTitle("Mode: Autonomous")
        # Switching between Autonomous Window and Manual Window
        self.ui_auto.manual_button.clicked.connect(self.open_manual)
        self.window_auto.showMaximized()

    def get_bluetooth(self):
        self.window_blue.show()
        self.ui_blue.buttonBox.clicked.connect(self.get_device_chosen)
        self.is_bluetooth = False

    def get_device_chosen(self):
        num = self.ui_blue.Device_chosen.value()
        address, name = self.nearby_devices[num-1]

        self.server_socket = bluetooth.BluetoothSocket()
        self.server_socket.connect((address, 5))
        self.server_socket.listen(1)
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Accepted connection from {self.client_address}")
        self.data_receive()
        self.data_send()

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
            elif received_data[0] == 'S':
                s = slice(1, len(received_data))
                self.ui_manual.speed.setText(received_data[s] + ' m/s')
                self.ui_auto.speed.setText(received_data[s] + ' m/s')
            elif received_data[0] == 'V':
                s = slice(1, len(received_data))
                self.ui_manual.voltage.setText(received_data[s] + ' V')
                self.ui_auto.voltage.setText(received_data[s] + ' V')
            elif received_data[0] == 'C':
                s = slice(1, len(received_data))
                self.ui_manual.current.setText(received_data[s] + ' A')
                self.ui_auto.current.setText(received_data[s] + ' A')
            elif received_data[0] == 'U':
                s = slice(1, len(received_data))
                self.ui_auto.ultrasonic.setText(received_data[s] + ' cm')

    def data_send(self):
        distance = self.ui_auto.set_distance.clicked.connect(self.get_distance)
        distance = 'D' + distance
        self.client_socket.send(distance.encode("utf-8"))
        speed = self.ui_auto.set_speed.clicked.connect(self.get_speed)
        speed = 'S' + speed
        self.client_socket.send(speed.encode("utf-8"))
        if self.ui_manual.Drive.clicked():
            status = 'D'
            self.client_socket.send(status.encode("utf-8"))
        if self.ui_manual.Park.clicked():
            status = 'S'
            self.client_socket.send(status.encode("utf-8"))
        if self.ui_manual.forward_button.clicked():
            status = 'F'
            self.client_socket.send(status.encode("utf-8"))
        elif self.ui_manual.backward_button.clicked():
            status = 'B'
            self.client_socket.send(status.encode("utf-8"))
        elif self.ui_manual.right_button.clicked():
            status = 'R'
            self.client_socket.send(status.encode("utf-8"))
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
            self.ui_auto.view_distance.setText(str(distance) + " cm")

        # Return distance to wall to be sent to ESP32 using Bluetooth
        return str(distance)

    def get_speed(self):
        # Prompt user to enter speed choose
        speed, done_speed = QInputDialog.getInt(self, "Speed Of Car", "Set Speed:")
        if done_speed:
            self.speed_choose = speed
            self.ui_auto.view_speed.setText(str(speed) + " m/s")
        # Return speed choose to be sent to ESP32 using Bluetooth
        return str(speed)


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
        if self.ui_manual.screenshot_button.clicked() or self.ui_auto.screenshot_button.clicked():
            image_q.save("Screenshot.jpg")
        capture.release()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

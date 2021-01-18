from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
try:
    from bme280_rpi.bme280_rpi import Sensor
except:
    pass
import sys


Ui_MainWindow, QtBaseClass = uic.loadUiType("test.ui")

def read_sensor():
    try:
        sensor = Sensor()
        data = sensor.get_data()
        return data
    except:
        print('Exception connecting to BME')
        error = '00.00'
        reply = {'timestamp': error, 'temperature': error, 'pressure': error, 'humidity': error}
        print(reply)
        return reply

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.tempSensor = '00.00'
        self.humSensor = '00.00'
        self.tempOutside = '00.00'
        self.humOutside = '00.00'
        self.ui.tempSensor.display(self.tempSensor)
        self.ui.humSensor.display(self.humSensor)
        self.ui.tempOutside.display(self.tempOutside)
        self.ui.humOutside.display(self.humOutside)

        def timeout1():
            try:
                self.MyThread1.start()
                self.MyTimer1.start(10)
            except Exception as e:
                self.tempSensor = '00.00'
                self.humSensor = '00.00'
                print(e)
                self.ui.tempSensor.display(self.tempSensor)
                self.ui.humSensor.display(self.humSensor)

        def timeout2():
            try:
                self.MyThread2.start()
                self.MyTimer2.start(10)
            except Exception as e:
                self.tempOutside = '00.00'
                self.humOutside = '00.00'
                print(e)
                self.ui.tempOutside.display(self.tempOutside)
                self.ui.humOutside.display(self.humOutside)

        def done1(temp, humi):
            self.tempSensor = temp
            self.humSensor = humi
            print(f"t {temp} H {humi} self: {self.tempSensor} {self.humSensor}")
            self.ui.tempSensor.display(self.tempSensor)
            self.ui.humSensor.display(self.humSensor)

        def done2(press):
            self.press = press
            self.ui.tempOutside.display(self.tempOutside)
            self.ui.humOutside.display(self.humOutside)

        self.MyThread1 = sensorThread()
        # self.MyThread1.connect(done1)
        self.MyThread1.MySignal1.connect(done1)
        self.MyThread2 = outsideThread()
        self.MyThread2.MySignal2.connect(done2)

        self.MyTimer1 = QTimer()
        self.MyTimer1.timeout.connect(timeout1)
        self.MyTimer1.start(10)
        self.MyTimer2 = QTimer()
        self.MyTimer2.timeout.connect(timeout2)
        self.MyTimer2.start(10)

    def __del__(self):
        self.MyTimer1.stop()
        self.MyTimer2.stop()
        self.MyThread1.terminate()
        self.MyThread2.terminate()


class sensorThread(QThread):
    MySignal1 = pyqtSignal(str, str)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            print('here')
            data = read_sensor()
            print(data)
            try:
                temp = str(round(data['temperature'], 2))
                humi = str(round(data['humidity'], 2))
            except Exception as e:
                print(e)
                temp = '00.00'
                humi = '00.00'
            print(temp)
            print(humi)
            self.MySignal1.emit(temp, humi)
            QThread.sleep(5)


class outsideThread(QThread):
    MySignal2 = pyqtSignal(str, str)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        temp = '00.00'
        humi = '00.00'
        self.MySignal2.emit(temp, humi)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

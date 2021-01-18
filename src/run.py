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
        error = 'Cannot connect to module'
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
                self.MyTimer1.start(90000)
            except:
                self.tempSensor = '00.00'
                self.humSensor = '00.00'
                self.ui.tempSensor.display(self.tempSensor)
                self.ui.humSensor.display(self.humSensor)

        def timeout2():
            try:
                self.MyThread2.start()
                self.MyTimer2.start(600000)
            except:
                self.tempOutside = '00.00'
                self.humOutside = '00.00'
                self.ui.tempOutside.display(self.tempOutside)
                self.ui.humOutside.display(self.humOutside)

        def done1(temp, humi):
            self.temp = temp
            self.humi = humi
            self.ui.tempSensor.display(self.tempSensor)
            self.ui.humSensor.display(self.humSensor)

        def done2(press):
            self.press = press
            self.ui.tempOutside.display(self.tempOutside)
            self.ui.humOutside.display(self.humOutside)

        self.MyThread1 = sensorThread()
        self.MyThread1.MySignal1.connect(done1)
        self.MyThread2 = outsideThread()
        self.MyThread2.MySignal2.connect(done2)

        self.MyTimer1 = QTimer()
        self.MyTimer1.timeout.connect(timeout1)
        self.MyTimer1.start(100)
        self.MyTimer2 = QTimer()
        self.MyTimer2.timeout.connect(timeout2)
        self.MyTimer2.start(100)

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
        temp = '00.00'
        humi = '00.00'
        while True:
            print('here')
            data = read_sensor()
            print(data)
            ctemp = data
            print(ctemp)
            print('last')
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
        # try:
        #     process = os.popen('rtl_433 -f 868250000 -g 42 -p 37 -q -R 8 -T 65')
        #     str = process.read()
        #     process.close()
        #
        #     if str:
        #         str = str.strip()
        #         str = str.replace('\t', '')
        #         str = str.replace('\n', ' ')
        #         data = str.split(' ')
        #
        #         if data[6] == 'Temperature:' and data[15] == 'Humidity:':
        #             temp = data[7]
        #             humi = data[16]
        #         elif data[6] == 'Humidity:' and data[15] == 'Temperature:':
        #             temp = data[16]
        #             humi = data[7]
        #     elif not str:
        #         temp = '--.-'
        #         humi = '--.-'
        # except:
        #     temp = '--.-'
        #     humi = '--.-'
        self.MySignal2.emit(temp, humi)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

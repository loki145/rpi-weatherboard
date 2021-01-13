import sys
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QLabel
# from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets, QtGui, QtCore
try:
    from bme280_rpi.bme280_rpi import Sensor
except:
    pass
#
#
def read_data():
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



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Tom")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Date = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Date.setFont(font)
        self.Date.setAlignment(QtCore.Qt.AlignCenter)
        self.Date.setObjectName("Date")
        self.verticalLayout.addWidget(self.Date)
        self.Time = QtWidgets.QLabel(self.centralwidget)

        self.verticalLayout.addWidget(self.Time)
        self.Weather = QtWidgets.QLabel(self.centralwidget)
        self.Weather.setAlignment(QtCore.Qt.AlignCenter)
        self.Weather.setWordWrap(False)
        self.Weather.setObjectName("Weather")
        self.verticalLayout.addWidget(self.Weather)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(771, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Tom", "Tom"))
        self.Date.setText(_translate("Tom", "Today is "))
        self.Time.setText(_translate("Tom", "It is currently "))
        self.Weather.setText(_translate("Tom", "New York City" ))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        timerTime = QtCore.QTimer(self)
        timerTime.timeout.connect(self.updateDate)
        timerTime.start(1000)
        #Here
        self.bme = GetBMEThread(self)
        self.bme.tempSignal.connect(self.updateTemp)
        self.bme.start()
        # self.pyowm = PyownThread(self)
        # self.pyowm.tempSignal.connect(self.updateTemp)
        # self.pyowm.start()

    def updateDate(self):
        date = QtCore.QDateTime.currentDateTime()
        self.Date.setText("Today is " + date.toString("ddd MMMM d yyyy"))
        self.Time.setText("It is currently " + date.toString("hh:mm:ss ap"))

    def updateTemp(self, temp):
        print(temp)
        self.Weather.setText("temperature:" + str(temp['temperature']) + " \u00B0C")


class GetBMEThread(QtCore.QThread):
    tempSignal = QtCore.pyqtSignal(dict)
    def __init__(self, parent=None):
        self._mutex = QtCore.QMutex()
        super(GetBMEThread, self).__init__(parent=parent)
#         self.owm = pyowm.OWM('1589dbcc0e9608e5b70f0ede23e757c8')
#
    def run(self):
        while True:
            self._mutex.lock()
            print('here')
            data = read_data()
            print(data)
            ctemp = data
            print(ctemp)
            self.tempSignal.emit(ctemp)
            self._mutex.unlock()
            QtCore.QThread.sleep(5 * 60)
            print('last')

#             observation = self.owm.weather_at_place('New York,us')
#             w = observation.get_weather()
#             ctemp = w.get_temperature('celsius')
#             self.tempSignal.emit(ctemp)
#             QtCore.QThread.sleep(5*60)

# class PyownThread(QtCore.QThread):
#     tempSignal = QtCore.pyqtSignal(dict)
#     def __init__(self, parent=None):
#         super(PyownThread, self).__init__(parent=parent)
#         self.owm = pyowm.OWM('1589dbcc0e9608e5b70f0ede23e757c8')
#
#     def run(self):
#         while True:
#             observation = self.owm.weather_at_place('New York,us')
#             w = observation.get_weather()
#             ctemp = w.get_temperature('celsius')
#             self.tempSignal.emit(ctemp)
#             QtCore.QThread.sleep(5*60)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
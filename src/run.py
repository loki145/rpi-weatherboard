#!/usr/bin/env python3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
try:
    from bme280_rpi.bme280_rpi import Sensor
except:
    pass
import sys, requests, json, os


Ui_MainWindow, QtBaseClass = uic.loadUiType("test.ui")
API_KEY = os.environ.get('OW_KEY')
AIR_KEY = os.environ.get('AQICN_KEY')
#General URL
openWeatherURL = f'http://api.openweathermap.org/data/2.5/weather?q=Krakow&appid={API_KEY}&units=metric'
#All in one URL
openWeatherURL = f'https://api.openweathermap.org/data/2.5/onecall?lat=50.0833&lon=19.9167&exclude=minutely,hourly&appid={API_KEY}&units=metric'
#Air pollution API
openWeatherPollutionURL = f'http://api.openweathermap.org/data/2.5/air_pollution?lat=50.0833&lon=19.9167&appid={AIR_KEY}'

aqicnAPIPollutionURL = f"https://api.waqi.info/feed/krakow/?token={AIR_KEY}"

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
        self.wind_speed = '00.00'
        self.air_value = '0'
        self.air_icon = 'icons/air.png'
        self.icon = 'icons/unknown.png'
        self.windIcon = 'icons/wind.png'
        self.pixmap = QPixmap(self.icon)
        self.F_D1 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
        self.F_D2 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
        self.F_D3 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
        self.pixmapD1 = QPixmap(self.F_D1["icon"])
        self.pixmapD2 = QPixmap(self.F_D2["icon"])
        self.pixmapD3 = QPixmap(self.F_D3["icon"])
        self.pixmapWind = QPixmap(self.windIcon)
        self.pixmapAIR = QPixmap(self.air_icon)
        self.ui.tempSensor.display(self.tempSensor)
        self.ui.humSensor.display(self.humSensor)
        self.ui.tempOutside.display(self.tempOutside)
        self.ui.humOutside.display(self.humOutside)
        self.ui.WeatherImage.setPixmap(self.pixmap)
        self.ui.WindIcon.setPixmap(self.pixmapWind)
        self.ui.WindSpeed.setText(self.wind_speed)
        self.ui.F_D1_I.setPixmap(self.pixmapD1)
        self.ui.F_D2_I.setPixmap(self.pixmapD2)
        self.ui.F_D3_I.setPixmap(self.pixmapD3)
        self.ui.F_D1_T.setText(f"{self.F_D1['t_day']}\{self.F_D1['t_night']}")
        self.ui.F_D2_T.setText(f"{self.F_D2['t_day']}\{self.F_D2['t_night']}")
        self.ui.F_D3_T.setText(f"{self.F_D3['t_day']}\{self.F_D3['t_night']}")
        self.ui.air_icon.setPixmap(self.pixmapAIR)
        self.ui.air_value.setText(self.air_value)



        def timeout1():
            try:
                self.MyThread1.start()
                self.MyTimer1.start(10)
            except Exception as e:
                self.tempSensor = '00.00'
                self.humSensor = '00.00'
                self.icon = 'icons/unknown.png'
                self.wind_speed = '00.00'
                self.F_D1 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
                self.F_D2 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
                self.F_D3 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
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
                self.icon = 'icons/unknown.png'
                self.wind_speed = '00.00'
                self.F_D1 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
                self.F_D2 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
                self.F_D3 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
                print(e)
                self.ui.tempOutside.display(self.tempOutside)
                self.ui.humOutside.display(self.humOutside)
                self.ui.WeatherImage.setPixmap(self.pixmap)

        def timeout3():
            try:
                self.MyThread3.start()
                self.MyTimer3.start(10)
            except Exception as e:
                self.air_value = '0'
                self.air_icon = 'icons/air.png'
                print(e)
                self.pixmapAIR = QPixmap(self.air_icon)
                self.ui.air_icon.setPixmap(self.pixmapAIR)
                self.ui.air_value.setText(self.air_value)

        def done1(temp, humi):
            self.tempSensor = temp
            self.humSensor = humi
            print(f"t {temp} H {humi} self: {self.tempSensor} {self.humSensor}")
            self.ui.tempSensor.display(self.tempSensor)
            self.ui.humSensor.display(self.humSensor)

        def done2(temp, humi, icon, wind_speed, F_D1, F_D2, F_D3):
            self.tempOutside = temp
            self.humOutside = humi
            self.icon = icon
            self.pixmap = QPixmap(self.icon)
            self.wind_speed = wind_speed
            self.F_D1 = F_D1
            self.F_D2 = F_D2
            self.F_D3 = F_D3
            self.ui.tempOutside.display(self.tempOutside)
            self.ui.humOutside.display(self.humOutside)
            self.ui.WeatherImage.setPixmap(self.pixmap)
            self.ui.WindSpeed.setText(self.wind_speed)
            self.pixmapD1 = QPixmap(self.F_D1["icon"])
            self.pixmapD2 = QPixmap(self.F_D2["icon"])
            self.pixmapD3 = QPixmap(self.F_D3["icon"])
            self.ui.F_D1_I.setPixmap(self.pixmapD1)
            self.ui.F_D2_I.setPixmap(self.pixmapD2)
            self.ui.F_D3_I.setPixmap(self.pixmapD3)
            self.ui.F_D1_T.setText(f"{self.F_D1['t_day']}\n{self.F_D1['t_night']}")
            self.ui.F_D2_T.setText(f"{self.F_D2['t_day']}\n{self.F_D2['t_night']}")
            self.ui.F_D3_T.setText(f"{self.F_D3['t_day']}\n{self.F_D3['t_night']}")
            print(self.F_D1)
            print(self.F_D2)
            print(self.F_D3)

        def done3(air_value):
            print("in done3")
            self.air_value = air_value
            self.air_icon = 'icons/air.png'
            print(f"got air quality {self.air_value} and {self.air_icon}")
            self.pixmapAIR = QPixmap(self.air_icon)
            self.ui.air_icon.setPixmap(self.pixmapAIR)
            self.ui.air_value.setText(self.air_value)
            color = ''
            if 0 <= int(self.air_value) <= 50:
                color = 'lightgreen'
            elif 51 <= int(self.air_value) <= 100:
                color = 'yellow'
            elif 101 <= int(self.air_value) <= 150:
                color = 'orange'
            elif 151 <= int(self.air_value) <= 200:
                color = 'red'
            elif 201 <= int(self.air_value) <= 300:
                color = 'purple'
            else:
                color = 'black'
            self.ui.air_icon.setStyleSheet(f"background-color: {color}")

        self.MyThread1 = sensorThread()
        self.MyThread1.MySignal1.connect(done1)
        self.MyThread2 = outsideThread()
        self.MyThread2.MySignal2.connect(done2)
        self.MyThread3 = airQThread()
        self.MyThread3.MySignal3.connect(done3)

        self.MyTimer1 = QTimer()
        self.MyTimer1.timeout.connect(timeout1)
        self.MyTimer1.start(10)
        self.MyTimer2 = QTimer()
        self.MyTimer2.timeout.connect(timeout2)
        self.MyTimer2.start(10)
        self.MyTimer3 = QTimer()
        self.MyTimer3.timeout.connect(timeout3)
        self.MyTimer3.start(10)

    def __del__(self):
        self.MyTimer1.stop()
        self.MyTimer2.stop()
        self.MyTimer3.stop()
        self.MyThread1.terminate()
        self.MyThread2.terminate()
        self.MyThread3.terminate()


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
    MySignal2 = pyqtSignal(str, str, str, str, dict, dict, dict)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        temp = '00.00'
        humi = '00.00'
        icon = 'icons/unknown.png'
        wind_speed = '0.0'
        wind_deg = 0
        F_D1 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
        F_D2 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
        F_D3 = {"t_day": "00.00", "t_night": "00.00", "icon": "icons/unknown.png"}
        while True:
            weather = requests.get(openWeatherURL)
            j_weather = weather.json()
            print(weather.status_code)
            print(openWeatherURL)
            print(weather.text)
            if (weather.status_code == 200) and ('current' in j_weather):
                print('code is fine')
                try:
                    temp = str(j_weather['current']['temp'])
                    humi = str(j_weather['current']['humidity'])
                    wind_speed = str(j_weather['current']['wind_speed'])
                    wind_deg = str(j_weather['current']['wind_speed'])
                    icon = 'icons/' + str(j_weather['current']['weather'][0]['icon']) + '.png'
                    if ('daily' in j_weather) and (len(j_weather['daily']) >= 3):
                        print(f'found dayily forecast {j_weather["daily"]}')
                        t1_day = "{:.0f}".format(j_weather["daily"][0]["temp"]["day"])
                        t1_night = "{:.0f}".format(j_weather["daily"][0]["temp"]["night"])
                        t2_day = "{:.0f}".format(j_weather["daily"][1]["temp"]["day"])
                        t2_night = "{:.0f}".format(j_weather["daily"][1]["temp"]["night"])
                        t3_day = "{:.0f}".format(j_weather["daily"][2]["temp"]["day"])
                        t3_night = "{:.0f}".format(j_weather["daily"][3]["temp"]["night"])
                        F_D1 = {"t_day": t1_day, "t_night": t1_night, "icon": f'icons/' + j_weather["daily"][0]["weather"][0]["icon"] + '.png'}
                        F_D2 = {"t_day": t2_day, "t_night": t2_night, "icon": f'icons/' + j_weather["daily"][1]["weather"][0]["icon"] + '.png'}
                        F_D3 = {"t_day": t3_day, "t_night": t3_night, "icon": f'icons/' + j_weather["daily"][2]["weather"][0]["icon"] + '.png'}
                except Exception as e:
                    print(f"OopenWeather error is {e}")
                print(f"Outside emit is {temp} and {humi} and icon {icon} and wind {wind_speed} towards {wind_deg}")
                self.MySignal2.emit(temp, humi, icon, wind_speed, F_D1, F_D2, F_D3)
            else:
                print('soemthing bad happened')
            QThread.sleep(600)


class airQThread(QThread):
    MySignal3 = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        print("Starting thread 3")
        air_value = '0'
        while True:
            print("while loop")
            try:
                air_response = requests.get(aqicnAPIPollutionURL)
                print(aqicnAPIPollutionURL)
                print(AIR_KEY)
            except Exception as e:
                print(f"Exception happened in Thread 3 {e}")
                self.MySignal3.emit(air_value)
                QThread.sleep(600)
            if (air_response.status_code == 200) and ('data' in air_response.json()) and (air_response.json()['status'] == 'ok'):
                j_body = air_response.json()
                print(f"Got 200 from Air with {j_body}")
                air_value = j_body['data']['aqi']
                print(f"Your city smells like {air_value}")
            else:
                print(f"Something bad happened {air_response.text} with code {air_response.status_code}")
                air_value = '0'
            print("Emitting it")
            self.MySignal3.emit(str(air_value))
            QThread.sleep(600)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MyApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)

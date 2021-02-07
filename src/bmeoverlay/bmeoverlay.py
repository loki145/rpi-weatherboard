class Sensor:
    def __init__(self):
        self.main_path = "/sys/bus/iio/devices/iio:device0/"
        self.temp_file = self.main_path + "in_humidityrelative_input"
        self.hum_file = self.main_path + "in_temp_input"
        self.temp_val = "00.00"
        self.hum_val = "00.00"

    def temp(self):
        with open(self.temp_file, 'r') as temp_file:
            value = float(temp_file.read())
            self.temp_val = value / 1000.0
            return self.temp_val

    def hum(self):
        with open(self.hum_file, 'r') as hum_file:
            value = float(hum_file.read())
            self.hum_val = value / 1000.0
            return self.hum_val

    def get_data(self):
        self.temp()
        self.hum()
        return {'timestamp': '', 'temperature': self.temp_val, 'pressure': '', 'humidity': self.hum_val}

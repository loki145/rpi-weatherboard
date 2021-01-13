import smbus2
import bme280


class Sensor:
    def __init__(self):
        self.port = 1
        self.address = 0x77
        self.bus = smbus2.SMBus(self.port)
        # TODO: should i call it time to time as well?
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

    def get_data(self):
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        return {'timestamp': data.timestamp, 'temperature': data.temperature, 'pressure': data.pressure, 'humidity': data.humidity}


# port = 1
# address = 0x77
# bus = smbus2.SMBus(port)
#
# calibration_params = bme280_rpi.load_calibration_params(bus, address)
#
# # the sample method will take a single reading and return a
# # compensated_reading object
# data = bme280_rpi.sample(bus, address, calibration_params)
#
# # the compensated_reading class has the following attributes
# print(data.id)
# print(data.timestamp)
# print(data.temperature)
# print(data.pressure)
# print(data.humidity)
#
# # there is a handy string representation too
# print(data)
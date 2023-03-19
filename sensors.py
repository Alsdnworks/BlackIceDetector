# ESP32 Micropython code to read sensor data
# In actual use, put the file of sensorModules in the same location
from machine import Pin, SoftI2C, UART
from micropyGPS import MicropyGPS
from bmp180 import BMP180
import mlx90614
import dht
import math


class SensorBase:
    def __init__(self) -> None:
        self.uart = UART(
            1,
            rx=12,
            tx=13,
            baudrate=9600,
            bits=8,
            parity=None,
            stop=1,
            timeout=5000,
            rxbuf=1024,
        )
        self.gps = MicropyGPS()
        self.bus = SoftI2C(scl=Pin(27), sda=Pin(14))
        self._bmp180 = BMP180(self.bus)
        self._bmp180.baseline = 1008.1 * 100
        self._bmp180.oversample_sett = 2
        self.i2c = SoftI2C(scl=Pin(25), sda=Pin(26), freq=100000)
        self._mlx90614 = mlx90614.mlx90614(self.i2c)
        self._dht = dht.DHT22(Pin(33))
        self.alpha = 17.27
        self.beta = 237.7

    def run(self):
        try:
            buf = self.uart.readline()
            TMP = self._bmp180.temperature / self._dht.temperature()
            PRES = self._bmp180.pressure
            GTMP = self._mlx90614.read_object_temp()
            REHU = self._dht.humidity()
            for char in buf:
                self.gps.update(chr(char))
            # print('UTC Timestamp:', gps.timestamp)
            # print('Date:', gps.date_string('long'))
            # print('Satellites:', self.gps.satellites_in_use)
            # print('Altitude:', gps.altitude)
            # print('Latitude:', self.gps.latitude)
            # print('Longitude:', self.gps.longitude_string())
            # print('Horizontal Dilution of Precision:', gps.hdop)
            # print('temperature:', temp)
            # print('pressure:', p)
            # print('ground_temp:', ground_temp)
            # print('hum:', hum)
            # print('DHTair_temp:', air_temp)
            # print('')
            res = None
            gamma = ((self.alpha * TMP) / (self.beta + TMP)) + math.log(REHU / 100.0)
            es = 6.112 * math.exp(gamma) * (PRES / 1013.25) ** (1.0 - 0.00075 * TMP)
            gamma_dp = math.log(es / 6.112)
            dew_point = (self.beta * gamma_dp) / (self.alpha - gamma_dp)
            res = True if ((dew_point > GTMP) and (GTMP < 4)) else False
            return (
                TMP,
                PRES,
                GTMP,
                REHU,
                self.gps.latitude,
                self.gps.longitude_string(),
                res,
            )

        except:
            return (None, None, None, None, None, None, None)


if __name__ == "__main__":
    s = SensorBase()
    uart = UART(1, baudrate=9600, tx=Pin(17), rx=Pin(16))
    while True:
        uart.write(str(s.run()))

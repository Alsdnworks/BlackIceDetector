# Raspberry Pi
# Code to read sensor data from ESP32 and save it to Postgresql
import serial
import psycopg2
import time


class SensorDataStreamer:
    def __init__(
        self,
        port="/dev/ttyACM0",
        baudrate=9600,
        host="000.000.000.000",
        dbname="test",
        user="postgres",
        password="0000",
        port_number=0000,
    ):
        self.ser = serial.Serial(port, baudrate)
        self.connection = psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password, port=port_number
        )
        self.cur = self.connection.cursor()

    def commit_stream_data(self):
        while True:
            try:
                now = time.time()
                data = self.ser.readline().decode().strip()
                if None not in data:
                    TMP, PRES, GTMP, REHU, lat, lon, res = data.split(",")
                    self.cur.execute(
                        "INSERT INTO sensor_data (timestamp, temperature, pressure, ground_temp, humidity, latitude, longitude, blackIce) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (now, TMP, PRES, GTMP, REHU, lat, lon, res),
                    )
                    self.connection.commit()
                    print("Success")
            except:
                print("READ Error")
                continue


if __name__ == "main":
    s = SensorDataStreamer()
    s.commit_stream_data()
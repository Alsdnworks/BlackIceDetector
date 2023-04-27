#include <SoftwareSerial.h>
#include <Adafruit_MLX90614.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Wire.h>

SoftwareSerial gpsSerial(2, 3); // RX, TX
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

typedef struct latlon {
    float lat;
    float lon;
} latlon;

const char* target = "$GPGGA";

latlon getLatLon() {
    char buffer[100];
    char raw;
    latlon result = { 0.0, 0.0 };
    int i = 0;

    while (gpsSerial.available()) {
        raw = gpsSerial.read();
        if (raw == '\n') {
            buffer[i] = '\0';
            if (strstr(buffer, target) != NULL) {
                char* p = strtok(buffer, ",");
                for (int i = 0; i < 8; i++) {
                    p = strtok(NULL, ",");
                    if (i == 1) {
                        result.lat = atof(p);
                    }
                    if (i == 3) {
                        result.lon = atof(p);
                    }
                }
                return result;
            }
            i = 0;
        }
        else {
            buffer[i] = raw;
            i++;
        }
    }
    return result;
}

void setup() {
    Serial.begin(9600);
    gpsSerial.begin(9600);
    mlx.begin();
}

void loop() {
    latlon ll = getLatLon();
    if (ll.lat != 0.0 && ll.lon != 0.0) {
        Serial.print("Lat: ");
        Serial.print(ll.lat, 6);
        Serial.print(" Lon: ");
        Serial.println(ll.lon, 6);
        Serial.print("Temp: ");
        Serial.println(mlx.readObjectTempC());
    }
}
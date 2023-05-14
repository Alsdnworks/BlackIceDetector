#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <math.h>

#define SLAVE_ADDRESS 0x08
#define PIEZO 12
#define DHTPIN1 10      // Pin where the DHT22 sensor is connected
#define DHTPIN2 6      // Pin where the DHT22 sensor is connected
#define DHTTYPE DHT22 // Define the type of sensor

int ledPin[] = { 2, 3, 4 }; //2 red, 3 green, 4 blue
Adafruit_MLX90614 mlx;
Adafruit_BMP085 bmp;
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

float interp(float *arr);
void runAlarm();
int blackIceDetection(float surfaceTemperature, float humidity, float temperature);

void setup(){
  Serial.begin(9600); // start serial for output
  Wire.begin(); // join i2c bus (address optional for master)
  bmp.begin(); // Start the BMP085 sensor
  mlx.begin(); // Start the MLX90614 sensor
  dht1.begin(); // Start the DHT sensor
  dht2.begin(); // Start the DHT sensor
  for (int i = 0; i < sizeof(ledPin) / sizeof(ledPin[0]); i++) { //init led
    pinMode(ledPin[i], OUTPUT);
  }
  pinMode(PIEZO, OUTPUT); //init piezo
}

float interp(float *arr) {
  int count = 0;
  float sum = 0;
  for (int i = 0; i < count; i++) {
    if (arr[i] != -999) {
      sum += arr[i];
      count++;
    }
  }
  if (count == 0) {
    return -999;
  }
  float avg = sum / count;
  for (int i = 0; i < count; i++) {
    if (abs(arr[i] - avg) > 5) {
      arr[i] = -999;
      interp(arr);
    }
  }
  return avg;
}

void runAlarm() {
  for (int hz = 300; hz <= 750; hz++) {
    tone(PIEZO, hz);
    delay(5);
  }
  for (int hz = 750; hz >= 300; hz--) {
    tone(PIEZO, hz);
    delay(5);
  }
}

int blackIceDetection(float surfaceTemperature, float humidity, float temperature) {
  //calculate dew point
  float a = 17.27;
  float b = 237.7;
  float alpha = ((a * temperature) / (b + temperature)) + log(humidity / 100.0);
  float dewPoint = (b * alpha) / (a - alpha);

  //high rate black ice probability -> run alarm with red led
  if (surfaceTemperature < 0 && humidity > 70 && surfaceTemperature - dewPoint < 3) {
    runAlarm();
    digitalWrite(ledPin[0], HIGH);
    return 3;
  }

  //low rate black ice probability -> run alarm with yellow led
  if (surfaceTemperature < 1) {
    runAlarm();
    digitalWrite(ledPin[1], HIGH);
    digitalWrite(ledPin[0], HIGH);
    return 2;
  }

  //no black  ice probability -> green led
  digitalWrite(ledPin[1], HIGH);
  return 1;
}

void loop(){
  //check serial status
  while (true) {
    //init rgb led
    for (int i = 0; i < 3; i++) {digitalWrite(ledPin[i], LOW);}
    //read and check sensor error - Temperature
    float temp1 = mlx.readAmbientTempC();
    float temp2 = bmp.readTemperature();
    float temp3 = dht1.readTemperature();
    float temp4 = dht2.readTemperature();
    float temp[] = {temp1, temp2, temp3, temp4};
    float temperature = interp(temp);
    if temperature == -999 {runAlarm();digitalWrite(ledPin[2], HIGH);continue;}
  
    //read and check sensor error - Humidity
    float hum1 = dht1.readHumidity();
    float hum2 = dht2.readHumidity();
    float hum[] = {hum1, hum2};
    float humidity = interp(hum);
    if humidity == -999 {runAlarm();digitalWrite(ledPin[2], HIGH);continue;}
  
    //read and check sensor error - Object Temperature
    float tempObj = mlx.readObjectTempC();
    if (tempObj < -100 || tempObj > 200) {runAlarm();digitalWrite(ledPin[2], HIGH);continue;}
  
    //black ice detection
    int blackIce = blackIceDetection(tempObj, humidity, temperature);
  
    //send data to master
    Wire.beginTransmission(SLAVE_ADDRESS);
    Wire.write(blackIce);
    Wire.write((byte*)&tempObj, sizeof(float));
    Wire.write((byte*)&humidity, sizeof(float));
    Wire.write((byte*)&temperature, sizeof(float));
    Wire.endTransmission();
  }
}

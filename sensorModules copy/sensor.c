#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <Adafruit_BMP085.h>
#include <DHT.h>
#include <math.h>
#include <Wire.h>
#define NUM_SENSORS 3
#define THRESHOLD 1
#define alpha 17.27
#define beta 237.7
#define DHTPIN1 10      // Pin where the DHT22 sensor is connected
#define DHTPIN2 6      // Pin where the DHT22 sensor is connected
#define DHTTYPE DHT22 // Define the type of sensor
//센서를 제어하고
int ledPin[] = { 2,3,4 }; //2 red, 3 green, 4 blue
char color[] = { 'r', 'g', 'b' };
int wait = 3000; //대기시간 변수처리
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
Adafruit_BMP085 bmp;
DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);
void requestEvent(bool isBI);
void setup()
{
    Serial.begin(9600);
    Wire.begin(0x08);
    Wire.onRequest(requestEvent);
    bmp.begin();
    mlx.begin();
    dht1.begin(); // Start the DHT sensor
    dht2.begin(); // Start the DHT sensor
    for (int i = 0; i < sizeof(ledPin) / sizeof(int); i++) { //int 형 4
    pinMode(ledPin[i], OUTPUT);
    }
}

void requestEvent(bool isBI) {
   if (isBI) {
      Wire.write(1);
   } else {
      Wire.write(0);
   }
}

void runAlram()
{
    for (int hz = 300; hz <= 750; hz++)
    {
        tone(10, hz);

        delay(5);
    }

    for (int hz = 750; hz >= 300; hz--)
    {
        tone(10, hz);

        delay(5);
    }
}

//TODO: detectBI 함수는 LED제어로 상황 표시
bool detectBI(float dp, float st, float at)
{
    if (at < dp || st < 2 && at < 4)
    {
        // runAlram();
        return true;
    }
    else
    {
        return false;
    }
}


//TODO: LED 제어는 R파워(init시 3초간) G() B() 3초간, 이후  LOOP에서는 detectBI 를 통해 bool값을 받아와서 제어
//현재의 경우는 LED는 장식용으로 사용되면 1초에 한번씩 내용을 변경하도록 설계하도록 한다
void statLed()
{
    for (int i = 0; i < sizeof(ledPin) / sizeof(int); i++) {//int 형 4

        Serial.print(color[i]);

        Serial.print(" on");

        for (int j = 0; j < sizeof(ledPin) / sizeof(int); j++) {//int 형 4

            digitalWrite(ledPin[j], LOW); //전체 LED

        }

        digitalWrite(ledPin[i], HIGH); //LED on

        delay(wait); //지연시간 추가

    }
}
void loop()
{
    float temp1 = mlx.readAmbientTempC();
    float temp2 = bmp.readTemperature();
    float temp3 = dht1.readTemperature(); // Read the temperature data from the sensor
    float temp4 = dht2.readTemperature(); // Read the temperature data from the sensor
    
    float hum1 = dht1.readHumidity();       // Read the humidity data from the sensor
    float hum2 = dht2.readHumidity();       // Read the humidity data from the sensor
    
    float tempObj = mlx.readObjectTempC();
    float atm_pressure = bmp.readPressure() / 100;// notuse

    float air_temperature = (temp1 + temp2 + temp3 + temp4) / 4;
    float humidity = (hum1 + hum2) / 2;
    
    bool isBI = false;
    float gamma = ((alpha * air_temperature) / (beta + air_temperature)) + log(humidity / 100.0);
    float es = 6.112 * exp(gamma) * pow((atm_pressure / 1013.25), (1.0 - 0.00075 * air_temperature));
    float gamma_dp = log(es / 6.112);
    float dew_point = (beta * gamma_dp) / (alpha - gamma_dp);

    Serial.print("Temperature:");
    Serial.println(air_temperature);
    Serial.print("humidity:");
    Serial.println(humidity);
    //Serial.print("atm_pressure:");
    //Serial.println(atm_pressure);
    Serial.print("serface Temperature:");
    Serial.println(tempObj);
    Serial.print("Dew Point Temperature:");
    Serial.println(dew_point);
    Serial.println();
    isBI = detectBI(dew_point, tempObj, air_temperature);
    
    statLed();
    
    requestEvent(isBI);
    digitalWrite(10, HIGH); // 4. HIGH: 전압이 5V(아두이노 보드 전압)로 설정됩니다.
    delay(1000);            // 5. 1000ms동안 대기합니다. 1000ms=1초
    digitalWrite(10, LOW);  // 6. LOW: 전압이 0V로 설정됩니다.
    delay(1000);
}
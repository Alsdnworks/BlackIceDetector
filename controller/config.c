#include <DHT.h>
#include <LiquidCrystal_I2C.h>

DHT dht[] = { DHT(4, DHT22), DHT(5, DHT22) };
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();
  lcd.backlight();
  for (auto& sensor : dht) {
    sensor.begin();
  }
}

void loop() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("HUM:CHKDHTCONN");
  //lcd.print("A_TMP: "); lcd.print(dht[0].readTemperature()); lcd.print("C");
  //lcd.print("A_HUM: "); lcd.print(dht[0].readHumidity()); lcd.print("%");
  lcd.setCursor(0,1);
  lcd.print("TMP:CHKDHTCONN");
  //lcd.print("G_TMP2: "); lcd.print(dht[1].readTemperature()); lcd.print("C");
  //lcd.print("G_HUM: "); lcd.print(dht[1].readHumidity()); lcd.print("%");
  delay(1000);
}
#include <DHT.h>

#define DHTPIN 21
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();   // Celsius
  float hum  = dht.readHumidity();

  // Check if reading failed
  if (isnan(temp) || isnan(hum)) {
    return; // skip this cycle
  }

  // Send in clean CSV format: temp,humidity
  Serial.print(temp, 2);   // 2 decimal places
  Serial.print(",");
  Serial.println(hum, 2);

  delay(2000);  // DHT11 needs ~2 seconds
}
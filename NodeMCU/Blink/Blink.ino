#include <Arduino.h>
#define LED 2

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(115200);
  pinMode(LED , OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED, LOW);  // turn the LED on D4/GPIO2. led is active at LOW
  Serial.println("LED is on");
  delay(1000); 
  digitalWrite(LED, HIGH);
  Serial.println("LED is off");
  delay(1000);
}

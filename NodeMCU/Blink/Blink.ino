#define led_built_in_ESP 2
#define led_built_in_Node 16

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(115200);
  pinMode(led_built_in_ESP, OUTPUT);
  pinMode(led_built_in_Node, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(led_built_in_ESP, HIGH); 
  digitalWrite(led_built_in_Node, LOW); // turn the LED on D4/GPIO2. led is active at LOW
  Serial.println("LED is on");
  delay(1000); 
  digitalWrite(led_built_in_ESP, LOW); 
  digitalWrite(led_built_in_Node, HIGH); 
  Serial.println("LED is off");
  delay(1000); 
}
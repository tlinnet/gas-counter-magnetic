# Gas counter with NodeMCU

In this example, we will use [NodeMCU Lua Lolin V3](https://www.az-delivery.de/products/nodemcu-lolin-v3-modul-mit-esp8266). ESP-12E processor with ESP8266 WLAN module, with [Lolin, manual available here](https://www.az-delivery.de/products/nodemcu-lolin-v3-kostenfreies-e-book) and [NodeMCU LUA Amica V2, manual available here](https://www.az-delivery.de/products/nodemcu-amica-v2-kostenfreies-e-book), where both should be read. 

I had problems getting the driver to work via CH340 USB interface, so instead used a PL-2303 TA USB to TTL. Connecting GND(Black) -> GND, 5V(Red) -> Vin, Tx(Green) -> Rx, Rx(White) -> Tx, and installed driver from [PL23XX_Prolific_DriverInstaller_v4300.zip](https://www.prolific.com.tw/US/ShowProduct.aspx?p_id=225&pcid=41).

Install [Arduino IDE](https://www.arduino.cc/en/Main/Software), and open Arduino IDE. Install board.
* `File > Preferences`. Additional URLs field= `https://arduino.esp8266.com/stable/package_esp8266com_index.json`
* `Tools > Board > Boards Manager`. Search `esp8266`. Install "esp8266 by ESP8266 Community".

`Lolin` has this diagram.

![](https://user-images.githubusercontent.com/16295580/37866513-dbaca3a2-2f8b-11e8-91f6-86b0a47e4781.jpg)

* Power supply via Micro USB-B wth 5V.
  * Note `Amica` also has version with USB-C.
* CH340 USB interface.
* 11 digital I O-Pins. Max 3.3V! 1 analog I/O-Pin
  * The pins are not 5V tolerant. > 3.6V on any pin will destroy the chip.
  * Analog input voltage range from 0.0V to 1.0V ->  3.3V will damage the chip.
  * Maximum current that can be drawn from a single GPIO pin is 12mA.
* ESP-12E processor. The `E` versions has `wake` on GPIO16 after a timed `ESP.deepSleep()`.
  * Note `Amica` ESP-12 processor, and does not have `wake` on GPIO16.
* GPIO 0-15 all have a built-in pull up resistor
* GPIO16 has a built-in pull down resistor.
* GPIO 6-11 are used to connect the flash memory chip, and cannot be used.
* I/O pins have a special function during boot: GPIO15, GPIO0, GPIO2.
* 1 builtin led that is attached to D4/GPIO2. led is active at LOW.
  * Note `Amica` has an additional Led on GPIO16. 

## Blink sketch

Set board and port
* `Tools > Board > esp8266 > NodeMCU 1.0 (ESP - 12E Module)`
* `Tools > Port > COM6`
  * Found via Windows `Device Manager` -> `Ports (COM & LPT)` -> `Prolific USB-to-Serial Comm Port (COM6)`

The use the template
* `File > Examples > 01.Basics -> Blink`
* The library is designed for the Amica model. With the `Lolin V3`, change all "LED_BUILTIN" to "2" or "D4" and

### Enable flashing/uploading mode
If you try to upload a sketch and get error: 
`esptool.FatalError: Failed to connect to ESP8266: Timed out waiting for packet header` . It means that your ESP8266 is not in flashing/uploading mode.

* Hold-down the FLASH+RST buttons in your ESP8266 development board
* Press the Upload button in the Arduino IDE to upload your sketch
* When you see the  `Connecting...` message in your Arduino IDE, release FLASH+RST buttons
* After that, you should see the "Done uploading" message

### Blink code with serial

```C++
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
```


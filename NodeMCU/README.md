# Gas counter with NodeMCU

In this example, we will use [NodeMCU Lua Lolin V3](https://www.az-delivery.de/products/nodemcu-lolin-v3-modul-mit-esp8266). ESP-12E processor with ESP8266 WLAN module, with [Lolin, manual available here](https://www.az-delivery.de/products/nodemcu-lolin-v3-kostenfreies-e-book) and [NodeMCU LUA Amica V2, manual available here](https://www.az-delivery.de/products/nodemcu-amica-v2-kostenfreies-e-book). 

Both should be read, and driver installed for CH340 USB interface.

Install [Arduino IDE](https://www.arduino.cc/en/Main/Software).

Open Arduino IDE
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
  * Note `Amica` ESP-12 processor, and not `wake` on GPIO16.
* GPIO 0-15 all have a built-in pull up resistor
* GPIO16 has a built-in pull down resistor.
* GPIO 6-11 are used to connect the flash memory chip, and cannot be used.
* I/O pins have a special function during boot: GPIO15, GPIO0, GPIO2.
* 1 builtin led that is attached to D4/GPIO2. led is active at LOW.
  * Note `Amica` has an additional Led on GPIO16. 

## Blink sketch

* `Tools > Board > esp8266 > NodeMCU 1.0 (ESP - 12E Module)`
* Upload the sketch code to the NodeMCU board, select port on which  you connected the board. Go to:
  * `Tools > Port > {port name}`
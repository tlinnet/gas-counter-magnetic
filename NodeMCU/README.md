# Gas counter with NodeMCU

In this example, we used [NodeMCU Lua Amica Module V2](https://www.az-delivery.de/en/products/nodemcu). ESP-12F processor with ESP8266 WLAN module, with  [NodeMCU LUA Amica V2, manual available here](https://www.az-delivery.de/products/nodemcu-amica-v2-kostenfreies-e-book) and [Lolin, manual available here](https://www.az-delivery.de/products/nodemcu-lolin-v3-kostenfreies-e-book), where both should be read. 

Install [Arduino IDE](https://www.arduino.cc/en/Main/Software), and open Arduino IDE. Install board.
* `File > Preferences`. Additional URLs field= `https://arduino.esp8266.com/stable/package_esp8266com_index.json`
* `Tools > Board > Boards Manager`. Search `esp8266`. Install "esp8266 by ESP8266 Community".

`NodeMC` has this diagram.

![NodeMCU](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2017/10/Slide14-i.jpg?w=785&quality=100&strip=all&ssl=1)

* Power supply via Micro USB-B wth 5V. In this case, the `Amica` with USB-C.
* CP2102 USB interface.
* 11 digital I O-Pins. Max 3.3V! 1 analog I/O-Pin
  * The pins are not 5V tolerant. > 3.6V on any pin will destroy the chip.
  * Analog input voltage range from 0.0V to 1.0V ->  3.3V will damage the chip.
  * Maximum current that can be drawn from a single GPIO pin is 12mA.
* ESP-12F processor. The `E/F` versions has [`wake`](https://randomnerdtutorials.com/esp8266-deep-sleep-with-arduino-ide/) on GPIO16 after a timed `ESP.deepSleep()`.
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
  * Found via Windows `Device Manager` -> `Ports (COM & LPT)` -> `Silicon Labs CP210x USB to UART Bridge (COM3)`

The use the template
* `File > Examples > 01.Basics -> Blink`

### Enable flashing/uploading mode
If you try to upload a sketch and get error: 
`esptool.FatalError: Failed to connect to ESP8266: Timed out waiting for packet header` . It means that your ESP8266 is not in flashing/uploading mode.

* Hold-down the FLASH+RST buttons in your ESP8266 development board
* Press the Upload button in the Arduino IDE to upload your sketch
* When you see the  `Connecting...` message in your Arduino IDE, release FLASH+RST buttons
* After that, you should see the "Done uploading" message

### Blink code with serial

See code [Blink.ino](/NodeMCU/Blink/Blink.ino)


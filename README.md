# Gas (German GT4) counter via KY-021 Mini reed magnet

I live in Germany, near Stuttgart.
I have this gas box from my supplier. It's a GT4 G4 from 2005. It says that one magnetic pulse equals: 1 imp=0,01 m3. The red box is marking a place for putting a magnet for reading the pulses.

![Screenshot 2024-09-22 at 20 27 04](https://github.com/user-attachments/assets/efbeef47-f8ea-45c7-b602-e2f2553b8e2d)

I thought it could be a funny project to count the gas, and see our gas consumption is:

* if usage happens during showering in the morning
* or usage happens during heating in the night / evening

Plan:
* Find a magnetic sensor that picks up the magnetic pulse
* Collect the pulse and send data somewhere for calculation or viewing

I have an Raspberry Pi 4B, with the [Explorer Hat Pro](https://learn.pimoroni.com/article/getting-started-with-explorer-hat) from Pimoroni, which we will use for initial circuit
exploration on the mini breadboard. 

The Explorer Hat Pro is an older, now discontinued, product. I initially tried Raspberry Pi OS 64-bit Bookworm, but I got problems with python installation and sound card for the [examples/drums.py](https://github.com/pimoroni/explorer-hat/blob/master/examples/drums.py). After I downgraded to Legacy Bullseye, 64-bit, Lite, then installation and examples worked as intended.

## KY-021 circuit

I conveniently found someone selling 3d-printed plastic holder with KY-021 Mini reed magnet [for 16 euro on ebay.de](https://www.ebay.de/itm/176451806010).
The internal circuit is [depicted here](https://win.adrirobot.it/sensori/37_in_1/KY-021-Mini-magnetic-reed-module.htm) 

![KY-021 circuit](https://win.adrirobot.it/sensori/37_in_1/KY-021-Mini-magnetic-reed-modules/KY-021_Mini_magnetic_reed_module_circuito.jpg)

In the default configuration with sensor on the left pin, 5V on the middle pin and ground on the right pin, the internal 10k R1 resistor works as pull-up resistor. With no magnet, the reed contact is open, and with the pull-up transistor, we should measure a HIGH/1. With a magnet pulse, the contact closes and a LOW/0 is measured.

### Measuring with PullUp

If we use a Rasperry with a [PullUp/PullDown resistor](https://raspi.tv/2013/rpi-gpio-basics-6-using-inputs-and-outputs-together-with-rpi-gpio-pull-ups-and-pull-downs), we would normally initialize the GPIO input pin with something like `GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)`, to make sure it's initially not in a floating state. If the Pin is in a floating stage, it is susceptible to random electromagnetic radiation or static from you, from any devices near or far and from the environment. Using this command, we use built-in pull-up resistors which can be enabled in software.

BUT, when we use the Explorer Hat Pro, Pi's GPIO pin is after the buffer, [input signals will not be pulled up or down by enabling the Pi's onboard pull resistors](https://github.com/pimoroni/explorer-hat/blob/master/documentation/Technical-reference.md#inputs-via-sn74lvc125apwr-5v-tolerant-input-buffer).
So, we need to build a PullUp resistor ourselves.

![KY-021 circuit raspberry PullUpo](https://github.com/user-attachments/assets/87dbc3f9-97e2-464a-9ef5-7489603170bb)

With the code 
```python
#!/usr/bin/env python
import explorerhat

led = 0
pin = explorerhat.input.one

def changed(input):
  state = int(input.read())
  name  = input.name
  print("Input: {}={}".format(name,state))
  if state:
    explorerhat.light[led].off()
  else:
    explorerhat.light[led].on()

pin.changed(changed) # Set callback
print("Initial: ",end='')
changed(pin) # Get initial

explorerhat.pause()
```

### Measuring with PullDown

The idea is later to move to an ESP8266 running on a small battery pack. We will let it be in sleep-mode, and wake it up sending a HIGH signal to a pin.
If we can get our KY-021 to work with as a PullDown transistor, we should initially measure a LOW/0. With a magnet pulse, the contact closes and a HIGHT/1 is measured.
If we can use this HIGH signal, we could wake the ESP8266 up, connect to wifi and deliver reading to an MQTT Broker like Mosquitto.

To achieve this, switch 5V/GND on the KY-021 pins, make a 10k R between Input 1 and GND (instead of 5V) and swithc the on/off of led diode in code.

![20240922_233102](https://github.com/user-attachments/assets/4f1dddc0-7e42-49ba-8c1c-337a9bd8513b)

```python
#!/usr/bin/env python
import explorerhat

led = 1
pin = explorerhat.input.one

def changed(input):
  state = int(input.read())
  name  = input.name
  print("Input: {}={}".format(name,state))
  if state:
    explorerhat.light[led].on()
  else:
    explorerhat.light[led].off()

pin.changed(changed) # Set callback
print("Initial: ",end='')
changed(pin) # Get initial

explorerhat.pause()
```

## Collecting data

I have an GL.iNet GL-A1300 (Slate Plus) with OpenWrt 23.05 as an Access Point in my office. We will install mosquitto on it.

```bash
# Install
opkg update
opkg install mosquitto-ssl
opkg install mosquitto-client-ssl libmosquitto-ssl
/etc/init.d/mosquitto enable
/etc/init.d/mosquitto restart

# Create user gas counter
mosquitto_passwd -c /etc/mosquitto/passwd gasuser

# Edit
nano /etc/mosquitto/mosquitto.conf
# Set value
allow_anonymous false
password_file /etc/mosquitto/passwd
persistence true
persistence_file mosquitto.db
persistence_location /etc/mosquitto

# Restart
/etc/init.d/mosquitto restart
ls /etc/mosquitto/
grep -v '^#' /etc/mosquitto/mosquitto.conf 
```



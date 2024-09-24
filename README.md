* [Gas counter via KY-021 Mini reed magnet](#gas-counter-via-ky-021-mini-reed-magnet)
   * [KY-021 circuit](#ky-021-circuit)
      * [Measuring pulse with PullUp](#measuring-pulse-with-pullup)
      * [Measuring pulse with PullDown](#measuring-pulse-with-pulldown)
   * [Test send and receive data via MQTT message service](#test-send-and-receive-data-via-mqtt-message-service)
      * [Install mosquitto broker on OpenWrt router](#install-mosquitto-broker-on-openwrt-router)
      * [Test mosquitto message exchange on OpenWrt router](#test-mosquitto-message-exchange-on-openwrt-router)
      * [Test mosquitto message exchange on Raspberry](#test-mosquitto-message-exchange-on-raspberry)
   * [Collecting data via mosquitto](#collecting-data-via-mosquitto)

# Gas counter via KY-021 Mini reed magnet
Near Stuttgart, Germany, the gas box from the supplier is a GT4 G4 from 2005. It says that one magnetic pulse equals: 1 imp=0,01 m3. The red box is marking a place for putting a magnet for reading the pulses.

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

# KY-021 circuit

I conveniently found someone selling 3d-printed plastic holder with KY-021 Mini reed magnet [for 16 euro on ebay.de](https://www.ebay.de/itm/176451806010).
The internal circuit is [depicted here](https://win.adrirobot.it/sensori/37_in_1/KY-021-Mini-magnetic-reed-module.htm) 

![KY-021 circuit](https://win.adrirobot.it/sensori/37_in_1/KY-021-Mini-magnetic-reed-modules/KY-021_Mini_magnetic_reed_module_circuito.jpg)

In the default configuration with sensor on the left pin, 5V on the middle pin and ground on the right pin, the internal 10k R1 resistor works as pull-up resistor. With no magnet, the reed contact is open, and with the pull-up transistor, we should measure a HIGH/1. With a magnet pulse, the contact closes and a LOW/0 is measured.

## Measuring pulse with PullUp

If we use a Rasperry with a [PullUp/PullDown resistor](https://raspi.tv/2013/rpi-gpio-basics-6-using-inputs-and-outputs-together-with-rpi-gpio-pull-ups-and-pull-downs), we would normally initialize the GPIO input pin with something like `GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)`, to make sure it's initially not in a floating state. If the Pin is in a floating stage, it is susceptible to random electromagnetic radiation or static from you, from any devices near or far and from the environment. Using this command, we use built-in pull-up resistors which can be enabled in software.

BUT, when we use the Explorer Hat Pro, Pi's GPIO pin is after the buffer, [input signals will not be pulled up or down by enabling the Pi's onboard pull resistors](https://github.com/pimoroni/explorer-hat/blob/master/documentation/Technical-reference.md#inputs-via-sn74lvc125apwr-5v-tolerant-input-buffer).
So, we need to build a PullUp resistor ourselves.

![KY-021 circuit raspberry PullUpo](https://github.com/user-attachments/assets/87dbc3f9-97e2-464a-9ef5-7489603170bb)

With the code [up-input-event.py](https://github.com/tlinnet/gas-counter-magnetic/blob/main/raspberry/up-input-event.py) 

## Measuring pulse with PullDown

The idea is later to move to an ESP8266 running on a small battery pack. We will let it be in sleep-mode, and wake it up sending a HIGH signal to a pin.
If we can get our KY-021 to work with as a PullDown transistor, we should initially measure a LOW/0. With a magnet pulse, the contact closes and a HIGHT/1 is measured.
If we can use this HIGH signal, we could wake the ESP8266 up, connect to wifi and deliver reading to an MQTT Broker like Mosquitto.

To achieve this, switch 5V/GND on the KY-021 pins, make a 10k R between Input 1 and GND (instead of 5V) and swithc the on/off of led diode in code.

![20240922_233102](https://github.com/user-attachments/assets/4f1dddc0-7e42-49ba-8c1c-337a9bd8513b)

With the code [down-input-event.py](https://github.com/tlinnet/gas-counter-magnetic/blob/main/raspberry/down-input-event.py) 


# Test send and receive data via MQTT message service

I have an GL.iNet GL-A1300 (Slate Plus) with OpenWrt 23.05 as an Access Point in my office. We will install mosquitto on it to act as a broker.

## Install mosquitto broker on OpenWrt router 

```bash
# Install
opkg update
opkg install mosquitto-ssl
opkg install mosquitto-client-ssl libmosquitto-ssl
# Optional, if configuration via click in Luci is preferred.
# opkg install luci-app-mosquitto

# Make sure mosquitto service can read/write 
chown root:mosquitto /etc/mosquitto
chmod g+w /etc/mosquitto/
# Create mosquitto user: gasuser
mosquitto_passwd -c /etc/mosquitto/passwd gasuser
# Give passwword: helloworld
# Change owner
chown mosquitto:mosquitto /etc/mosquitto/passwd


# Edit configuration file
nano /etc/mosquitto/mosquitto.conf
# Set values
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883 0.0.0.0
persistence true
persistence_file mosquitto.db
persistence_location /etc/mosquitto

# Check
ls -la /etc/mosquitto/
grep -v '^#' /etc/mosquitto/mosquitto.conf | grep -v -e '^$'
mosquitto --verbose --config-file /etc/mosquitto/mosquitto.conf 
# If no errors then break.

# Enable, Restart
/etc/init.d/mosquitto enable
/etc/init.d/mosquitto restart
```

## Test mosquitto message exchange on OpenWrt router

Since, the Access Point is named `slateplus` in luci `system->system->hostname` we can use `slateplus.lan` as hostname.

Login 2x with ssh to the OpenWrt router.

```bash
# Try from 1 terminal and listen
mosquitto_sub -h slateplus.lan  -u "gasuser" -P "helloworld" -t test
# Publish from other terminal
mosquitto_pub -h slateplus.lan  -u "gasuser" -P "helloworld" -t test -m "Testing"
```

## Test mosquitto message exchange on Raspberry

Install mosquitto client on Raspberry

```bash
# Bash client
sudo apt-get update
sudo apt-get install mosquitto-clients
# Python module
sudo pip install paho-mqtt
```

Test publish with [--retain](https://mosquitto.org/man/mosquitto_pub-1.html).
When a client is subscribing, it always get retained messages-

```bash
# First Publish from other terminal
mosquitto_pub -h slateplus.lan  -u "gasuser" -P "helloworld" -r -t test -m "Testing Retain"

# Try from 1 terminal and see if retained message is there
mosquitto_sub -h slateplus.lan  -u "gasuser" -P "helloworld" -t test
```

With python code [paho-mqtt.py](https://github.com/tlinnet/gas-counter-magnetic/blob/main/raspberry/paho-mqtt.py), try to publish and watch subscription terminal.

# Collecting data via mosquitto


## Create another client user for listening
On OpenWrt router, create user and restart server

```bash
# Create user for reading
mosquitto_passwd -b /etc/mosquitto/passwd gasread Hello
# Pickup new password
/etc/init.d/mosquitto restart
```

## Test mosquitto message exchange from Raspberry with QoS 1 to 

Manuel for [`mosquitto_sub`](https://mosquitto.org/man/mosquitto_sub-1.html) and [`mqtt`](https://mosquitto.org/man/mqtt-7.html). Listen with QoS  and enable enable persistent client mode. With -v, topic is added prepended to message lines.

On OpenWrt router, listen

```bash
mosquitto_sub -h slateplus.lan  -u "gasread" -P "Hello" -v -t "sensors/gas/#" --qos 1 --id "gasread" --disable-clean-session 
```

On raspberry, run script [gas-sensor.py](https://github.com/tlinnet/gas-counter-magnetic/blob/main/raspberry/gas-sensor.py).

Try to keep making magnetic pulses, while breaking and connecting again `mosquitto_sub` and see all messages is received.

## init script for OpenWrt

We will make a [script that starts on boot](https://stackoverflow.com/questions/33340659/how-to-auto-start-an-application-in-openwrt) and save to file. The boot script [`gas_counter`](https://github.com/tlinnet/gas-counter-magnetic/blob/main/OpenWrt/etc/init.d/gas_counter) and the receive script [`recv_mosquitto.sh`](https://github.com/tlinnet/gas-counter-magnetic/blob/main/OpenWrt/root/recv_mosquitto.sh)

Make sure:
```bash
# Make executable
chmod +x /etc/init.d/gas_counter
chmod +x /root/recv_mosquitto.sh

# Enable and start
/etc/init.d/gas_counter enable
/etc/init.d/gas_counter enabled && echo on
/etc/init.d/mosquitto restart
```
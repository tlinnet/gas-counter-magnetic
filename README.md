# Gas (German GT4) counter via KY-021 Mini reed magnet

I live in Germany, near Stuttgart.

![Screenshot 2024-09-22 at 20 27 04](https://github.com/user-attachments/assets/efbeef47-f8ea-45c7-b602-e2f2553b8e2d)

I have this gas box from my supplier. It's a GT4 G4 from 2005. It says that one magnetic pulse equals: 1 imp=0,01 m3.

I thought it could be a funny project to count the gas, and see if our gas consumption is:

* If usage happens during showering in the morning
* or usage happens during heating in the night / evening

Plan:
* Find a magnetic sensor that picks up the magnetic pulse
* Collect the pulse and send data somewhere for calculation or viewing

I have an Raspberry Pi 4B, with the [Explorer Hat Pro](https://learn.pimoroni.com/article/getting-started-with-explorer-hat] from Pimoroni, which we will use for initial circuit
exploration on the mini breadboard. 

The Explorer Hat Pro is an older, now discontinued, product. I initially tried Raspberry Pi OS 64-bit Bookworm, but I got problems with python installation and sound card for the (examples/drums.py)[https://github.com/pimoroni/explorer-hat/blob/master/examples/drums.py]. After I downgraded to Legacy Bullseye, 64-bit, Lite, then installation and examples worked as intended.

## Initial circuit

I conveniently found someone selling 3d-printed plastic holder with KY-021 Mini reed magnet [for 16 euro on ebay.de](https://www.ebay.de/itm/176451806010).
The internal circuit is [depicted here](https://win.adrirobot.it/sensori/37_in_1/KY-021-Mini-magnetic-reed-module.htm) 

![KY-021 circuit](https://win.adrirobot.it/sensori/37_in_1/KY-021-Mini-magnetic-reed-modules/KY-021_Mini_magnetic_reed_module_circuito.jpg)

In the default configuration with sensor on the left pin, 5V on the middle pin and ground on the right pin, the internal 10k R1 resistor works as pull-up resistor. With no magnet, the reed contact is open, and with the pull-up transistor, we should measure a HIGH/1. With a magnet pulse, the contact closes and a LOW/0 is measured.

If we where programming direcly in Rasperry, 


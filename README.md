# Gas (German GT4) counter via KY-021 Mini reed magnet

I live in Germany, near Stuttgart.

![Screenshot 2024-09-22 at 20 27 04](https://github.com/user-attachments/assets/efbeef47-f8ea-45c7-b602-e2f2553b8e2d)

I have this gas box from my supplier. It says that one magnetic pulse equals: 1 imp=0,01 m3.
So, I thought it could be a funny project to count the gas, and see if our gas consumption is:

* If usage happens during showering in the morning
* or usage happens during heating in the night / evening

Plan:
* Find a magnetic sensor that picks up the magnetic pulse
* Collect the pulse and send data somewhere for calculation or viewing

I have an Raspberry Pi 4B, with the (Explorer Hat Pro)[https://learn.pimoroni.com/article/getting-started-with-explorer-hat] from Pimoroni.
We will use the RPI for the initial. The Explorer Hat Pro is an older, now discontinued, product. 

I initially tried Raspberry Pi OS 64-bit Bookworm, but I got problems with python installation and sound card for the (examples/drums.py)[https://github.com/pimoroni/explorer-hat/blob/master/examples/drums.py].
So I downgraded to Legacy Bullseye, 64-bit, Lite, and then installation and examples/d

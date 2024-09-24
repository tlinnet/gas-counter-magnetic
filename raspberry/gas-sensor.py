#!/usr/bin/env python
import explorerhat
import paho.mqtt.client as mqtt
from datetime import datetime as dt

led = 1
pin = explorerhat.input.one
counter = 0  

def changed(input):
    state = int(input.read())
    name  = input.name
    print("Input: {}={}".format(name,state))
    if state:
        explorerhat.light[0].on()
    else:
        explorerhat.light[0].off()

try:
    """
    # Do a try/except/finally to clean up
    # https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
    """
    pin.changed(changed) # Set callback
    print("Initial: ",end='')
    changed(pin) # Get initial

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username="gasuser", password="helloworld")
    client.connect(host="slateplus.lan", port=1883 , keepalive=60)

    explorerhat.pause()

except KeyboardInterrupt:  
    """
    Here you put any code you want to run before the program exits when you press CTRL+C  
    """
    print("############\n# break\n###########")

except:  
    """
    This catches ALL other exceptions including errors.  
    """
    print("############\n# Other error or exception occurred!#\n############")

finally:
    """"
    https://github.com/pimoroni/explorer-hat/blob/master/library/explorerhat/__init__.py#L86
    Does also GPIO.cleanup()
    """
    explorerhat.explorerhat_exit()
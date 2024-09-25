#!/usr/bin/env python
import explorerhat
import paho.mqtt.client as mqtt
from datetime import datetime as dt

led = 1
pin = explorerhat.input.one
topic = 'sensors/gas/pulse'
counter = 0  

def changed(input):
    global counter
    name  = input.name
    state = int(input.read())
    if state:
        explorerhat.light[led].on()
        counter += 1
        msg = f"{counter}; {dt.now()}"
        print(msg)
        # call `loop()` frequently to maintain network traffic flow with the broker
        client.publish(topic=topic,payload=msg, qos=1)
        client.loop()
    else:
        explorerhat.light[led].off()

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connection:", reason_code)

def on_connect_fail(client, userdata, flags, reason_code, properties=None):
    print("Fail Connection:", reason_code)

def on_disconnect(client, userdata, flags, reason_code, properties=None):
    print(reason_code)

try:
    """
    # Do a try/except/finally to clean up
    # https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi
    """
    pin.changed(changed) # Set callback

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username="gasuser", password="helloworld")
    client.connect(host="slateplus.lan", port=1883, keepalive=60)
    client.on_connect = on_connect
    client.on_connect_fail = on_connect_fail
    client.on_disconnect = on_disconnect
    # call `loop()` frequently to maintain network traffic flow with the broker
    client.loop()

    explorerhat.pause()

except KeyboardInterrupt:  
    """
    Here you put any code you want to run before the program exits when you press CTRL+C  
    """
    print("############\n# break\n###########")

#except:  
#    """
#    This catches ALL other exceptions including errors.  
#    """
#    print("############\n# Other error or exception occurred!#\n############")

finally:
    """"
    https://github.com/pimoroni/explorer-hat/blob/master/library/explorerhat/__init__.py#L86
    Does also GPIO.cleanup()
    """
    client.disconnect()
    explorerhat.explorerhat_exit()
#!/usr/bin/env python
import explorerhat
import paho.mqtt.client as mqtt
from datetime import datetime as dt

# MQTT
mqtt_host = "slateplus.lan"
mqtt_port = 1883
mqtt_user = "gasuser"
mqtt_password = "helloworld"
topic = 'sensors/gas/pulse'

# Raspberry
led = 1
pin = explorerhat.input.one
counter = 0


# MQTT Functions
def on_connect(client, userdata, flags, reason_code, properties=None):
    #print("Connection:", reason_code)
    pass

def on_connect_fail(client, userdata, flags, reason_code, properties=None):
    print("Fail Connection:", reason_code)

def on_disconnect(client, userdata, flags, reason_code, properties=None):
    #print(reason_code)
    pass

def get_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username=mqtt_user, password=mqtt_password)
    client.connect(host=mqtt_host, port=mqtt_port, keepalive=60)
    client.on_connect = on_connect
    client.on_connect_fail = on_connect_fail
    client.on_disconnect = on_disconnect
    # call `loop()` frequently to maintain network traffic flow with the broker
    client.loop()

    return client  

def changed(input):
    global counter
    name  = input.name
    state = int(input.read())
    if state:
        explorerhat.light[led].on()
        counter += 1
        msg = f"{counter}; {dt.now()}"
        print(msg)
        # Connect, Publish, Disconnect
        client = get_client()
        client.publish(topic=topic,payload=msg, qos=1)
        client.loop()
        client.disconnect()
    else:
        explorerhat.light[led].off()

# Do a try/except/finally to clean up
# https://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi

try:
    pin.changed(changed) # Set callback
    print("Ready for magnet pulse")
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
    print("Exiting")
    explorerhat.explorerhat_exit()
#!/usr/bin/env python

import paho.mqtt.client as mqtt
from datetime import datetime as dt

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connection:", reason_code)
    client.subscribe(topic="test")

def on_connect_fail(client, userdata, flags, reason_code, properties=None):
    print("Fail Connection:", reason_code)

def on_disconnect(client, userdata, flags, reason_code, properties=None):
    print(reason_code)

def on_message(client, userdata, message, properties=None):
    print(
        f"{dt.now()} Received message {message.payload} on topic '{message.topic}' with QoS {message.qos}"
    )

def on_subscribe(client, userdata, mid, qos, properties=None):
    print(f"{dt.now()} Subscribed with QoS {qos}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="gasuser", password="helloworld2")
client.connect(host="slateplus.lan", port=1883 , keepalive=60)
client.on_connect = on_connect
client.on_connect_fail = on_connect_fail
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe
# call `loop()` frequently to maintain network traffic flow with the broker
client.loop()

if client.is_connected():
    msg = f"Testing python {dt.now()}"
    print("Publishing:", msg)
    client.publish(topic='test',payload=msg, retain=True)
    client.loop()

# `loop_forever()` to handle calling `loop()` for you in a blocking function.
# Listen for traffic
client.loop_forever()

#!/usr/bin/env python

import paho.mqtt.client as mqtt
from datetime import datetime as dt

def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(topic="test")

def on_message(client, userdata, message, properties=None):
    print(
        f"{dt.now()} Received message {message.payload} on topic '{message.topic}' with QoS {message.qos}"
    )

def on_subscribe(client, userdata, mid, qos, properties=None):
    print(f"{dt.now()} Subscribed with QoS {qos}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.username_pw_set(username="gasuser", password="helloworld")
client.connect(host="slateplus.lan", port=1883 , keepalive=60)

# qos Defaults to 0.
client.publish(topic='test',payload=f"Testing python {dt.now()}", retain=True)

client.disconnect() # Publish and exit
# client.loop_forever() # Publish and stay and listen

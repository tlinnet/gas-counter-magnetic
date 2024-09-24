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

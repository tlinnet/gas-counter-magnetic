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

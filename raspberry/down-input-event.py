#!/usr/bin/env python
import explorerhat

led = 1
pin = explorerhat.input.one

def changed(input):
  state = int(input.read())
  name  = input.name
  print("Input: {}={}".format(name,state))
  if state:
    explorerhat.light[0].on()
  else:
    explorerhat.light[0].off()

pin.changed(changed) # Set callback
print("Initial: ",end='')
changed(pin) # Get initial

explorerhat.pause()

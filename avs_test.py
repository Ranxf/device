#! /usr/bin/python

import xin300
import apc
import time,re
import pexpect

console = xin300.xin300()
apc = apc.apc()
outlet = '8'
usbport = '/dev/ttyUSB0'
spawn_id = console.connect(usbport,'UBOOT.*#')
#console.reset_to_system()
apc.connect("192.168.1.90","> ")
apc.login("ap","ap")
apc.enter_outlet_menu()
t = 1 
while True:
    apc.outlet_cmd(outlet,"2")
    print("sleep %d seconds"%t)
    time.sleep(t)
    apc.outlet_cmd(outlet,"1")
    
    index = spawn_id.expect(['Linux version 2.6.37',pexpect.TIMEOUT])
    if index == 0:
         print("-------------AVS test passed------------------\n")
         t = t - 1
         if t < 0:
             break
         pass
    elif index == 1:
         print("-------------AVS test Failed------------------\n")
         t = t + 1
         pass

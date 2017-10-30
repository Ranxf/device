#! /usr/bin/python

import apc
import time
import sys

"""
     1- Immediate On
     2- Immediate Off
     3- Immediate Reboot
     4- Delayed On
     5- Delayed Off
     6- Delayed Reboot
     7- Cancel
"""

outlet = sys.argv[1]
action = sys.argv[2]
x = apc.apc()
x.connect("192.168.1.90", "> ")
x.login("ap","ap")
x.enter_outlet_menu()
x.outlet_cmd(outlet,action)

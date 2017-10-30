#! /usr/bin/python

import xin300
import sys

def xin300_reboot(port,times):
    cur=1
    fd=open(port,'w')
    while (cur < int(times)):
        fd.write("current reboot %s times %s ---------------\n"%(port,cur))
        x.reset_to_system()
        cur=cur+1
        fd.flush()
    fd.close()
x = xin300.xin300()


usbport = sys.argv[1]
times = sys.argv[2]
print "/dev/%s"%usbport
print times
spawn_id = x.connect('/dev/%s'%usbport,'UBOOT.*#')
xin300_reboot(usbport,times)


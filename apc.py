#! /usr/bin/python

import re,sys,os
import pexpect
import datetime
import time

class apc:
    def connect(self,ip,prompt):
        self.spawn_id = pexpect.spawn('telnet ' + ip)
        self.spawn_id.logfile=open("log/apc.out-" + str(datetime.datetime.now()) + ".log",'w')
        self.spawn_id.logfile_read = sys.stdout
        self.prompt = prompt
        return self.spawn_id

    def login(self,user,passwd):
        self.spawn_id.expect("User Name :")
        self.spawn_id.send(user + "\r")
        self.spawn_id.expect("Password  :")
        self.spawn_id.send(passwd + "\r")
        self.spawn_id.expect("Control Console")
        self.spawn_id.send("\r")
        self.spawn_id.expect(self.prompt)
        return self.spawn_id
    def enter_outlet_menu(self):
        self.spawn_id.send("\r")
        self.spawn_id.expect("Device Manager")    
        self.spawn_id.expect(self.prompt)
        self.spawn_id.send("1\r")
        self.spawn_id.expect(self.prompt)
        self.spawn_id.send("2\r")
        self.spawn_id.expect(self.prompt)
        self.spawn_id.send("1\r")
        self.spawn_id.expect(self.prompt)
        return
    def outlet_cmd(self,outlet,command):
        self.spawn_id.send(str(outlet) + "\r")
        self.spawn_id.expect(self.prompt)
        self.spawn_id.send(str(command) + "\r")
        self.spawn_id.expect("Enter \'YES\' to continue or <ENTER> to cancel :")
        self.spawn_id.send("YES\r")
        self.spawn_id.expect('Press <ENTER> to continue\.\.\.')
        self.spawn_id.send("\r")
        self.spawn_id.expect(self.prompt)
        self.spawn_id.send("")
        self.spawn_id.expect(self.prompt)
        return
    def enter_main_menu(self):
        p = re.compile("Control Console")
        while True:  
            self.spawn_id.send("")
            self.spawn_id.expect(self.prompt)
            if(p.search(self.spawn_id.before)):
                break

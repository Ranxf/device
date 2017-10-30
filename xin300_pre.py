#! /usr/bin/python

import re,sys,os
import pexpect
import datetime
import time


class xin300:
    def connect(self,con,prompt):
        self.spawn_id = pexpect.spawn('minicom -D ' + con)
        self.spawn_id.logfile=open("log/expect.out-" + str(datetime.datetime.now()) + ".log",'w')
        self.spawn_id.logfile_read = sys.stdout
        self.uboot_prompt = prompt
        self.system_prompt = "root@.*#"
        return self.spawn_id

    def nand_scrub(self):
        self.spawn_id.sendline("nand scrub")
        self.spawn_id.expect("<y/N>")
        self.spawn_id.send("y\r")
        self.spawn_id.expect("OK")
        return

    def reset_to_uboot(self):
        self.spawn_id.send("\n")
        while True:  
            index = self.spawn_id.expect([self.uboot_prompt,self.system_prompt])  
            if index == 0:  
                self.spawn_id.sendline("reset")
                self.spawn_id.expect("Hit any key to stop autoboot")
                self.spawn_id.send("\n")
                self.spawn_id.expect(self.uboot_prompt)
                break
            elif index == 1:  
                self.spawn_id.sendline("reboot")
                self.spawn_id.expect("Unmounting")
                self.spawn_id.expect("Hit any key to stop autoboot")
                self.spawn_id.sendline("\n")
                self.spawn_id.expect(self.uboot_prompt)
                break 

    def reset_to_system(self):
        self.spawn_id.send("\n")
        while True:
            index = self.spawn_id.expect([self.uboot_prompt,self.system_prompt])
            if index == 0:  
                self.spawn_id.sendline("reset")
                self.spawn_id.expect("Hit any key to stop")
                time.sleep(5)
                self.spawn_id.send("\n")
                self.spawn_id.expect(self.system_prompt,timeout=500)
                break
            elif index == 1:  
                self.spawn_id.sendline("reboot")
                self.spawn_id.expect("Hit any key to stop")
                time.sleep(5)
                self.spawn_id.send("\n")
                self.spawn_id.expect(self.system_prompt,timeout=500)
                break

    def enter_uboot_mode(self):
        self.spawn_id.send("\n")
        while True:  
            index = self.spawn_id.expect('Hit any key to stop autoboot',timeout=500)  
            self.spawn_id.send("\n")
            self.spawn_id.expect(self.uboot_prompt)
            break
                
    def config_uboot_env(self,ip):
        self.spawn_id.sendline("setenv ipaddr " + ip)
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("setenv gatewayip 192.168.1.9")
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("setenv netmask 255.255.255.0")
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("setenv serverip 192.168.1.9")
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("setenv bootargs \'console=ttyO2,115200n8 noinitrd ip=" + ip + " mem=256M rootwait=1 rw ubi.mtd=8,2048 rootfstype=ubifs root=ubi0:rootfs init=/init vram=20M notifyk.vpssm3_sva=0xBEE00000 stdin=serial ddr_mem=1024M\'")
        self.spawn_id.expect(self.uboot_prompt)
        # delete extra arguments
        self.spawn_id.sendline("setenv 'noinitrd rw ubi.mtd'")
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("setenv ip")
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("saveenv")
        self.spawn_id.expect(self.uboot_prompt)

    def write_uboot_bin(self,ubootf):
        self.config("ls", self.uboot_prompt)
        self.spawn_id.sendline("mw.b 0x81000000 0xFF 0x260000")
        self.spawn_id.expect(self.uboot_prompt)
        self.spawn_id.sendline("tftp 0x81000000 " + ubootf)
        self.spawn_id.expect("Load address: ",timeout=500)
        self.spawn_id.expect("done",timeout=500)
        self.spawn_id.expect('transferred =\s+(\d+)\s+\(0x(.*)\)',timeout=500)
        size = self.spawn_id.match.group(2)
        if size <= 0:
	    raise("transferred error")
        # adjust size to 1k
        size = "0x%x" % ((int(size,16)+0x1000)/0x1000*0x1000)

        self.config("nandecc hw 2", self.uboot_prompt)
        self.config("nand erase 0x0 " + size, self.uboot_prompt)
        self.spawn_id.sendline("nand write.i 0x81000000  0x0 " + size)
        index = self.spawn_id.expect("written: OK",timeout=120)
        if index == 0:
            return
        else:
            raise("not written ok")

    def config(self,cmd,prompt):
        self.spawn_id.sendline(cmd)
        index = self.spawn_id.expect(prompt,timeout=1200)
        if index == 0:
            return self.spawn_id.before
        else:
            raise("%s command execute error" % cmd)
    
    def write_kernel_bin(self,kernelf):
        self.config("ls", self.uboot_prompt)
        self.config("mw.b 0x81000000 0xFF 0x300000",self.uboot_prompt)
        self.spawn_id.sendline("tftp 0x81000000 " + kernelf)
        self.spawn_id.expect("Load address: ",timeout=500)
        self.spawn_id.expect("done",timeout=500)
        self.spawn_id.expect('transferred =\s+(\d+)\s+\(0x(.*)\)',timeout=500)
        size = self.spawn_id.match.group(2)
        # adjust size to 1k
        size = "0x%x" % ((int(size,16)+0x1000)/0x1000*0x1000)

        self.config("nand erase 0x00580000 " + size, self.uboot_prompt)
        self.spawn_id.sendline("nand write.i 0x81000000  0x00580000 " + size)
        index = self.spawn_id.expect("written: OK",timeout=120)
        if index == 0:
            return
        else:
            raise("not written ok")
    

    def write_fs_bin(self,fsf):
        self.config("ls", self.uboot_prompt)
        self.config("mw.b 0x81000000 0xFF 0x4000000",self.uboot_prompt)
        self.spawn_id.sendline("tftp 0x81000000 " + fsf)
        self.spawn_id.expect("Load address: ",timeout=500)
        self.spawn_id.expect("done",timeout=500)
        self.spawn_id.expect('transferred =\s+(\d+)\s+\(0x(.*)\)',timeout=500)
        size = self.spawn_id.match.group(2)
        # adjust size to 1k
        size = "0x%x" % ((int(size,16)+0x10000)/0x1000*0x1000)

        self.config("nand erase 0x009c0000 " + size, self.uboot_prompt)
        self.spawn_id.sendline("nand write 0x81000000 0x009c0000 " + size)
        index = self.spawn_id.expect("written: OK",timeout=500)
        # clean last command
        if index == 0:
            self.spawn_id.sendline("ls")
            return
        else:
            self.spawn_id.sendline("ls")
            raise("not written ok")
    

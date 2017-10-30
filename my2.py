#! /usr/bin/python

import xin300

def upgrade_firmware(ip,date):
    x.config_uboot_env(ip)
    x.nand_scrub()
    x.write_uboot_bin(date + "/xzrs_uboot.bin")
    x.config_uboot_env(ip)
    x.reset_to_uboot()
    x.write_kernel_bin(date + "/xzrs_uimage.bin")
    x.write_fs_bin(date + "/xzrs_fs.bin")
    x.reset_to_system()

x = xin300.xin300()

spawn_id = x.connect('/dev/ttyUSB2','UBOOT.*#')
x.reset_to_uboot()
#x.reset_to_system()
ip="192.168.1.132"
date="2016-5-10"

#x.config_uboot_env(ip)
upgrade_firmware(ip,date)


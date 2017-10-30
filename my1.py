#! /usr/bin/python

import xin300

def upgrade_firmware(ip,date):
    x.config_uboot_env(ip)
    x.nand_scrub()
    x.write_uboot_bin(date + "/dm8168/xzrs_uboot_dm8168")
    x.config_uboot_env(ip)
    x.reset_to_uboot()
    x.write_kernel_bin(date + "/dm8168/xzrs_uimage_dm8168")
    x.write_fs_bin(date + "/dm8168/xzrs_fs_dm8168")
    x.reset_to_system()

x = xin300.xin300()

spawn_id = x.connect('/dev/ttyUSB0','UBOOT.*#')
x.reset_to_uboot()
#x.reset_to_system()
ip="192.168.1.210"
date="2016-10-9"

#x.config_uboot_env(ip)
upgrade_firmware(ip,date)


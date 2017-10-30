#! /usr/bin/python

import xin300_8148

def upgrade_firmware(ip,date):
    x.config_uboot_env(ip)
    x.nand_scrub()
    x.write_first_uboot_bin(date + "/dm8148/xzrs_uboot_nand_dm8148")
    x.write_uboot_bin(date + "/dm8148/xzrs_uboot_dm8148")
    x.config_uboot_env(ip)
    x.reset_to_uboot()
    x.write_kernel_bin(date + "/dm8148/xzrs_uimage_dm8148")
    #x.write_kernel_bin(date + "/dm8148/uImage-20170316")
    x.write_fs_bin(date + "/dm8148/xzrs_fs_dm8148")
    #x.write_fs_bin(date + "/dm8148/ubi_128_DM814X_TI_EVM.img")
    x.reset_to_system()

x = xin300_8148.xin300_8148()
spawn_id = x.connect('/dev/ttyUSB2', '8148_EVM#')
x.reset_to_uboot()
ip = "192.168.1.146"
date = "2017-4-7_zhongtianxin"
upgrade_firmware(ip, date)
x.change_root_passwd()
x.get_serial()

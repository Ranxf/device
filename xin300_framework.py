#! /usr/bin/python

import device
import job
import logging
import xin300_8148
import xin300

class xin300_fmwk:
      def __init__(self):
            self.job = {}
            self.pre_running_job = {}
            self.running_job = {}
            self.runned_job = {}
            self.obsolate_job = {}
            self.task = {}

            self.device_lock = {}
            self.device_queue = {}
          
            logging.basicConfig(filename="/tmp/xin300_frm.log",level="INFO")
            logging.info("framework init start")

      def get_submit_jobs(self):
           # get all submitted jobs
           j = job.job()
           j.get_all_jobs()
           self.job = j.jobs
           logging.info("framework init start %s",self.job)

      def update_device(self):
           # get all devices
           dev = device.device()
           dev.get_all_device()
           self.device_queue = dev.device

      def check_job(self):
           # check job content are correct
           # put correct job to pre_running_job
           for j in self.job.keys():
                 for m in self.device_queue.keys():
                       if m not in self.device_lock:
                             #logging.info("job %s, device %s",j,m)
                             if self.job[j]["model"] == self.device_queue[m]["model"]:
                                   self.pre_running_job[j] = self.job.pop(j)
                                   self.device_lock[m] = self.device_queue[m]
                                   self.task[j] = m
                                   logging.info("job queue %s",self.job)
                                   logging.info("lock %s",self.device_lock)
                                   logging.info("job task %s, device %s" , j,self.task[j])
                                   break
                       else:
                             logging.info("found job %s require device %s", j, m)
      def run_job(self):
          for j in self.task.keys():
              if self.pre_running_job[j]["firmware"]["reimage"]:
                    m = self.task[j]
                    date = self.pre_running_job[j]["firmware"]["date"]
                    con = self.device_queue[m]["xin300"]["console"]["port"]
                    ip = self.device_queue[m]["xin300"]["ip"]
                    model = self.device_queue[m]["model"]
                    prompt = self.device_queue[m]["xin300"]["console"]["prompt"]
                    if model == "dm8148":
                          x = xin300_8148.xin300_8148()
                          x.connect(con,prompt)
                          self.upgrade_firmware_8148(x,ip,date)
                    elif model == "dm8168":
                          x = xin300.xin300()
                          x.connect(con,prompt)
                          self.upgrade_firmware_8168(x,ip,date)

      def upgrade_firmware_8148(self,x,ip,date):
          x.reset_to_uboot()
          x.config_uboot_env(ip)
          x.nand_scrub()
          x.write_first_uboot_bin(date + "/dm8148/xzrs_uboot_nand_dm8148")
          x.write_uboot_bin(date + "/dm8148/xzrs_uboot_dm8148")
          x.config_uboot_env(ip)
          x.reset_to_uboot()
          x.write_kernel_bin(date + "/dm8148/xzrs_uimage_dm8148")
          x.write_fs_bin(date + "/dm8148/xzrs_fs_dm8148")
          x.reset_to_system()
      def upgrade_firmware_8168(self,x,ip,date):
          x.config_uboot_env(ip)
          x.nand_scrub()
          x.write_uboot_bin(date + "/dm8168/xzrs_uboot_dm8168")
          x.config_uboot_env(ip)
          x.reset_to_uboot()
          x.write_kernel_bin(date + "/dm8168/xzrs_uimage_dm8168")
          x.write_fs_bin(date + "/dm8168/xzrs_fs_dm8168")
          x.reset_to_system()


if __name__ == "__main__":
      
      xin_fmwk = xin300_fmwk()
      xin_fmwk.get_submit_jobs()
      xin_fmwk.update_device()
      xin_fmwk.check_job()
      xin_fmwk.run_job()
       
      #print(xin_fmwk.job)
      #print(xin_fmwk.device_queue)

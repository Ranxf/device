#! /usr/bin/python

import yaml
import glob
import os


class job:
      
      def __init__(self):
           self.jobs={}
           self.jobs_dir=r'job/*.yaml'
      def get_all_jobs(self):

          file_list=glob.iglob(self.jobs_dir)

          for  f in file_list:
              name=f[4:-5]
              with open(f) as fd:
                  self.jobs[name]= yaml.load(fd)

      def mv_job_old(self,job):
	  file_list=glob.iglob(self.jobs_dir)
          job_f = 'job/' + job + '.yaml'
          if job_f in file_list:
              os.system("mv " + job_f + " " + job_f+'.old')

if __name__ == '__main__':
      x = job()
      x.get_all_jobs()
      for f in x.jobs:
          x.mv_job_old(f)

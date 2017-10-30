#! /usr/bin/python

import yaml
import glob


class device:
      
      def __init__(self):
           self.device={}
           self.device_dir=r'device/*.yaml'
      def get_all_device(self):

          file_list=glob.iglob(self.device_dir)

          for  f in file_list:
              name=f[7:-5]
              with open(f) as fd:
                  self.device[name]= yaml.load(fd)

if __name__ == '__main__':
      x = device()
      x.get_all_device()

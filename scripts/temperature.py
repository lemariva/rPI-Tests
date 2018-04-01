#!/usr/bin/env python
import os, sys, time
from datetime import datetime


class tempControl():
    def __init__(self, filename=None):
        self._filename = filename
        
        if(self._filename is not None):
            with open(self._filename, "w") as myfile:
                myfile.write("time,cpu_temp,gpu_temp\n")
            
    def get_gpu_temp(self):
        res = os.popen('vcgencmd measure_temp').readline()
        res = float(res.replace('temp=','').replace('\'C\n',''))
        return res

    def get_cpu_temp(self):
        res = float(os.popen("cat /sys/class/thermal/thermal_zone0/temp").read())/1000
        return res

    def get_temp(self):
        return self.get_cpu_temp(), self.get_gpu_temp()
        
    def save_temp(self):
        now = datetime.now()
        now_epoch = now.strftime('%s')

        if(self._filename is not None):
            with open(self._filename, "a") as myfile:
                myfile.write("%s, %.2f, %.2f \n" %(now_epoch, self.get_cpu_temp(), self.get_gpu_temp()))
        
        print("cpu: %.2f gpu: %.2f \n" %(self.get_cpu_temp(), self.get_gpu_temp()))


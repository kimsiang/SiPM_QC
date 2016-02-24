# A wrapper Class for the BK Precision 9124 Power Supply
import serial
import u3
import urllib2 as url
from urllib import quote

class BKPrecision:

    def __init__(self, dev_path, baud=4800, timeout=1):
        self.s = serial.Serial(dev_path, baud, timeout=timeout)
#        print '%s' % self.get_version()
   	#self.id = int(self.get_version().split(',')[-2][-4:])

    def get_version(self):
        self.s.write('*IDN?\n')
        return self.s.read(64).strip()

    def get_state(self):
        self.s.write('OUTP:STAT?\n')
        return self.s.read(64).strip()

    def meas_volt(self):
        self.s.write('MEAS:VOLT?\n')
        return self.s.read(64).strip()

    def get_volt(self):
	self.s.write('LIST:VOLT?\n')

    def set_volt(self, new_volt):
	self.s.write('SOUR:VOLT ' + str(new_volt) + '\n')

    def input_cmd(self, cmd):
	self.s.write(cmd + '\n')
	return self.s.read(64).strip()

    def power_on(self):
	self.s.write('OUTPUT ON\n')

    def power_off(self):
	self.s.write('OUTPUT OFF\n')

    def meas_curr(self):
	self.s.write('MEAS:CURR?\n')
	return self.s.read(64).strip()

    def get_curr(self):
	self.s.write('LIST:CURR?\n')
	return self.s.read(64).strip()

    def set_curr(self, new_curr):
	self.s.write('SOUR:CURR ' + str(new_curr) + '\n')


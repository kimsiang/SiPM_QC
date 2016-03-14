# slow_control_server.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
from labjack import labjack
from bk_precision import BKPrecision
import json


class SlowControl():

    def __init__(self):
        print 'Slow control initiated!'
        self.lj = labjack()
        #self.bk = BKPrecision('/dev/ttyUSB0')
        self.block = False
        #self.__volt=0
        #self.__curr=0


    def lj_server(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        port="5556"
        socket.bind("tcp://*:%s" % port)
        print "Running LJ server on port: ", port

        while True:
            if not self.block:
                self.read_temp()
                self.read_gain()
                self.read_eeprom()
                self.read_serial()
                self.read_led()
                socket.send('[{0}][{1}][{2}][{3}][{4}][{5}]'.format(self.get_time(),
                    self.__temp,self.__gain,self.__eeprom,self.__serial,self.__led_no))
                self.dump_info()
                time.sleep(5)

    def client(self):
        port_push="5556"
        context = zmq.Context()
        socket_pull = context.socket(zmq.PULL)
        socket_pull.connect("tcp://localhost:%s" % port_push)
        print "Connected to server with port %s" % port_push
        # Initialize poll set
        poller = zmq.Poller()
        poller.register(socket_pull, zmq.POLLIN)

        # Work on requests from server
        while True:
            socks = dict(poller.poll(200))
            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
                self.block = True
                msg = socket_pull.recv()
                print "Recieved control command: %s" % msg

                if msg[0:8] == "SetGain ":
                    print '[{0}] Received msg {1}'.format(self.get_time(),msg)
                    gain=int(msg[8:])
                    self.set_gain(gain)

                elif msg[0:7] == "SetLED ":
                    print '[{0}] Received msg {1}'.format(self.get_time(),msg)
                    led_no=int(msg[7:])
                    self.set_led(led_no)

                elif msg[0:6] == "SiPM# ":
                    print '[{0}] Received msg {1}'.format(self.get_time(),msg)
                    sipm_no=int(msg[6:])
            else:
                self.block = False


    ## Get time in a specific format
    def get_time(self):
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    ## T-sensor
    def read_temp(self):
        self.__temp = float(self.lj.read_temperature())

    def read_gain(self):
        self.__gain = float(self.lj.read_gain())

    def set_gain(self,gain):
        self.lj.set_gain(gain)

    def read_eeprom(self):
        _readout = self.lj.read_eeprom(1)
        for _idx,_i in enumerate(_readout):
            if _i == 0xff:
                _readout[_idx] = 32
        _array = [chr(_i) for _i in _readout]
        self.__eeprom = ''.join(_array)

    def read_serial(self):
        _readout = self.lj.read_eeprom(1)
        for _idx,_i in enumerate(_readout):
            if _i == 0xff:
                _readout[_idx] = 32
        _array = [chr(_i) for _i in _readout]
        _string = ''.join(_array)
        _array = _string.split(' ')
        if len(_array) == 3 and _array[0] == _array[2] and _array[1] == 'UWSiPM':
            self.__serial = int(_array[0])
        else:
            self.__serial = 0

    def read_led(self):
        self.__led_no = self.lj.read_led()

    def set_led(self,led):
        self.lj.set_led(led)

#    def read_volt(self):
#        if(self.bk.meas_volt()):
#            self.__volt = float(self.bk.meas_volt())
#        else:
#            self.__volt = -1

#    def read_curr(self):
#        if(self.bk.meas_curr()):
#            self.__curr = float(self.bk.meas_curr())*1000
#        else:
#            self.__curr = -1

    def dump_info(self):
        log_dict = {
               'Datetime': self.get_time(),
               'Temperature': self.__temp,
               'Gain': self.__gain,
               'Serial_No': self.__serial,
               'Led_No': self.__led_no,
               }

        json_outfile = open('../gui/modular/data/log/current.log', 'w')
        json.dump(log_dict, json_outfile, indent=4, sort_keys=True)



slowctrl = SlowControl()

Process(target=slowctrl.client, args=()).start()
Process(target=slowctrl.lj_server, args=()).start()
#Process(target=slowctrl.bk_server, args=()).start()


# slow_control_server.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
from labjack import Labjack
from bk_precision import BKPrecision
import json


class SlowControl():

    def __init__(self):
        print 'Slow control initiated!'
        self.bk = BKPrecision('/dev/ttyUSB0')
        self.lj = Labjack()

    def get_time(self):
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    def lj_server(self):
        # define socket numbers for push and publish ports
        lj_port_push = "5556"
        lj_port_pub = "5566"

        # create pull socket for receiving commands from GUI
        context = zmq.Context()
        socket_pull = context.socket(zmq.PULL)
        socket_pull.connect("tcp://localhost:%s" % lj_port_push)
        print "Connected to server with port %s" % lj_port_push

        # initialize poll set
        poller = zmq.Poller()
        poller.register(socket_pull, zmq.POLLIN)

        # initialize labjack publisher
        socket_pub = context.socket(zmq.PUB)
        socket_pub.bind("tcp://*:%s" % lj_port_pub)
        print "Publish info with port %s" % lj_port_pub

        # work on requests from SiPM GUI
        while True:
            socks = dict(poller.poll(2000))

            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
                msg = socket_pull.recv()
                print '{0} Received control command: {1}'.format(
                    self.get_time(), msg)

                # interpret the GUI messages here
                if msg == "read temp":
                    print self.lj.read_temp()
                elif msg == "read gain":
                    print self.lj.read_gain()
                elif msg == "read pga":
                    print self.lj.read_pga()
                elif msg == "read eeprom":
                    print self.lj.read_eeprom()
                elif msg == "read led":
                    print self.lj.read_led()
                elif msg[0:10] == "set eeprom":
                    print self.lj.write_eeprom(int(msg[11:12]), msg[13:29])
                elif msg[0:7] == "set led":
                    print self.lj.set_led(int(msg[8:]))
                elif msg[0:8] == "set gain":
                    print self.lj.set_gain(int(msg[9:]))
                else:
                    print "Unknown command! Try again."

            else:
                temp = self.lj.read_temp()
                gain = self.lj.read_gain()
                eeprom1 = self.lj.read_eeprom(1)
                eeprom2 = self.lj.read_eeprom(2)
                eeprom3 = self.lj.read_eeprom(3)
                eeprom4 = self.lj.read_eeprom(4)
                eeprom5 = self.lj.read_eeprom(5)
                eeprom6 = self.lj.read_eeprom(6)
                eeprom7 = self.lj.read_eeprom(7)
                eeprom8 = self.lj.read_eeprom(8)
                serial = self.lj.read_serial()
                led_no = self.lj.read_led()

                lj_data = {
                    'time': self.get_time(),
                    'temp': temp,
                    'gain': gain,
                    'eeprom1': eeprom1,
                    'eeprom2': eeprom2,
                    'eeprom3': eeprom3,
                    'eeprom4': eeprom4,
                    'eeprom5': eeprom5,
                    'eeprom6': eeprom6,
                    'eeprom7': eeprom7,
                    'eeprom8': eeprom8,
                    'serial': serial,
                    'ledno': led_no
                }

                socket_pub.send_json(lj_data)

    def bk_server(self):
        # define socket numbers for push and publish ports
        bk_port_push = "5557"
        bk_port_pub = "5567"

        # create pull socket for receiving commands from GUI
        context = zmq.Context()
        socket_pull = context.socket(zmq.PULL)
        socket_pull.connect("tcp://localhost:%s" % bk_port_push)
        print "Connected to server with port %s" % bk_port_push

        # initialize poll set
        poller = zmq.Poller()
        poller.register(socket_pull, zmq.POLLIN)

        # initialize bk publisher
        socket_pub = context.socket(zmq.PUB)
        socket_pub.bind("tcp://*:%s" % bk_port_pub)
        print "Publish info with port %s" % bk_port_pub

        # work on requests from SiPM GUI
        while True:
            socks = dict(poller.poll(2000))

            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
                msg = socket_pull.recv()
                print '{0} Received control command: {1}'.format(
                    self.get_time(), msg)

                # interpret the GUI messages here
                if msg == "power on":
                    print self.bk.power_on()
                elif msg == "power off":
                    print self.bk.power_off()
                elif msg == "get state":
                    print self.bk.get_state()
                elif msg == "read volt":
                    print float(self.bk.meas_volt())
                elif msg == "read curr":
                    print float(self.bk.meas_curr())
                elif msg[0:8] == "set volt":
                    self.bk.set_volt(float(msg[9:]))
                elif msg[0:8] == "set curr":
                    self.bk.set_curr(float(msg[9:]))
                else:
                    print "Unknown command, try again."

            else:
                volt = self.bk.meas_volt()
                curr = self.bk.meas_curr()
                state = self.bk.get_state()

                bk_data = {
                    'time': self.get_time(),
                    'volt': volt,
                    'curr': curr,
                    'state': state
                }

                socket_pub.send_json(bk_data)


# main function
def main():
    slowctrl = SlowControl()
    Process(target=slowctrl.bk_server, args=()).start()
    Process(target=slowctrl.lj_server, args=()).start()

if __name__ == '__main__':
    main()

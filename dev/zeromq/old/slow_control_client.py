# slow_control_server.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process


class SlowControl():

    def __init__(self):
        print 'Slow control initiated!'

    def client(self,port_push="5557"):
        context = zmq.Context()
        socket_pull = context.socket(zmq.PULL)
        socket_pull.connect("tcp://localhost:%s" % port_push)
        print "Connected to server with port %s" % port_push

        # Initialize poll set
        poller = zmq.Poller()
        poller.register(socket_pull, zmq.POLLIN)

        # Work on requests from server
        should_continue = True
        while should_continue:
            socks = dict(poller.poll())
            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
                message = socket_pull.recv()
                print "Recieved control command: %s" % message


    def server_push(self,port="5557"):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.bind("tcp://*:%s" % port)
        print "Running server on port: ", port

#        socket.send('SetGain 20')
        for i in range(16):
            socket.send('SetLED {}'.format(i+1))
#            socket.send('SiPM# {}'.format(i+1))
            time.sleep(1)

slowctrl = SlowControl()
Process(target=slowctrl.client, args=()).start()
Process(target=slowctrl.server_push, args=()).start()

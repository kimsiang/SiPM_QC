import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

while True:
        msg = socket.recv()
        print 'received msg:{}'.format(msg)
        print 'follow instruction in msg'
        socket.send("do this")
        time.sleep(1)

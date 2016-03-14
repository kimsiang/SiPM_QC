import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

while True:
        socket.send("slow control msg to GUI")
        msg = socket.recv()
        print msg
        time.sleep(1)

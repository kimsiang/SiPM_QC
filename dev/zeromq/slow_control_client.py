
import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
from bk_precision import BKPrecision


context = zmq.Context()
#print("Connecting DRS4 Server")
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5557")
#print("Sending request")
socket.send ("power on")
socket.send ("read curr")
socket.send ("read volt")
socket.send ("set volt 60")
time.sleep(3)
socket.send ("read volt")
socket.send ("set volt 30")
time.sleep(3)
socket.send ("read volt")
time.sleep(3)
socket.send ("read curr")
socket.send ("read volt")


context = zmq.Context()
socket_sub1 = context.socket(zmq.SUB)
socket_sub2 = context.socket(zmq.SUB)

socket_sub1.connect("tcp://localhost:%s" % 5566)
socket_sub2.connect("tcp://localhost:%s" % 5567)

socket_sub1.setsockopt(zmq.SUBSCRIBE, "")
socket_sub2.setsockopt(zmq.SUBSCRIBE, "")


while True:
    json_data1 = socket_sub1.recv_json()
    json_data2 = socket_sub2.recv_json()
    print('{0}'.format(json_data1))
    print('{0}'.format(json_data2))

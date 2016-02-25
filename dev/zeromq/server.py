import zmq
import time
import sys
import random
from multiprocessing import Process


def server_push(port="5556"):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%s" % port)
    print "Running server on port: ", port
    # serves only 5 request and dies
    for reqnum in range(100):
        if reqnum < 96:
            socket.send("Hello I am Kim")
        else:
            socket.send("Exit")
            break
        time.sleep(1)

server_push_port = "5556"
Process(target=server_push, args=(server_push_port,)).start()

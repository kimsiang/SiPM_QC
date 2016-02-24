import zmq
import time
import sys
import random
from multiprocessing import Process


def client(port_push):
    context = zmq.Context()
    socket_pull = context.socket(zmq.PULL)
    socket_pull.connect("tcp://localhost:%s" % port_push)
    print "Connected to server with port %s" % port_push

    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket_pull, zmq.POLLIN)

    # Work on requests from both server and publisher
    should_continue = True
    while should_continue:
        socks = dict(poller.poll())
        if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
            message = socket_pull.recv()
            print "Recieved control command: %s" % message
            if message == "Exit":
                print "Received exit command, client will stop receiving messages"
                should_continue = False


if __name__ == "__main__":
    # Now we can run a few servers
    server_push_port = "5556"
    Process(target=client, args=(server_push_port,)).start()
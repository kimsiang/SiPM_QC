#!/usr/bin/python

# drs4.py

import zmq
from multiprocessing import Process
import json

class DRS4():

    def __init__(self):

        ## kill any instances of drs4_exam and sipm_qc.py
        _proc = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, shell=True)
        (out, err) = _proc.communicate()

        for line in out.splitlines():
            if 'drs_exam' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

        ## logging drs_exam output
        fw = open("tmpout", "wb")
        self.drs4_proc = subprocess.Popen("/home/midas/KimWork/drs-5.0.3/drs_exam",
                stdin=subprocess.PIPE, stderr=fw, stdout=subprocess.PIPE)
        for line in iter(self.drs4_proc.stdout.readline, b''):
            if 'Invalid magic number' in line:
                print 'Invalid Magic number! Please replug DRS4 USB Cable!'
            elif 'Could not set frequency' in line:
                print 'Could not set frequency for DRS4! Please replug DRS4 USB Cable!'
            elif 'Please begin the measurement' in line:
                self.drs4_proc.stdin.write('begin\n')
                return True


    def drs4_ready(self):
        for line in iter(self.drs4_proc.stdout.readline, b''):
            if 'Please enter the (SiPM#, Run type, Subrun#, Seq#)' in line:
                print 'Please enter the SiPM#'
                return 'True'

    def zmq_client(self, port_push):
        context = zmq.Context()
        socket_pull = context.socket(zmq.PULL)
        socket_pull.connect("tcp://localhost:%s" % port_push)
        #print "Connected to server with port %s" % port_push

        # Initialize poll set
        poller = zmq.Poller()
        poller.register(socket_pull, zmq.POLLIN)

        # Work on requests from server
        should_continue = True
        while should_continue:
            socks = dict(poller.poll())
            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
                message = socket_pull.recv()
                print "Received control command: %s" % message
                self.drs4_proc.stdin.write('{0:04d} {1} {2:02d} {3:05d}\n'.format(self.__serial,self.__type,self.__subrun_no,self.__seq_no))
                if message == "Exit":
                    #print "Received exit command, client will stop receiving messages"
                    should_continue = False




def main():

    if __name__ == '__main__':
        main()

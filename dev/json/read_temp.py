from datetime import datetime
import time, sys
import u3
import Gnuplot
import json
import serial
import slow_control as sc
import zmq
import random
port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
#socket.setsockopt(zmq.RCVTIMEO, 50)
socket.bind("tcp://*:%s" % port)

d = u3.U3()
#d.debug = True
spi_conf_temp = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 8,
	"CLKPinNum": 12,
	"MISOPinNum": 15,
	"MOSIPinNum": 14
	}

spi_conf_pga = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 11,
	"CLKPinNum": 12,
	"MISOPinNum": 9,
	"MOSIPinNum": 14
}


dev_path = '/dev/ttyUSB0'
aa = open("temp_log.txt", "a+",0)

def read_temp():
	#make sure pga CS is high
	d.setDOState(spi_conf_pga['CSPINNum'], 1)
	data = d.spi([0x50, 0x00, 0x00, 0x00], **spi_conf_temp)
	res = data['SPIBytes']
        temp = (res[1] << 8 | res[2]) / 128.0
        return temp

def setup_temp():
	#make sure pga CS is high
	d.setDOState(spi_conf_pga['CSPINNum'], 1)
	data = d.spi([0x08, 0x80], **spi_conf_temp)

def read_gain():
	#make sure temp chip CS is high
	d.setDOState(spi_conf_temp['CSPINNum'], 1)

        res = d.spi([0x83, 0x00], **spi_conf_pga)
	gain_read = res['SPIBytes'][1]
        return ( 26.0 - gain_read / 4.0 )

if __name__ == "__main__":

        bk_dev = sc.BKPrecision(dev_path)
	for i in range(500000):
#		time.sleep(1)
		temp=read_temp()
                gain=read_gain()
                volt = bk_dev.meas_volt()
                curr = bk_dev.meas_curr()
 #               socket.send("slow control msg to GUI")
  #              msg = socket.recv()
   #             print msg
               # del bk_dev

                #print >> aa, time.strftime("%Y/%m/%d %H:%M:%S"), temp, gain, volt, curr
                print >> aa, time.time(), temp, gain, volt, curr

                #data = {'Time': time.strftime("%Y/%m/%d %H:%M:%S"),
                data = {'Time': time.time(),
                        'Temperature': temp, 'Gain': gain, 'HV' : volt, 'I' :
                        curr}
                json_file = open("test.json","w")
                json.dump(data, json_file)
                json_file.close()

aa.close()

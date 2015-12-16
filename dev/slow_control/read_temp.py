import time, sys
import u3
import Gnuplot
import json

d = u3.U3()
#d.debug = True

spi_conf_temp = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 14,
	"CLKPinNum": 15,
	"MISOPinNum": 17,
	"MOSIPinNum": 16
	}

spi_conf_pga = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 18,
	"CLKPinNum": 15,
	"MISOPinNum": 19,
	"MOSIPinNum": 16
}

aa = open("temp_log.txt", "a+",0)

json_file = open("test.json","w")


def read_temperature():
	#make sure pga CS is high
	d.setDOState(spi_conf_pga['CSPINNum'], 1)
	data = d.spi([0x50, 0x00, 0x00, 0x00], **spi_conf_temp)
	res = data['SPIBytes']
        temp = (res[1] << 8 | res[2]) / 128.0
	print >> aa, time.strftime("%Y/%m/%d %H:%M:%S"), temp
        data = {'Time': time.strftime("%Y/%m/%d %H:%M:%S"), 'Temperature': temp}
        return json.dump(data, json_file)

def setup_temperature():
	#make sure pga CS is high
	d.setDOState(spi_conf_pga['CSPINNum'], 1)
	data = d.spi([0x08, 0x80], **spi_conf_temp)

if __name__ == "__main__":

	for i in range(50000):
		time.sleep(1)
		read_temperature()
aa.close()

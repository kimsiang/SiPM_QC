import time, sys
import u3
import Gnuplot

d = u3.U3()

spi_conf_temp = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 9,
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

spi_conf_eeprom = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 14,
	"CLKPinNum": 15,
	"MISOPinNum": 17,
	"MOSIPinNum": 16
	}


#adt7320 id and status
#spi.writebytes([0x40])
#res = spi.readbytes(1)
#print res
#status
#res = spi.xfer2([0x40, 0x00])

def set_gain(gain):
	GPIO.output("P9_15", GPIO.HIGH)

	res = spi.xfer2([0x83, 0x00])
	print "old gain: %d" % res[1]

	res = spi.xfer2([0x03, gain])
	#print res

	res = spi.xfer2([0x83, 0x00])
	print "new gain: %d = %f dB" % (res[1], 26 - res[1] / 4.0)


def check_eeprom_status():
	res = spi.xfer2([0x05, 0x00])
	print "eeprom status 0x%02x\n" % res[1]

def write_eeprom(page, msg):
	print "writing %s to page %d\n" % (msg, page)
	check_eeprom_status()

	page <<= 4

	print "enable write latch"
	spi.xfer2([0x06])
	check_eeprom_status()

	print "write page"
	cmd = [0x02, page] + msg
	res = spi.xfer2(cmd)
	print res
	check_eeprom_status()

	print "read page"
	cmd = [0x03, page] + [0 for i in range(16)]
	res = spi.xfer2(cmd)
	print res
	check_eeprom_status()

	print "read eeprom"
	cmd = [0x03, 0] + [0 for i in range(8*16)]
	res = spi.xfer2(cmd)
	print res


if __name__ == "__main__":
	GPIO.setup("P9_11", GPIO.OUT)
	GPIO.setup("P9_12", GPIO.OUT)
	GPIO.setup("P9_13", GPIO.OUT)
	GPIO.setup("P9_14", GPIO.OUT)
	GPIO.setup("P9_15", GPIO.OUT)

	#spi = SPI()
	#spi.open(0, 0)
	#spi.msh = 0

	spi = SpiDev(1,0)
	spi.mode = 3
	spi.max_speed_hz = 100000


	check_eeprom_status()
	write_eeprom(3, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

	GPIO.cleanup()
	spi.close()



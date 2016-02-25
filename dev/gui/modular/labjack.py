#!/usr/bin/python

#labjack.py

import u3
d = u3.U3 ()
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

spi_conf_eeprom = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 10,
	"CLKPinNum": 12,
	"MISOPinNum": 15,
	"MOSIPinNum": 14
}

class labjack():

    def __init__(self):
#        print 'LabJack U3-LV initiated!'
        pass

    def read_temperature(self):
	#make sure pga and eeprom CS are high
	d.setDOState(spi_conf_pga['CSPINNum'], 1)
	d.setDOState(spi_conf_eeprom['CSPINNum'], 1)
	data = d.spi([0x50, 0x00, 0x00, 0x00], **spi_conf_temp)
	res = data['SPIBytes']
        temp = (res[1] << 8 | res[2]) / 128.0
                #threading.Timer(1.0, self.read_temperature).start()
        #print >> aa, time.strftime("%m-%d/%H:%M:%S"), temp
        return "%.2f" % temp

    def setup_temperature(self):
	#make sure pga and eeprom CS are high
	d.setDOState(spi_conf_pga['CSPINNum'], 1)
	d.setDOState(spi_conf_eeprom['CSPINNum'], 1)
	data = d.spi([0x08, 0x80], **spi_conf_temp)

    def read_gain(self):
	#make sure temp chip and eeprom CS are high
	d.setDOState(spi_conf_temp['CSPINNum'], 1)
	d.setDOState(spi_conf_eeprom['CSPINNum'], 1)

        res = d.spi([0x83, 0x00], **spi_conf_pga)
	gain_read = res['SPIBytes'][1]
        return ( 26.0 - gain_read / 4.0 )
        #print "old gain readout: %d = %f dB" % (gain_read, 26 - gain_read / 4.0)

    def set_gain(self,gain_value):
	#make sure temp chip and eeprom CS are high
	d.setDOState(spi_conf_temp['CSPINNum'], 1)
	d.setDOState(spi_conf_eeprom['CSPINNum'], 1)
        gain_value = 4 * (26 - gain_value)
        res = d.spi([0x03, gain_value], **spi_conf_pga)

        #res = d.spi([0x83, 0x00], **spi_conf_pga)
	#gain_read = res['SPIBytes'][1]
        #print "new gain readout: %d = %f dB" % (gain_read, 26 - gain_read / 4.0)

    def check_eeprom_status(self):
	#make sure temp and pga chips CS are high
	#d.setDOState(spi_conf_eeprom['CSPINNum'], 0)
	d.setDOState(spi_conf_temp['CSPINNum'], 1)
	d.setDOState(spi_conf_pga['CSPINNum'], 1)

        res = d.spi([0x05, 0x00], **spi_conf_eeprom)
#	print "eeprom status 0x%02x\n" % res['SPIBytes'][1]

    def write_eeprom(self, page, msg):
#	print "writing %s to page %d\n" % (msg, page)
	self.check_eeprom_status()

	page <<= 4

#	print "enable write latch"
	res = d.spi([0x06], **spi_conf_eeprom)
	self.check_eeprom_status()

#	print "write page"
	cmd = [0x02, page] + msg
        res = d.spi(cmd, **spi_conf_eeprom)
#	print res['SPIBytes']
	self.check_eeprom_status()

#	print "read page"
        cmd = [0x03, page] + [0 for i in range(16)]
        res = d.spi(cmd, **spi_conf_eeprom)
 #       print res['SPIBytes'][2:]
	self.check_eeprom_status()

	#print "read eeprom"
	#cmd = [0x03, 0] + [0 for i in range(8*16)]
	#cmd = [0x03] + [0 for i in range(8*16)]
	#res = d.spi(cmd, **spi_conf_eeprom)
	#print res['SPIBytes']


    def read_eeprom(self, page):
#        print "Reading page %d of EEPROM ......\n" % page
	page <<= 4
        cmd = [0x03, page] + [0 for i in range(16)]
        res = d.spi(cmd, **spi_conf_eeprom)
#        er_safe_int = res['SPIBytes'][2:]
#        for idx,i in enumerate(res['SPIBytes'][2:]):
#            if i == 0xff:
#                er_safe_int[idx] = 32
#        return [chr(i) for i in er_safe_int]
        return res['SPIBytes'][2:]

    def set_led(self, led_number):
        if led_number == 1:
            d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 2:
	    d.getFeedback(u3.BitStateWrite(16,0))
            d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 3:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 4:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 5:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 6:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 7:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 8:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 9:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 10:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 11:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 12:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 13:
	    d.getFeedback(u3.BitStateWrite(16,0))
	    d.getFeedback(u3.BitStateWrite(17,0))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 14:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,0))

        elif led_number == 15:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,0))
	    d.getFeedback(u3.BitStateWrite(19,1))

        elif led_number == 16:
	    d.getFeedback(u3.BitStateWrite(16,1))
	    d.getFeedback(u3.BitStateWrite(17,1))
	    d.getFeedback(u3.BitStateWrite(18,1))
	    d.getFeedback(u3.BitStateWrite(19,1))


#led = LEDBoard()
#led.On(1)

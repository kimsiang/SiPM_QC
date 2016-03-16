#!/usr/bin/python

# labjack.py

import u3
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


class Labjack():

    def __init__(self):
        # print 'LabJack U3-LV initiated!'
        pass

    def read_temp(self):
        # make sure pga and eeprom CS are high
        d.setDOState(spi_conf_pga['CSPINNum'], 1)
        d.setDOState(spi_conf_eeprom['CSPINNum'], 1)
        data = d.spi([0x50, 0x00, 0x00, 0x00], **spi_conf_temp)
        res = data['SPIBytes']
        temp = (res[1] << 8 | res[2]) / 128.0
        return "%.2f" % temp

    def setup_temp(self):
        # make sure pga and eeprom CS are high
        d.setDOState(spi_conf_pga['CSPINNum'], 1)
        d.setDOState(spi_conf_eeprom['CSPINNum'], 1)
        data = d.spi([0x08, 0x80], **spi_conf_temp)

    def read_gain(self):
        # make sure temp chip and eeprom CS are high
        d.setDOState(spi_conf_temp['CSPINNum'], 1)
        d.setDOState(spi_conf_eeprom['CSPINNum'], 1)

        res = d.spi([0x83, 0x00], **spi_conf_pga)
        gain_read = res['SPIBytes'][1]
        return (26.0 - gain_read / 4.0)

    def set_gain(self, gain_value):
        # make sure temp chip and eeprom CS are high
        d.setDOState(spi_conf_temp['CSPINNum'], 1)
        d.setDOState(spi_conf_eeprom['CSPINNum'], 1)
        gain_value = 4 * (26 - gain_value)
        res = d.spi([0x03, gain_value], **spi_conf_pga)

    def check_eeprom_status(self):
        # make sure temp and pga chips CS are high
        # d.setDOState(spi_conf_eeprom['CSPINNum'], 0)
        d.setDOState(spi_conf_temp['CSPINNum'], 1)
        d.setDOState(spi_conf_pga['CSPINNum'], 1)

        res = d.spi([0x05, 0x00], **spi_conf_eeprom)
        # print "eeprom status 0x%02x\n" % res['SPIBytes'][1]

    def write_eeprom(self, page, msg):
        # print "writing %s to page %d\n" % (msg, page)
        self.check_eeprom_status()
        page <<= 4

        # print "enable write latch"
        res = d.spi([0x06], **spi_conf_eeprom)
        self.check_eeprom_status()

        # convert string to int array
        string_list = list(msg)
        int_array = [ord(s) for s in string_list]

        # Add spaces if the length is smaller than 16
        while len(int_array) < 16:
            int_array.append(32)

        cmd = [0x02, page] + int_array
        res = d.spi(cmd, **spi_conf_eeprom)
        self.check_eeprom_status()

        # print "read page"
        cmd = [0x03, page] + [0 for i in range(16)]
        res = d.spi(cmd, **spi_conf_eeprom)
        self.check_eeprom_status()

    def read_eeprom(self, page):
        # print "Reading page %d of EEPROM ......\n" % page
        page <<= 4
        cmd = [0x03, page] + [0 for i in range(16)]
        res = d.spi(cmd, **spi_conf_eeprom)

        # join all the 16 bytes into a string
        readout = res['SPIBytes'][2:]
        for idx, i in enumerate(readout):
            if i == 0xff:
                readout[idx] = 32
        array = [chr(i) for i in readout]
        return ''.join(array)

    def read_serial(self):
        cmd = [0x03, 16] + [0 for i in range(16)]
        res = d.spi(cmd, **spi_conf_eeprom)
        readout = res['SPIBytes'][2:]

        for idx, i in enumerate(readout):
            if i == 0xff:
                readout[idx] = 32
        array = [chr(i) for i in readout]
        string = ''.join(array)
        array = string.split(' ')

        # return SiPM serial number
        if len(array) == 3 and array[0] == array[2] and array[1] == 'UWSiPM':
            return int(array[0])
        else:
            return 0

    def set_led(self, led_no):
        # convert led_number into binary format
        binary = format(led_no-1, "#06b")
        array = list(binary)

        d.getFeedback(u3.BitStateWrite(16, int(array[2])))
        d.getFeedback(u3.BitStateWrite(17, int(array[3])))
        d.getFeedback(u3.BitStateWrite(18, int(array[4])))
        d.getFeedback(u3.BitStateWrite(19, int(array[5])))

    def read_led(self):
        # encode led channel number in a binary string
        read = []
        read.append(d.getFeedback(u3.BitStateRead(16))[0])
        read.append(d.getFeedback(u3.BitStateRead(17))[0])
        read.append(d.getFeedback(u3.BitStateRead(18))[0])
        read.append(d.getFeedback(u3.BitStateRead(19))[0])

        array = [str(i) for i in read]
        binary = ''.join(array)
        led_no = int(binary, 2) + 1

        return led_no

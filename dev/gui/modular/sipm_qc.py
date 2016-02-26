#!/usr/bin/python

# sipm_qc.py

## Import all needed libraries
import wx
import wx.lib.agw.flatnotebook as fnb
from threading import Thread
from bk_precision import BKPrecision
from labjack import labjack
from sipm_qc_gui import control_panel, display_panel, eeprom_panel, logger_panel
import time, sys, subprocess, os, threading, signal
from datetime import date, datetime, tzinfo, timedelta
import zmq
from multiprocessing import Process
import json

## Define the MainFrame
class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=wx.EmptyString,
                          pos=wx.DefaultPosition,
                          size=wx.Size(1400, 700),
                          style=wx.DEFAULT_FRAME_STYLE |
                          wx.TAB_TRAVERSAL)

#        self.Centre(wx.BOTH)

    def __del__(self):
        pass

class Panel1(control_panel):

    def __init__(self, parent):
        control_panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour('silver')

class Panel2(display_panel):

    def __init__(self, parent):
        display_panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour('silver')

class Panel3(eeprom_panel):

    def __init__(self, parent):
        eeprom_panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour('silver')

class Panel4(logger_panel):

    def __init__(self, parent):
        logger_panel.__init__(self, parent)
        self.parent = parent

class NoteBook(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)

        ## Add menu bar
        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(22, '&Quit', 'Exit Panel Control')
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        wx.EVT_MENU(self, 22, self.on_close)

        # Here we create a panel and a notebook on the panel
        self.nb = fnb.FlatNotebook(self)

        # create the page windows as children of the notebook
        self.page1 = Panel1(self.nb)
        self.page2 = Panel2(self.nb)
        self.page3 = Panel3(self.nb)
        self.page4 = Panel4(self)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(self.page1, 'Control')
        self.nb.AddPage(self.page2, 'Display')
        self.nb.AddPage(self.page3, 'EEPROM')

        # finally, put the notebook in a sizer for the panel to manage the layout
        grid = wx.GridBagSizer(hgap=10, vgap=10)

        # start of grid
        grid.Add(self.nb, pos=(0, 0), span=(1,2), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.page4, pos=(0, 2), flag=wx.TE_RIGHT)
        self.SetSizerAndFit(grid)

        # start process for zmq polling
        server_push_port = "5556"
        Process(target=self.zmq_client, args=(server_push_port,)).start()

        # define private variabls for status checking
        self.__volt=0.0
        self.__curr=0.0
        self.__temp=0.0
        self.__gain=0.0
        self.__serial=0
        self.__led_no=0
        self.__seq_no=0
        self.__sipm_status=False
        self.__bk_status=False

        # initialize all the environment and do the layout
        self.init_daq()
        self.init_thread()
        self.bind_bk()
        self.bind_led()
        self.bind_pga()
        self.bind_eeprom()
        self.bind_drs4()
        self.do_logger_binding()

        # redo layout realign all the variables
        self.page1.Layout()
        ### end of __init__


    def init_daq(self):
        ## initialize BK precision
        self.page4.logger.AppendText('[{0}] ### Start SiPM QC Station ###\n'.format(self.get_time()))

        self.bk = BKPrecision('/dev/ttyUSB0')

        if self.bk:
            self.page4.logger.AppendText('[{0}] # BK initialized\n'.format(self.get_time()))

        ## initialize Labjack U3-LV

        self.lj = labjack()

        if self.lj:
            self.page4.logger.AppendText('[{0}] # Labjack initialized\n'.format(self.get_time()))

        ## initialize drs4
        self.init_drs4()

        self.page4.logger.AppendText('[{}] #####################\n'.format(self.get_time()))

        self.read_bk_state()
        self.read_volt()
        self.read_curr()
        self.read_temp()
        self.read_pga()
        self.read_eeprom()
        self.read_serial()
        self.read_led()

    def init_thread(self):
        ## initialize threads for labjack and bk to refresh variables
        self.t1=Thread(target=self.refresh_lj)
        self.t2=Thread(target=self.refresh_bk)
        self.t1.start()
        self.t2.start()

    def bind_bk(self):
        ## bind the BK buttons to update the display and call bk.set_volt etc
        self.Bind(wx.EVT_BUTTON, self.update_bk_state, self.page1.lblname1s)
        self.Bind(wx.EVT_BUTTON, self.update_volt, self.page1.lblname2s)
        self.Bind(wx.EVT_BUTTON, self.update_curr, self.page1.lblname3s)

    def bind_led(self):
        ## bind the LED buttons to update the display and call labjack.set_led()
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led1)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led2)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led3)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led4)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led5)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led6)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led7)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led8)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led9)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led10)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led11)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led12)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led13)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led14)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led15)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led16)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.led16)
        self.Bind(wx.EVT_BUTTON, self.update_led, self.page1.lblname7s)

    def bind_pga(self):
        ## bind the PGA buttons to update the display and call labjack.read_pga()
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button5)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button6)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button7)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button8)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.lblname6s)

    def bind_eeprom(self):
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem1s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem2s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem3s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem4s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem5s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem6s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem7s)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem8s)
        self.Bind(wx.EVT_BUTTON, self.update_serial, self.page1.lblname4s)

    def bind_drs4(self):
        self.Bind(wx.EVT_BUTTON, self.run_drs4, self.page1.drs4_button)

    def do_logger_binding(self):
        # do all the logger bindings
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.drs4_button)

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_spin, self.page1.lblname2w)
        self.Bind(wx.EVT_SPINCTRL, self.on_spin, self.page1.lblname3w)
        self.Bind(wx.EVT_SPINCTRL, self.on_spin, self.page1.lblname4w)
        self.Bind(wx.EVT_SPINCTRL, self.on_spin, self.page1.lblname6w)
        self.Bind(wx.EVT_SPINCTRL, self.on_spin, self.page1.lblname7w)

        self.Bind(wx.EVT_BUTTON, self.on_switch, self.page1.lblname1s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page1.lblname2s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page1.lblname3s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page1.lblname4s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page1.lblname6s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page1.lblname7s)

        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button1)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button2)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button3)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button4)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button5)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button6)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button7)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button8)

        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led1)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led2)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led3)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led4)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led5)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led6)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led7)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led8)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led9)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led10)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led11)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led12)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led13)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led14)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led15)
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.led16)

        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem1s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem2s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem3s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem4s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem5s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem6s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem7s)
        self.Bind(wx.EVT_BUTTON, self.on_set, self.page3.mem8s)

    def on_click(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.page4.logger.AppendText('[{0}] Clicked on {1}\n'.format(self.get_time(), labeltext))
        event.Skip()

    def on_spin(self, event):
        self.page4.logger.AppendText(
                '[%s] %s to %.1f\n' % (self.get_time(), event.GetEventObject().GetName(),event.GetValue()))
        event.Skip()

    def on_switch(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.page4.logger.AppendText('[{0}] Clicked on {1}\n'.format(self.get_time(), labeltext))
        event.Skip()

    def on_set(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        unit = ''
        if labeltext == 'Set V':
            value = self.page1.lblname2w.GetValue()
            unit = 'V'
        elif labeltext == 'Set I':
            value = self.page1.lblname3w.GetValue()
            unit = 'mA'
        elif labeltext == 'Set SiPM#':
            value = self.page1.lblname4w.GetValue()
        elif labeltext == 'Set Gain':
            value = self.page1.lblname6w.GetValue()
            unit = 'dB'
        elif labeltext == 'Set LED#':
            value = self.page1.lblname7w.GetValue()
        elif labeltext == 'Set Page1':
            value = self.page3.mem1w.GetValue()
        elif labeltext == 'Set Page2':
            value = self.page3.mem2w.GetValue()
        elif labeltext == 'Set Page3':
            value = self.page3.mem3w.GetValue()
        elif labeltext == 'Set Page4':
            value = self.page3.mem4w.GetValue()
        elif labeltext == 'Set Page5':
            value = self.page3.mem5w.GetValue()
        elif labeltext == 'Set Page6':
            value = self.page3.mem6w.GetValue()
        elif labeltext == 'Set Page7':
            value = self.page3.mem7w.GetValue()
        elif labeltext == 'Set Page8':
            value = self.page3.mem8w.GetValue()

        self.page4.logger.AppendText('[{0}] {1} to {2} {3}\n'.format(self.get_time(), labeltext, value, unit))
        event.Skip()

    def init_drs4(self):

        ## kill any instances of drs4_exam
        _proc = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, shell=True)
        (out, err) = _proc.communicate()

        for line in out.splitlines():
            if 'drs_exam' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
                self.page4.logger.AppendText('[{0}] # Killed running DRS4 \n'.format(self.get_time()))

        ## logging drs_exam output
        fw = open("tmpout", "wb")
        fr = open("tmpout", "r")
        self.drs4_proc = subprocess.Popen("/home/midas/KimWork/drs-5.0.3/drs_exam",
            stdin=subprocess.PIPE, stderr=fw,stdout=fw, bufsize=1)
        if self.drs4_proc:
            self.page4.logger.AppendText('[{0}] # DRS4 initialized\n'.format(self.get_time()))

    #### define functions for BK Precision
    def bk_on(self, event):
        self.bk.power_on()
        self.page1.lblname2r.SetLabel('ON')
        event.Skip()

    def bk_off(self, event):
        self.bk.power_off()
        self.page1.lblname2r.SetLabel('OFF')
        event.Skip()

    def update_bk_state(self, event):
        label = event.GetEventObject().GetLabelText()
        if label == 'Turn ON':
            self.bk.power_on()
            self.page1.lblname1r.SetLabel('ON')
            self.page1.lblname1s.SetLabel('Turn OFF')
        elif label == 'Turn OFF':
            self.bk.power_off()
            self.page1.lblname1r.SetLabel('OFF')
            self.page1.lblname1s.SetLabel('Turn ON')
        event.Skip()

    def read_bk_state(self):
        if(self.bk.get_state()):
            state = self.bk.get_state()
            if state == '1':
                self.page1.lblname1r.SetLabel('ON')
                self.page1.lblname1s.SetLabel('Turn OFF')
            elif state == '0':
                self.page1.lblname1r.SetLabel('OFF')
                self.page1.lblname1s.SetLabel('Turn ON')
        else:
            pass

    def read_volt(self):
        if(self.bk.meas_volt()):
            self.__volt = float(self.bk.meas_volt())
            self.page1.lblname2r.SetLabel('{:.2f}'.format(self.__volt))
            #print 'V={0} V'.format(volt)
        else:
            self.__volt = -1
            self.page1.lblname2r.SetLabel('')

    def update_volt(self, event):
        setvalue = self.page1.lblname2w.GetValue()
        self.bk.set_volt(setvalue)
        wx.CallAfter(self.read_volt)
        event.Skip()

    def read_curr(self):
        if(self.bk.meas_curr()):
            self.__curr = float(self.bk.meas_curr())*1000
            self.page1.lblname3r.SetLabel(str(self.__curr))
            #print 'I={0} mA'.format(curr)
        else:
            self.__curr = -1
            self.page1.lblname3r.SetLabel('')

    def update_curr(self, event):
        setvalue = self.page1.lblname3w.GetValue()
        self.bk.set_curr(setvalue/1000.)
        wx.CallAfter(self.read_curr)
        event.Skip()

    def check_bk_status(self):
        _bk_status = self.__bk_status
        if self.__volt < 0 and self.__curr < 0:
            self.page1.lblname9r.SetLabel('NO')
            self.__bk_status = False
            if _bk_status == True:
                    self.page4.logger.AppendText('[{0}] BK Precision is powered off!\n'.format(self.get_time()))


        elif self.__volt > -1 and self.__curr > -1:
            self.page1.lblname9r.SetLabel('YES')
            self.__bk_status = True
            if _bk_status == False:
                    self.page4.logger.AppendText('[{0}] BK Precision is powered on!\n'.format(self.get_time()))
                    self.read_bk_state()

    def refresh_bk(self):
        while True:
            wx.CallAfter(self.read_volt)
            wx.CallAfter(self.read_curr)
            wx.CallAfter(self.check_bk_status)
            time.sleep(10)


    #### define functions for Labjack

    ## T-sensor
    def read_temp(self):
        self.__temp = float(self.lj.read_temperature())
        self.page1.lblname5r.SetLabel(str(self.__temp))
        #print 'T={0} C'.format(temp)

    ## PGA
    def update_pga(self, event):
        _label = event.GetEventObject().GetLabelText()
        ## fast buttons (Gain10, Gain16, Gain20, Gain26)
        if _label[0:4] == 'Gain':
            self.lj.set_gain(int(_label[4:]))
            self.read_pga()
        ## Spin Control Text (G = 6 - 26)
        if _label[0:8] == 'Set Gain':
            _setvalue = self.page1.lblname6w.GetValue()
            self.lj.set_gain(int(_setvalue))
            self.read_pga()
        event.Skip()

    def read_pga(self):
        self.__gain = float(self.lj.read_gain())
        self.page1.lblname6r.SetLabel(str(self.__gain))
        #print 'gain={0} dB'.format(gain)

    ## EEPROM
    def read_eeprom(self):
        for _page in range(8):
            _page = _page + 1
            _readout = self.lj.read_eeprom(_page)
            for _idx,_i in enumerate(_readout):
                if _i == 0xff:
                    _readout[_idx] = 32
            _array = [chr(_i) for _i in _readout]
            _string = ''.join(_array)
            if _page == 1:
                self.page3.mem1r.SetLabel(_string)
                self.page3.mem1w.SetValue(_string)
            elif _page == 2:
                self.page3.mem2r.SetLabel(_string)
            elif _page == 3:
                self.page3.mem3r.SetLabel(_string)
            elif _page == 4:
                self.page3.mem4r.SetLabel(_string)
            elif _page == 5:
                self.page3.mem5r.SetLabel(_string)
            elif _page == 6:
                self.page3.mem6r.SetLabel(_string)
            elif _page == 7:
                self.page3.mem7r.SetLabel(_string)
            elif _page == 8:
                self.page3.mem8r.SetLabel(_string)

    def update_eeprom(self, event):
        _label = event.GetEventObject().GetLabelText()
        if _label[0:8] == 'Set Page':
            _page = int(_label[8:])
            if _page == 1:
                _string = self.page3.mem1w.GetValue()
            elif _page == 2:
                _string = self.page3.mem2w.GetValue()
            elif _page == 3:
                _string = self.page3.mem3w.GetValue()
            elif _page == 4:
                _string = self.page3.mem4w.GetValue()
            elif _page == 5:
                _string = self.page3.mem5w.GetValue()
            elif _page == 6:
                _string = self.page3.mem6w.GetValue()
            elif _page == 7:
                _string = self.page3.mem7w.GetValue()
            elif _page == 8:
                _string = self.page3.mem8w.GetValue()

            ## Get the first 16 characters
            _string_list = list(_string[:16])
            _int_array = [ord(s) for s in _string_list]

            ## Add spaces if the length is smaller than 16
            while len(_int_array) < 16:
                _int_array.append(32)
            self.lj.write_eeprom(_page, _int_array)
            self.read_eeprom()
            self.page3.Layout()
            event.Skip()
        else:
            pass

    def read_serial(self):
        _readout = self.lj.read_eeprom(1)
        for _idx,_i in enumerate(_readout):
            if _i == 0xff:
                _readout[_idx] = 32
        _array = [chr(_i) for _i in _readout]
        _string = ''.join(_array)
        _array = _string.split(' ')
        # print _array
        if len(_array) == 3 and _array[0] == _array[2] and _array[1] == 'UWSiPM':
            self.page1.lblname4r.SetLabel(str(int(_array[0])))
            self.__serial = int(_array[0])
        else:
            self.page1.lblname4r.SetLabel('')
            self.__serial = 0

    def update_serial(self, event):
        _sn_string = self.page1.lblname4r.GetLabel()
        if _sn_string == '':
            _sn = self.page1.lblname4w.GetValue()
            _string = ('%04d UWSiPM %04d') % (_sn, _sn)
            _str_list = list(string)
            _int_array = [ord(_s) for _s in _str_list]
            #lj.write_eeprom(1, int_array)
            read_serial()
        elif int(_sn_string):
            self.page4.logger.AppendText('[{0}] SiPM# {1} found! Please don\'t alter it.\n'.format(self.get_time(), int(_sn_string)))

    def check_sipm_status(self):
        _sipm_status = self.__sipm_status
        if self.__temp > 50.0 or self.__gain > 25.0:
            # self.page4.logger.AppendText('[{0}] No SiPM found!\n'.format(self.get_time()))
            self.page1.lblname8r.SetLabel('NO')
            self.__sipm_status = False
            if _sipm_status == True:
                    self.page4.logger.AppendText('[{0}] A SiPM is being taken off!\n'.format(self.get_time()))


        elif self.__temp < 50.0 and self.__gain < 25.0:
            # self.page4.logger.AppendText('[{0}] SiPM found!\n'.format(self.get_time()))
            self.page1.lblname8r.SetLabel('YES')
            self.__sipm_status = True
            if _sipm_status == False:
                if self.__serial == 0:
                    self.page4.logger.AppendText('[{0}] A new SiPM is inserted!\n'.format(self.get_time()))
                else:
                    self.page4.logger.AppendText('[{0}] SiPM #{1} is inserted!\n'.format(self.get_time(), self.__serial))


    def refresh_lj(self):
        while True:
            wx.CallAfter(self.read_temp)
            wx.CallAfter(self.read_pga)
            wx.CallAfter(self.read_serial)
            wx.CallAfter(self.read_led)
            wx.CallAfter(self.check_sipm_status)
            wx.CallAfter(self.page1.Layout)
            time.sleep(2)
            #print 'V={0}, I={1}, T={2}, G={3}, SN={4}, STAT={5}'.format(self.__volt, self.__curr, self.__temp, self.__gain, self.__serial, self.__sipm_status)

    ## LED Board
    def update_led(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:3] == 'LED':
            self.lj.set_led(int(label[3:]))
        elif label[0:8] == 'Set LED#':
            setvalue = self.page1.lblname7w.GetValue()
            self.lj.set_led(setvalue)
        self.read_led()
        event.Skip()

    def read_led(self):
        self.__led_no = self.lj.read_led()
        self.page1.lblname7r.SetLabel(str(self.__led_no))

    def run_drs4(self, event):
        self.drs4_proc.stdin.write('{0:04d} {1} {2:02d} {3:05d}\n'.format(self.__serial,'led',self.__led_no,self.__seq_no))
        self.__seq_no  += 1
        self.dump_log()

    ## functions for Notebook
    def get_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    def dump_log(self):

        _log_dict = {
           'Datetime': self.get_time(),
           'Temperature': self.__temp,
           'Voltage': self.__volt,
           'Current': self.__curr,
           'Gain': self.__gain,
           'Serial_No': self.__serial,
           'Led_No': self.__led_no,
           'Sequence_No': self.__seq_no
        }

        json_outfile = open('./data/log/{0:04d}.txt'.format(self.__seq_no), 'w')
        json.dump(_log_dict, json_outfile, indent=4, sort_keys=True)


    def on_close(self, event):
        self.Close()

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
                #wx.CallAfter(self.page4.logger.AppendText, '[{0}] {1}\n'.format(self.get_time(), message))
                if message == "Exit":
                    #print "Received exit command, client will stop receiving messages"
                    should_continue = False


def main():
    app = wx.App()
    window = NoteBook(None)
    window.Layout()
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

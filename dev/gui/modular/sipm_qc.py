#!/usr/bin/python

# sipm_qc.py

## Import all needed libraries
import wx
import wx.lib.agw.flatnotebook as fnb
from threading import Thread, Event
from sipm_qc_gui import control_panel, display_panel, eeprom_panel, logger_panel
import time, sys, subprocess, os, threading, signal
from datetime import date, datetime, tzinfo, timedelta
import zmq
from multiprocessing import Process
import json

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

## Define the MainFrame
class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                title=wx.EmptyString,
                pos=wx.DefaultPosition,
                size=wx.Size(1300, 1000),
                style=wx.DEFAULT_FRAME_STYLE |
                wx.TAB_TRAVERSAL)

        def __del__(self):
            pass

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
        self.page1 = control_panel(self.nb)
        self.page2 = display_panel(self.nb)
        self.page3 = eeprom_panel(self.nb)
        self.page4 = logger_panel(self)

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

        # initialize for zmq
        drs4_port="5555"
        lj_port_push="5556"
        lj_port_pub="5566"
        bk_port_push="5557"
        bk_port_pub="5567"

        context = zmq.Context()

        self.socket_req_drs4 = context.socket(zmq.REQ)
        self.socket_req_drs4.connect("tcp://localhost:%s" % drs4_port)

        self.socket_push_bk = context.socket(zmq.PUSH)
        self.socket_push_bk.bind("tcp://*:%s" % bk_port_push)

        self.socket_push_lj = context.socket(zmq.PUSH)
        self.socket_push_lj.bind("tcp://*:%s" % lj_port_push)

        self.socket_sub_bk = context.socket(zmq.SUB)
        self.socket_sub_lj = context.socket(zmq.SUB)

        self.socket_sub_bk.connect("tcp://localhost:%s" % bk_port_pub)
        self.socket_sub_lj.connect("tcp://localhost:%s" % lj_port_pub)

        self.socket_sub_bk.setsockopt(zmq.SUBSCRIBE, "")
        self.socket_sub_lj.setsockopt(zmq.SUBSCRIBE, "")


        # define private variabls for status checking
        self.__volt=0.0
        self.__curr=0.0
        self.__state=0
        self.__temp=0.0
        self.__gain=0.0
        self.__eeprom1=''
        self.__eeprom2=''
        self.__eeprom3=''
        self.__eeprom4=''
        self.__eeprom5=''
        self.__eeprom6=''
        self.__eeprom7=''
        self.__eeprom8=''
        self.__serial=0
        self.__led_no=0
        self.__subrun_no=0
        self.__seq_no=0
        self.__count=0
        self.__type='none'
        self.__amp_avg=0.0
        self.__sipm_status=False
        self.__bk_status=False

        # initialize all the environment and do the layout
        self.init_thread()
        self.bind_bk()
        self.bind_led()
        self.bind_pga()
        self.bind_eeprom()
        self.bind_drs4()
        self.do_logger_binding()

        # redo layout realign all the variables
        self.page1.Layout()
        self.page2.Layout()
        self.page3.Layout()
        self.page4.Layout()
        ### end of __init__

    def init_thread(self):
        ## initialize thread for bk to refresh variables
        self.t1=Thread(target=self.refresh_bk)
        self.t1.daemon = True
        self.t1.start()

        ## initialize thread for labjack to refresh variables
        self.t2=Thread(target=self.refresh_lj)
        self.t2.daemon = True
        self.t2.start()

        ## initialize thread for constant logging
        self.t3=Thread(target=self.dump_log)
        self.t3.daemon = True
        self.t3.start()

    def msg_logger(self, msg):
        self.page4.logger.AppendText(msg)

    def bind_bk(self):
        ## bind the BK buttons to update the display and call bk.set_volt etc
        self.Bind(wx.EVT_BUTTON, self.update_bk_state, self.page1.lblname1s)
        self.Bind(wx.EVT_BUTTON, self.update_volt, self.page1.lblname2s)
        self.Bind(wx.EVT_BUTTON, self.update_curr, self.page1.lblname3s)

    def bind_led(self):
        ## bind the LED buttons to update the display and call labjack.set_led()
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led1)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led2)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led3)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led4)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led5)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led6)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led7)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led8)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led9)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led10)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led11)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led12)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led13)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led14)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led15)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led16)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.led16)
        self.Bind(wx.EVT_BUTTON, self.set_led, self.page1.lblname7s)

    def bind_pga(self):
        ## bind the PGA buttons to update the display and call labjack.update_gain()
        self.Bind(wx.EVT_BUTTON, self.set_gain, self.page1.button1)
        self.Bind(wx.EVT_BUTTON, self.set_gain, self.page1.button2)
        self.Bind(wx.EVT_BUTTON, self.set_gain, self.page1.button3)
        self.Bind(wx.EVT_BUTTON, self.set_gain, self.page1.button4)
        self.Bind(wx.EVT_BUTTON, self.set_gain, self.page1.lblname6s)

    def bind_eeprom(self):
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem1s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem2s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem3s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem4s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem5s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem6s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem7s)
        self.Bind(wx.EVT_BUTTON, self.set_eeprom, self.page3.mem8s)
        self.Bind(wx.EVT_BUTTON, self.set_serial, self.page1.lblname4s)

    def bind_drs4(self):
        self.Bind(wx.EVT_BUTTON, self.run_drs4, self.page1.drs4_button)
        self.Bind(wx.EVT_BUTTON, self.led_scan, self.page1.led_scan_button)
        self.Bind(wx.EVT_BUTTON, self.volt_scan, self.page1.volt_scan_button)

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
        self.msg_logger('[{0}] Clicked on {1}\n'.format(self.get_time(), labeltext))
        event.Skip()

    def on_spin(self, event):
        self.msg_logger(
                '[%s] %s to %.1f\n' % (self.get_time(), event.GetEventObject().GetName(),event.GetValue()))
        event.Skip()

    def on_switch(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.msg_logger('[{0}] Clicked on {1}\n'.format(self.get_time(), labeltext))
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

        self.msg_logger('[{0}] {1} to {2} {3}\n'.format(self.get_time(), labeltext, value, unit))
        event.Skip()

    #### define functions for BK Precision
    def send_to_bk(self, string):
        self.socket_push_bk.send(string)

    def send_to_lj(self, string):
        self.socket_push_lj.send(string)

    def read_from_bk(self):
        return self.socket_sub_bk.recv_json()

    def read_from_lj(self):
        return self.socket_sub_lj.recv_json()

    def send_to_drs4(self, string):
        self.socket_req_drs4.send(string)
        message = self.socket_req_drs4.recv()
        print("Received reply [%s]" % (message))

    def bk_on(self, event):
        self.send_to_bk("power on")
        self.page1.lblname2r.SetLabel('ON')
        event.Skip()

    def bk_off(self, event):
        self.send_to_bk("power off")
        self.page1.lblname2r.SetLabel('OFF')
        event.Skip()

    def update_bk_state(self, event):
        label = event.GetEventObject().GetLabelText()
        if label == 'Set ON':
            self.send_to_bk("power on")
        elif label == 'Set OFF':
            self.send_to_bk("power off")
        self.read_bk_state()
        event.Skip()

    def read_bk_state(self):
        state = self.__state
        if state == 1:
            self.page1.lblname1r.SetLabel('ON')
            self.page1.lblname1s.SetLabel('Set OFF')
        else:
            self.page1.lblname1r.SetLabel('OFF')
            self.page1.lblname1s.SetLabel('Set ON')

    def read_volt(self):
        volt = self.__volt
        self.page1.lblname2r.SetLabel('{:.2f}'.format(float(volt)))

    def update_volt(self, event):
        setvalue = self.page1.lblname2w.GetValue()
        self.send_to_bk('set volt {}'.format(setvalue))
        event.Skip()

    def read_curr(self):
        curr = self.__curr
        self.page1.lblname3r.SetLabel('{:.2f}'.format(float(curr)))

    def update_curr(self, event):
        setvalue = self.page1.lblname3w.GetValue()
        self.send_to_bk('set curr {}'.format(setvalue/1000.))
        event.Skip()

    def check_bk_status(self):
        bk_status = self.__bk_status
        if self.__volt < 0 and self.__curr < 0:
            self.page1.lblname9r.SetLabel('NO')
            self.__bk_status = False
            if bk_status == True:
                self.msg_logger('[{0}] BK Precision is powered off!\n'.format(self.get_time()))


        elif self.__volt > -1 and self.__curr > -1:
            self.page1.lblname9r.SetLabel('YES')
            self.__bk_status = True
            if bk_status == False:
                self.msg_logger('[{0}] BK Precision is powered on!\n'.format(self.get_time()))
                 #  self.read_bk_state()

    def refresh_bk(self):
        while True:
            json_data = self.read_from_bk()
            self.__volt = float(json_data["volt"])
            self.__curr = float(json_data["curr"])
            self.__state = int(json_data["state"])
            wx.CallAfter(self.read_volt)
            wx.CallAfter(self.read_curr)
            wx.CallAfter(self.read_bk_state)
            wx.CallAfter(self.check_bk_status)
            wx.CallAfter(self.page1.Layout)
            #print('{0}'.format(json_data))

    #### define functions for Labjack
    ## T-sensor
    def update_temp(self):
        temp = self.__temp
        self.page1.lblname5r.SetLabel(str(temp))
        self.page2.plot_temp('./data/log/slowctrl_{}.log'.format(self.get_day()))

    ## PGA
    def set_gain(self, event):
        label = event.GetEventObject().GetLabelText()

        ## fast buttons (Gain10, Gain16, Gain20, Gain26)
        if label[0:4] == 'Gain':
            self.send_to_lj('set gain {}'.format(int(label[4:])))

        ## Spin Control Text (G = 6 - 26)
        if label[0:8] == 'Set Gain':
            setvalue = self.page1.lblname6w.GetValue()
            self.send_to_lj('set gain {}'.format(int(setvalue)))
            event.Skip()

    def update_gain(self):
        gain = self.__gain
        self.page1.lblname6r.SetLabel(str(gain))

    ## EEPROM
    def update_eeprom(self):
        self.page3.mem1r.SetLabel(self.__eeprom1)
        self.page3.mem1w.SetValue(self.__eeprom1)
        self.page3.mem2r.SetLabel(self.__eeprom2)
        self.page3.mem3r.SetLabel(self.__eeprom3)
        self.page3.mem4r.SetLabel(self.__eeprom4)
        self.page3.mem5r.SetLabel(self.__eeprom5)
        self.page3.mem6r.SetLabel(self.__eeprom6)
        self.page3.mem7r.SetLabel(self.__eeprom7)
        self.page3.mem8r.SetLabel(self.__eeprom8)

    def set_eeprom(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:8] == 'Set Page':
            page = int(label[8:])
            if page == 1:
                string = self.page3.mem1w.GetValue()
            elif page == 2:
                string = self.page3.mem2w.GetValue()
            elif page == 3:
                string = self.page3.mem3w.GetValue()
            elif page == 4:
                string = self.page3.mem4w.GetValue()
            elif page == 5:
                string = self.page3.mem5w.GetValue()
            elif page == 6:
                string = self.page3.mem6w.GetValue()
            elif page == 7:
                string = self.page3.mem7w.GetValue()
            elif page == 8:
                string = self.page3.mem8w.GetValue()

            ## Get the first 16 characters
            string_list = list(string[:16])
            int_array = [ord(s) for s in string_list]

            ## Add spaces if the length is smaller than 16
            while len(int_array) < 16:
                int_array.append(32)

            self.send_to_lj('set eeprom {0} {1}'.format(page, string[:16]))
            event.Skip()

        else:
            pass

    def update_serial(self):
        serial = self.__serial
        if serial > 0:
            self.page1.lblname4r.SetLabel(str(serial))
        else:
            self.page1.lblname4r.SetLabel('')

    def set_serial(self, event):
        sn_string = self.page1.lblname4r.GetLabel()
        if sn_string == '':
            sn = self.page1.lblname4w.GetValue()
            string = ('%04d UWSiPM %04d') % (sn, sn)
            str_list = list(string)
            int_array = [ord(s) for s in str_list]
            self.send_to_lj('set eeprom {0} {1}'.format(page, int_array))
            update_serial()
        elif int(sn_string):
            self.msg_logger('[{0}] SiPM# {1} found! Please don\'t alter it.\n'.format(self.get_time(), int(sn_string)))
        event.Skip()


    def check_sipm_status(self):
        _sipm_status = self.__sipm_status
        if self.__temp > 50.0 and self.__gain == 26.0:
            self.msg_logger('[{0}] No SiPM found!\n'.format(self.get_time()))
            self.page1.lblname8r.SetLabel('NO')
            self.__sipm_status = False
            if _sipm_status == True:
                self.msg_logger('[{0}] SiPM #{1} is being taken off!\n'.format(self.get_time(), self.__serial))


        elif self.__temp < 50.0 and self.__gain < 26.1:
            self.page1.lblname8r.SetLabel('YES')
            self.__sipm_status = True
            if _sipm_status == False:
                if self.__serial == 0:
                    self.msg_logger('[{0}] A new SiPM is inserted!\n'.format(self.get_time()))
                else:
                    self.msg_logger('[{0}] SiPM #{1} is inserted!\n'.format(self.get_time(), self.__serial))


    def refresh_lj(self):
        while True:
            json_data = self.read_from_lj()
            self.__temp=float(json_data["temp"])
            self.__gain=float(json_data["gain"])
            self.__serial=int(json_data["serial"])
            self.__led_no=int(json_data["ledno"])
            self.__eeprom1=json_data["eeprom1"]
            self.__eeprom2=json_data["eeprom2"]
            self.__eeprom3=json_data["eeprom3"]
            self.__eeprom4=json_data["eeprom4"]
            self.__eeprom5=json_data["eeprom5"]
            self.__eeprom6=json_data["eeprom6"]
            self.__eeprom7=json_data["eeprom7"]
            self.__eeprom8=json_data["eeprom8"]
            wx.CallAfter(self.update_temp)
            wx.CallAfter(self.update_gain)
            wx.CallAfter(self.update_eeprom)
            wx.CallAfter(self.update_serial)
            wx.CallAfter(self.update_led)
            wx.CallAfter(self.check_sipm_status)
            wx.CallAfter(self.page1.Layout)
            wx.CallAfter(self.page3.Layout)
            #print('{0}'.format(json_data))

    ## LED Board
    def set_led(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:3] == 'LED':
            self.send_to_lj('set led {}'.format(int(label[3:])))
        elif label[0:8] == 'Set LED#':
            setvalue = self.page1.lblname7w.GetValue()
            self.send_to_lj('set led {}'.format(int(setvalue)))
        event.Skip()

    def update_led(self):
        self.__subrun_no = self.__led_no
        self.page1.lblname7r.SetLabel(str(self.__led_no))

    def run_drs4(self, event):
        ## decide runtype here from the pressed button label
        label = event.GetEventObject().GetLabelText()
        if label[0:7] == 'Run DRS':
            self.__type = 'test'
        elif label[0:7] == 'Run LED':
            self.__type = 'led'
        elif label[0:8] == 'Run Volt':
            self.__type = 'volt'
            self.__volt = 65.25 + 0.25 * self.__subrun_no

        ## initialize the gauge, increment the seq_no, send command to drs4
        self.page1.singlescan_gauge.SetValue(0)
        self.__seq_no += 1
        self.msg_logger('[{0}][Seq:{1}] Running SiPM with Bias = {2:.2f} V (and LED# {3})\n'.format(self.get_time(),self.__seq_no, self.__volt, self.__subrun_no))
        self.send_to_drs4('{0:04d} {1} {2:02d} {3:05d} '.format(self.__serial,self.__type,self.__subrun_no,self.__seq_no))
        self.dump_run_log(self.__volt,self.__subrun_no)
        self.page1.singlescan_gauge.SetValue(1)
        self.update_plot(self.__seq_no)
        event.Skip()

    def const_scan(self, event):
        self.__count = 1
        for _led_no in range (1, 100):
            print 'Start Scanning'
            self.__subrun_no = self.__count
            self.run_drs4(event)
            self.__count += 1
        event.Skip()

    def led_scan(self, event):
        for led_no in range (1, 17):
            self.__subrun_no = led_no
            self.send_to_lj('set led {}'.format(led_no))
            print 'Start LED Scan'
            self.page1.led_gauge.SetValue(led_no)
            self.run_drs4(event)
        event.Skip()

    def volt_scan(self, event):
        self.__count = 1
        for volt in frange (65.50, 69.50, 0.25):
            self.send_to_bk('set volt {}'.format(volt))
            self.__subrun_no = self.__count
            time.sleep(1)
            self.__volt == volt
            print 'Start Bias Scan'
            self.page1.volt_gauge.SetValue(self.__count)
            self.run_drs4(event)
            self.__count += 1
        self.send_to_bk("set volt 65")
        event.Skip()

    ## functions for Notebook
    def get_time(self):
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    def get_day(self):
        return datetime.strftime(datetime.now(), "%Y%m%d")

    def update_plot(self, seq_no):
        with open('./data/log/{0:05d}.txt'.format(seq_no),'r') as f:
            data = json.load(f)
        self.msg_logger('[{0}][Seq:{1}] Plotting SiPM#: {2}, Bias: {3:.2f}, LED#: {4}!\n'.format(self.get_time(), data["Sequence_No"],
            data["Serial_No"], data["Voltage"], data["Subrun_No"]))
        self.page1.plot_waveform('./data/sipm_{0:04d}/sipm_{0:04d}_{1}_{2:02d}_{3:05d}_full.txt'.format(data["Serial_No"],
            data["Type"], data["Subrun_No"], data["Sequence_No"]))
        self.page1.plot_amp_hist('./data/sipm_{0:04d}/sipm_{0:04d}_{1}_{2:02d}_{3:05d}.txt'.format(data["Serial_No"],data["Type"],data["Subrun_No"],data["Sequence_No"]))
        #result = self.page1.get_fit_result()
        #self.msg_logger('[{0}][Seq:{1}] Fit Results: Norm={2:.2f}, Mean={3:.2f}, Sig={4:.2f}\n'.format(self.get_time(), data["Sequence_No"],result[0], result[1], result[2]))
        self.__amp_avg = self.page1.get_amp_avg()
        self.msg_logger('[{0}][Seq:{1}] Scan Result: Amp={2:.2f}\n'.format(self.get_time(), data["Sequence_No"], self.__amp_avg))

    def dump_run_log(self, volt, subrun_no):

        _log_dict = {
                'Datetime': self.get_time(),
                'Temperature': self.__temp,
                'Voltage': volt,
                'Current': self.__curr,
                'Gain': self.__gain,
                'Serial_No': self.__serial,
                'Subrun_No': subrun_no,
                'Type': self.__type,
                'Sequence_No': self.__seq_no,
                'Amp_Avg': self.__amp_avg
                }

        json_outfile = open('./data/log/{0:05d}.txt'.format(self.__seq_no), 'w')
        json.dump(_log_dict, json_outfile, indent=4, sort_keys=True)

    def dump_log(self):

        while True:
            fdata = open('./data/log/slowctrl_{}.log'.format(self.get_day()), "a+")
            print >> fdata, self.get_time(), ' ', self.__temp, ' ', self.__volt, ' ', self.__curr, ' ', self.__gain, ' ', self.__serial, ' ', self.__subrun_no, ' ', self.__type, ' ', self.__seq_no
            time.sleep(5)


    def on_close(self, event):
        self.Close()
        self.Destroy()
        event.Skip()


def main():
    app = wx.App()
    window = NoteBook(None)
    window.Layout()
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

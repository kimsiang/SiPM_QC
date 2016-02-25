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

## Define the MainFrame
class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=wx.EmptyString,
                          pos=wx.DefaultPosition,
                          size=wx.Size(1450, 620),
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

        # initialize all the environment and do the layout
        self.init_daq()
        self.init_thread()
        self.bind_bk()
        self.bind_led()
        self.bind_pga()
        self.bind_eeprom()
        self.do_logger_binding()
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

        ## kill any running instances of drs_exam
        self.kill_drs4()

        ## initialize drs4
        self.run_drs4()
        self.page4.logger.AppendText('[{}] #####################\n'.format(self.get_time()))

        self.read_bk_state()
        self.read_volt()
        self.read_curr()
        self.read_temp()
        self.read_pga()
        self.read_eeprom()

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

    def do_logger_binding(self):
        # do all the logger bindings
        self.Bind(wx.EVT_BUTTON, self.on_click, self.page1.button)

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

    def kill_drs4(self):

        ## kill any instances of drs4_exam
        self.p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, shell=True)
        (out, err) = self.p.communicate()

        for line in out.splitlines():
            if 'drs_exam' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
        return True

    def run_drs4(self):
        ## logging drs_exam output
        fw = open("tmpout", "wb")
        fr = open("tmpout", "r")
        self.p = subprocess.Popen("/home/midas/KimWork/drs-5.0.3/drs_exam",
            stdin=subprocess.PIPE, stderr=fw,stdout=fw, bufsize=1)
        if self.p:
            self.page4.logger.AppendText('[{0}] # DRS4 initialized\n'.format(self.get_time()))
        return True

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
        state = self.bk.get_state()
        if state == '1':
            self.page1.lblname1r.SetLabel('ON')
            self.page1.lblname1s.SetLabel('Turn OFF')
        elif state == '0':
            self.page1.lblname1r.SetLabel('OFF')
            self.page1.lblname1s.SetLabel('Turn ON')

    def read_volt(self):
        volt = float(self.bk.meas_volt())
        self.page1.lblname2r.SetLabel('{:.2f}'.format(volt))
        #print 'V={0} V'.format(volt)

    def update_volt(self, event):
        setvalue = self.page1.lblname2w.GetValue()
        self.bk.set_volt(setvalue)
        wx.CallAfter(self.read_volt)
        event.Skip()

    def read_curr(self):
        curr = float(self.bk.meas_curr())*1000
        self.page1.lblname3r.SetLabel(str(curr))
        #print 'I={0} mA'.format(curr)

    def update_curr(self, event):
        setvalue = self.page1.lblname3w.GetValue()
        self.bk.set_curr(setvalue/1000.)
        wx.CallAfter(self.read_curr)
        event.Skip()

    def refresh_bk(self):
        while True:
            time.sleep(10)
            wx.CallAfter(self.read_volt)
            wx.CallAfter(self.read_curr)


    #### define functions for Labjack

    ## T-sensor
    def read_temp(self):
        temp = self.lj.read_temperature()
        #print 'T={0} C'.format(temp)
        #self.page4.logger.AppendText('[{0}] Temperature readout is {1}\n'.format(self.get_time(),temp))
        self.page1.lblname5r.SetLabel(str(temp))

    ## PGA
    def update_pga(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:4] == 'Gain':
            self.lj.set_gain(int(label[4:]))
            self.read_pga()
        if label[0:8] == 'Set Gain':
            setvalue = self.page1.lblname6w.GetValue()
            self.lj.set_gain(int(setvalue))
            self.read_pga()
        event.Skip()

    def read_pga(self):
        gain = self.lj.read_gain()
        #print 'gain={0} dB'.format(gain)
        self.page1.lblname6r.SetLabel(str(gain))
        #self.page4.logger.AppendText('[{0}] Gain readout is {1}\n'.format(self.get_time(), gain))

    ## EEPROM
    def read_eeprom(self):
        for page in range(8):
            page = page + 1
            readout = self.lj.read_eeprom(page)
            for idx,i in enumerate(readout):
                if i == 0xff:
                    readout[idx] = 32
            array = [chr(i) for i in readout]
            string = ''.join(array)
            if page == 1:
                self.page3.mem1r.SetLabel(string)
                self.page3.mem1w.SetValue(string)
                self.page1.lblname4r.SetLabel(self.check_serial(string))
            elif page == 2:
                self.page3.mem2r.SetLabel(string)
            elif page == 3:
                self.page3.mem3r.SetLabel(string)
            elif page == 4:
                self.page3.mem4r.SetLabel(string)
            elif page == 5:
                self.page3.mem5r.SetLabel(string)
            elif page == 6:
                self.page3.mem6r.SetLabel(string)
            elif page == 7:
                self.page3.mem7r.SetLabel(string)
            elif page == 8:
                self.page3.mem8r.SetLabel(string)

    def update_eeprom(self, event):
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
            #print string_list
            int_array = [ord(s) for s in string_list]
            #print int_array
            ## Add spaces if the length is smaller than 16
            while len(int_array) < 16:
                int_array.append(32)
            self.lj.write_eeprom(page, int_array)
            self.read_eeprom()
            self.page3.Layout()
            event.Skip()
        else:
            pass

    def check_serial(self, _string):
        array = _string.split(' ')
        print array
        if len(array) == 3 and array[0] == array[2] and array[1] == 'UWSiPM':
            self.page4.logger.AppendText('[{0}] SiPM# {1} found\n'.format(self.get_time(), int(array[0])))
            return str(int(array[0]))
        else:
            self.page4.logger.AppendText('[{0}] SiPM# not found. Please enter.\n'.format(self.get_time()))
            return '0'

    def refresh_lj(self):
        while True:
            time.sleep(2)
            wx.CallAfter(self.read_temp)
            wx.CallAfter(self.read_pga)


    ## LED Board
    def update_led(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:3] == 'LED':
            self.page1.lblname7r.SetLabel(label[3:])
            self.lj.set_led(int(label[3:]))
        if label[0:8] == 'Set LED#':
            setvalue = self.page1.lblname7w.GetValue()
            self.page1.lblname7r.SetLabel(str(setvalue))
        event.Skip()

    ## functions for Notebook

    def get_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

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
                #print "Received control command: %s" % message
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

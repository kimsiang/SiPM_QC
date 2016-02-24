#!/usr/bin/python

# sipm_qc.py

## Import all needed libraries
import wx
from bk_precision import BKPrecision
from labjack import labjack
from sipm_qc_gui import control_panel, display_panel, eeprom_panel, logger_panel
import time, sys, subprocess, os, threading, signal
from datetime import date, datetime, tzinfo, timedelta

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
        self.nb = wx.Notebook(self)

        # create the page windows as children of the notebook
        self.page1 = Panel1(self.nb)
        self.page2 = Panel2(self.nb)
        self.page3 = Panel3(self.nb)
        self.page4 = Panel4(self)

        # add the pages to the notebook with the label to show on the tab
        self.nb.AddPage(self.page1, "Control")
        self.nb.AddPage(self.page2, "Display")
        self.nb.AddPage(self.page3, "EEPROM")


        self.__init_timer()
        self.__init_daq()
        self.__bind_bk()
        self.__bind_led()
        self.__bind_pga()
        self.__bind_eeprom()
        self.__do_binding()
        self.__do_layout()

    def __init_timer(self):

        TIMER_ID = 100  # pick a number
        self.timer = wx.Timer(self, TIMER_ID)  # message will be sent to the panel
        self.timer.Start(5000)  # milliseconds
        wx.EVT_TIMER(self, TIMER_ID, self.on_timer)  # call the on_timer function

    def __init_daq(self):
        ## initialize BK precision
        self.page4.logger.AppendText("[%s] ### Start SiPM QC Station ###\n" % self.get_time())
        self.bk = BKPrecision('/dev/ttyUSB0')
        if self.bk:
            self.page4.logger.AppendText("[%s] # BK initialized\n" % self.get_time())

        ## initialize Labjack U3-LV
        self.lj = labjack()
        if self.lj:
            self.page4.logger.AppendText("[%s] # Labjack initialized\n" % self.get_time())

        ## kill any running instances of drs_exam
        self.kill_drs4()

        ## initialize drs4
        self.run_drs4()
        self.page4.logger.AppendText('[%s] #####################\n' % self.get_time())


    def __do_binding(self):

        # do all the event binding here
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button)

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.EvtSpinText, self.page1.lblname2w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.page1.lblname3w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.page1.lblname4w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.page1.lblname6w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.page1.lblname7w)

        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.page1.lblname1s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page1.lblname2s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page1.lblname3s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page1.lblname4s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page1.lblname6s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page1.lblname7s)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button1)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button2)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button3)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button4)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button5)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button6)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button7)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.button8)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led1)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led2)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led3)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led4)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led5)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led6)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led7)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led8)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led9)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led10)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led11)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led12)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led13)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led14)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led15)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.page1.led16)

        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem1s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem2s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem3s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem4s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem5s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem6s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem7s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.page3.mem8s)


    def get_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    def OnSwitch(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.page4.logger.AppendText("[%s] Clicked on %s\n" % (self.get_time(), labeltext))
        if labeltext == 'Turn ON':
            self.page1.lblname1r.SetLabel('ON')
            self.page1.lblname1s.SetLabel('Turn OFF')
        if labeltext == 'Turn OFF':
            self.page1.lblname1r.SetLabel('OFF')
            self.page1.lblname1s.SetLabel('Turn ON')
        event.Skip()

    def OnClick(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.page4.logger.AppendText("[%s] Clicked on %s\n" % (self.get_time(), labeltext))
        event.Skip()

    def OnSet(self, event):
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

    def EvtSpinText(self, event):
        self.page4.logger.AppendText(
                '[%s] %s to %.1f\n' % (self.get_time(), event.GetEventObject().GetName(),event.GetValue()))
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
            self.page4.logger.AppendText('[%s] # DRS4 initialized\n' % self.get_time())
        return True

    def __bind_bk(self):
        ## bind the BK buttons to update the display and call bk.set_volt etc
        self.Bind(wx.EVT_BUTTON, self.update_volt, self.page1.lblname2s)

    def __bind_led(self):
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

    def __bind_pga(self):
        ## bind the PGA buttons to update the display and call labjack.read_pga()
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button5)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button6)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button7)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.button8)
        self.Bind(wx.EVT_BUTTON, self.update_pga, self.page1.lblname6s)

    def __bind_eeprom(self):
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem1)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem2)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem3)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem4)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem5)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem6)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem7)
        self.Bind(wx.EVT_BUTTON, self.update_eeprom, self.page3.mem8)

    def update_led(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:3] == "LED":
            self.page1.lblname7r.SetLabel(label[3:])
            self.lj.set_led(int(label[3:]))
        if label[0:8] == "Set LED#":
            setvalue = self.page1.lblname7w.GetValue()
            self.page1.lblname7r.SetLabel(str(setvalue))

        event.Skip()

    def update_pga(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:4] == "Gain":
           # self.page1.lblname6r.SetLabel(label[4:])
            self.lj.set_gain(int(label[4:]))
            self.read_pga()
        if label[0:8] == "Set Gain":
            setvalue = self.page1.lblname6w.GetValue()
            self.lj.set_gain(int(setvalue))
            self.read_pga()
            #self.page1.lblname6r.SetLabel(str(setvalue))
        event.Skip()

    def update_eeprom(self, event):
        er_array = lj.read_eeprom(1)
        event.Skip()

    def read_pga(self):
        gain = self.lj.read_gain()
        self.page1.lblname6r.SetLabel(str(gain))
        self.page4.logger.AppendText('[{0}] Gain readout is {1}\n'.format(self.get_time(), gain))

    def read_temp(self):
        temp = self.lj.read_temperature()
        #self.page4.logger.AppendText('[{0}] Temperature readout is {1}\n'.format(self.get_time(),temp))
        self.page1.lblname5r.SetLabel(str(temp))

    def read_volt(self):
        volt = self.bk.meas_volt()
        self.page1.lblname2r.SetLabel(str(volt))

    def update_volt(self, event):
        setvalue = self.page1.lblname2w.GetValue()
        print setvalue
        self.bk.set_volt(setvalue)

    def __do_layout(self):
        # finally, put the notebook in a sizer for the panel to manage the layout
        grid = wx.GridBagSizer(hgap=10, vgap=10)

        # start of grid
        grid.Add(self.nb, pos=(0, 0), span=(1,2), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.page4, pos=(0, 2), flag=wx.TE_RIGHT)
        self.SetSizerAndFit(grid)

    def on_timer(self, event):
#       self.page4.logger.AppendText('[{0}]\n'.format(self.get_time()))
        self.read_temp()
        self.read_volt()

    def on_close(self, event):
        self.timer.Stop()
        self.Destroy()


#   def update_bk_status(self, event):
        # bk off
#       global v_setpoint
#        v_setpoint = float(bk.meas_volt()[:4])
#        print "Saving V_setpoint ...... V_setpoint = %f" % v_setpoint
#        bk.set_volt(0.0)
#        bk.power_off()
#        bk.set_curr(0.005)
#        time.sleep(2)
#	self.display1.Clear()
#        self.display1.AppendText(bk.meas_volt())
#        self.display1.SetBackgroundColour("red")
#        self.label1.SetBackgroundColour("red")
        ## bk on
#        bk.power_on()
#       print "Current V_setpoint ...... V_setpoint = %f" % v_setpoint
#        bk.set_volt(v_setpoint)
#        time.sleep(2)
#        print "Current HV: %f ......" % float(bk.meas_volt())
#        self.SetGain1(self)
#        self.ReadGain(self)
#        self.ReadTemp(self)
#        self.display1.Clear()
#        self.display1.AppendText(bk.meas_volt())
#        self.display1.SetBackgroundColour("green")
#        self.label1.SetBackgroundColour("green")

#        if float(self.display1.GetValue()) > -0.01 and float(self.display1.GetValue()) < 70.01:
#            bk.set_volt(float(self.display1.GetValue()))
#            time.sleep(2)
#            self.display1.Clear()
#            self.display1.AppendText(bk.meas_volt())


def main():
    app = wx.App()
    window = NoteBook(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

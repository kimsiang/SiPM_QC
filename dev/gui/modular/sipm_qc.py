#!/usr/bin/python

# sipm_qc.py

## Import all needed libraries
import wx
from bk_precision import BKPrecision
from labjack import labjack
from sipm_qc_gui import control_panel, display_panel, eeprom_panel
import time, sys, subprocess, os, threading, signal

## Define the MainFrame
class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=wx.EmptyString,
                          pos=wx.DefaultPosition,
                          size=wx.Size(1350, 700),
                          style=wx.DEFAULT_FRAME_STYLE |
                          wx.TAB_TRAVERSAL)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

class Panel1(control_panel):

    def __init__(self, parent):
        control_panel.__init__(self, parent)
        self.parent = parent
        #self.parent.SetTitle("SiPM QC Station - L0 - Control Panel")
        self.SetBackgroundColour('silver')

    def changeIntroPanel(self, event):
        if self.IsShown():
            label = event.GetEventObject().GetLabelText()
        #    self.parent.SetTitle("SiPM QC Station - L0 (%s)" % label)
            self.Hide()
            if label == 'Display Panel':
                self.parent.panelTwo.Show()
            if label == 'EEPROM Panel':
                self.parent.panelThree.Show()


class Panel2(display_panel):

    def __init__(self, parent):
        display_panel.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel(self, event):
        if self.IsShown():
            label = event.GetEventObject().GetLabelText()
       #     self.parent.SetTitle("SiPM QC Station - L0 (%s)" % label)
            self.Hide()
            if label == 'Control Panel':
                self.parent.panelOne.Show()
            if label == 'EEPROM Panel':
                self.parent.panelThree.Show()

class Panel3(eeprom_panel):

    def __init__(self, parent):
        eeprom_panel.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel(self, event):
        if self.IsShown():
            label = event.GetEventObject().GetLabelText()
      #      self.parent.SetTitle("SiPM QC Station - L0 (%s)" % label)
            self.Hide()
            if label == 'Control Panel':
                self.parent.panelOne.Show()
            if label == 'Display Panel':
                self.parent.panelTwo.Show()

class NoteBook(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page1 = Panel1(nb)
        page2 = Panel2(nb)
        page3 = Panel3(nb)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Page 1")
        nb.AddPage(page2, "Page 2")
        nb.AddPage(page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

## Define the MainApp
class MainApp(MainFrame):

    def __init__(self, parent):
        MainFrame.__init__(self, parent)


        self.panelOne = Panel1(self)
        self.panelTwo = Panel2(self)
        self.panelThree = Panel3(self)
        self.panelTwo.Hide()
        self.panelThree.Hide()

        ## initialize BK precision
        self.panelOne.logger.AppendText("[%s] ### Start SiPM QC Station ###\n" % self.panelOne.get_time())
        self.bk = BKPrecision('/dev/ttyUSB0')
        if self.bk:
            self.panelOne.logger.AppendText("[%s] # BK initialized\n" % self.panelOne.get_time())

        ## initialize Labjack U3-LV
        self.lj = labjack()
        if self.lj:
            self.panelOne.logger.AppendText("[%s] # Labjack initialized\n" % self.panelOne.get_time())

        ## kill any running instances of drs_exam
        self.kill_drs4()

        ## initialize drs4
        self.run_drs4()
        self.panelOne.logger.AppendText('[%s] #####################\n' % self.panelOne.get_time())

        ## do the binding here
        self.__bind_led()
        self.__bind_pga()

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
            self.panelOne.logger.AppendText('[%s] # DRS4 initialized\n' % self.panelOne.get_time())
        return True

    def __bind_led(self):

        ## bind the LED buttons to update the display and call labjack.set_led()
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led1)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led2)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led3)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led4)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led5)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led6)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led7)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led8)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led9)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led10)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led11)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led12)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led13)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led14)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led15)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led16)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.led16)
        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.lblname7s)

    def __bind_pga(self):
        self.Bind(wx.EVT_BUTTON, self.update_pga_value, self.panelOne.button5)
        self.Bind(wx.EVT_BUTTON, self.update_pga_value, self.panelOne.button6)
        self.Bind(wx.EVT_BUTTON, self.update_pga_value, self.panelOne.button7)
        self.Bind(wx.EVT_BUTTON, self.update_pga_value, self.panelOne.button8)
        self.Bind(wx.EVT_BUTTON, self.update_pga_value, self.panelOne.lblname6s)


    def __bind_eeprom(self):
        self.Bind(wx.EVT_BUTTON, self.update_eeprom_value, id=11)

#    def __bind_bk(self):
#        ## bind the BK buttons to update the display and call bk.set_volt etc
#        self.Bind(wx.EVT_BUTTON, self.update_led_value, self.panelOne.button1)

    def update_led_value(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:3] == "LED":
            self.panelOne.lblname7r.SetLabel(label[3:])
            self.lj.set_led(int(label[3:]))
        if label[0:8] == "Set LED#":
            setvalue = self.panelOne.lblname7w.GetValue()
            self.panelOne.lblname7r.SetLabel(str(setvalue))

    def update_pga_value(self, event):
        label = event.GetEventObject().GetLabelText()
        if label[0:4] == "Gain":
            self.panelOne.lblname6r.SetLabel(label[4:])
            self.lj.set_gain(int(label[4:]))
        if label[0:8] == "Set Gain":
            setvalue = self.panelOne.lblname6w.GetValue()
            self.panelOne.lblname6r.SetLabel(str(setvalue))

    def update_eeprom_value(self, event):
        er_array = lj.read_eeprom(1)


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

#    def update_bk_value(self, event):
#        if float(self.display1.GetValue()) > -0.01 and float(self.display1.GetValue()) < 70.01:
#            bk.set_volt(float(self.display1.GetValue()))
#            time.sleep(2)
#            self.display1.Clear()
#            self.display1.AppendText(bk.meas_volt())


def main():
    app = wx.App()
    #window = MainApp(None)
    window = NoteBook(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

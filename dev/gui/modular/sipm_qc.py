#!/usr/bin/python

# sipm_qc.py

## Import all needed libraries
import wx
from bk_precision import BKPrecision
from labjack import labjack
from sipm_qc_gui import control_panel, display_panel, eeprom_panel, logger_panel
import time, sys, subprocess, os, threading, signal

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

class Panel4(logger_panel):

    def __init__(self, parent):
        logger_panel.__init__(self, parent)
        self.parent = parent

class NoteBook(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        self.page1 = Panel1(nb)
        self.page2 = Panel2(nb)
        self.page3 = Panel3(nb)
        self.page4 = Panel4(p)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.page1, "Control")
        nb.AddPage(self.page2, "Display")
        nb.AddPage(self.page3, "EEPROM")

        self.__do_binding()

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

    def get_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    def EvtRadioBox(self, event):
        self.page4.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
        event.Skip()

    def get_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    def EvtRadioBox(self, event):
        self.page4.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
        event.Skip()

    def EvtComboBox(self, event):
        self.page4.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
        event.Skip()

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
        if labeltext == 'Set V':
            value = self.page1.lblname2w.GetValue()
            unit = 'V'
        elif labeltext == 'Set I':
            value = self.page1.lblname3w.GetValue()
            unit = 'mA'
        elif labeltext == 'Set SiPM#':
            value = self.page1.lblname4w.GetValue()
            unit = ''
        elif labeltext == 'Set Gain':
            value = self.page1.lblname6w.GetValue()
            unit = 'dB'
        elif labeltext == 'Set LED#':
            value = self.page1.lblname7w.GetValue()
            unit = ''
        self.page4.logger.AppendText("[%s] %s to %.1f %s\n" % (self.get_time(), labeltext, value, unit))
        event.Skip()

    def EvtText(self, event):
        self.page4.logger.AppendText('EvtText: %s\n' % event.GetString())
        event.Skip()

    def EvtChar(self, event):
        self.page4.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def EvtCheckBox(self, event):
        self.page4.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
        event.Skip()

    def EvtSpinText(self, event):
        self.page4.logger.AppendText(
                '[%s] %s to %.1f\n' % (self.get_time(), event.GetEventObject().GetName(),event.GetValue()))
        event.Skip()


        # finally, put the notebook in a sizer for the panel to manage the layout
#        sizer = wx.BoxSizer(wx.HORIZONTAL)

        grid = wx.GridBagSizer(hgap=10, vgap=10)

        # start of grid
        grid.Add(nb, pos=(0, 0), span=(1,2), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(logger, pos=(0, 2), flag=wx.TE_RIGHT)

        #sizer.Add(nb, 1, wx.EXPAND)
#        sizer.Add(nb, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)
#        sizer.Add(logger, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)
#        p.SetSizerAndFit(sizer)
        p.SetSizerAndFit(grid)



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
#        self.panelOne.logger.AppendText("[%s] ### Start SiPM QC Station ###\n" % self.panelOne.get_time())
        self.bk = BKPrecision('/dev/ttyUSB0')
#        if self.bk:
#            self.panelOne.logger.AppendText("[%s] # BK initialized\n" % self.panelOne.get_time())

        ## initialize Labjack U3-LV
        self.lj = labjack()
 #       if self.lj:
 #           self.panelOne.logger.AppendText("[%s] # Labjack initialized\n" % self.panelOne.get_time())

        ## kill any running instances of drs_exam
        self.kill_drs4()

        ## initialize drs4
        self.run_drs4()
  #      self.panelOne.logger.AppendText('[%s] #####################\n' % self.panelOne.get_time())

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
 #       if self.p:
#            self.panelOne.logger.AppendText('[%s] # DRS4 initialized\n' % self.panelOne.get_time())
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

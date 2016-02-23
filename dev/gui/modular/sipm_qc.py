#!/usr/bin/python

# sipm_qc.py

## Import all needed libraries
import wx
from bk_precision import BKPrecision
from labjack import labjack
from sipm_qc_gui import control_panel, display_panel
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

        #self.panelOne = ControlPanel(self)
        #self.panelTwo = DisplayPanel(self)
        # self.panelTwo.Hide()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass

class Panel1(control_panel):

    def __init__(self, parent):
        control_panel.__init__(self, parent)
        self.parent = parent
        self.parent.SetTitle("SiPM QC Station - L0 (Control Panel)")
        self.SetBackgroundColour('silver')
        self.__do_daq_binding()

    def changeIntroPanel(self, event):
        if self.IsShown():
            self.parent.SetTitle("SiPM QC Station - L0 (Display Panel)")
            self.Hide()
            self.parent.panelTwo.Show()

    def __do_daq_binding(self):
        self.button1.SetLabel('102')

class Panel2(display_panel):

    def __init__(self, parent):
        display_panel.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel(self, event):
        if self.IsShown():
            self.parent.SetTitle("SiPM QC Station - L0 (Control Panel)")
            self.parent.panelOne.Show()
            self.Hide()

## Define the MainApp
class MainApp(MainFrame):

    def __init__(self, parent):
        MainFrame.__init__(self, parent)

        self.panelOne = Panel1(self)
        self.panelTwo = Panel2(self)
        self.panelTwo.Hide()

        print '##########################################################'
        self.bk = BKPrecision('/dev/ttyUSB0')
        self.lj = labjack()

        ## kill any running instances of drs_exam
        self.kill_drs4()
        self.run_drs4()
        print '##########################################################'

    def kill_drs4(self):
        self.p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, shell=True)
        (out, err) = self.p.communicate()

        ## Kill any instances of drs4_exam
        for line in out.splitlines():
            if 'drs_exam' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)


    def run_drs4(self):
        ## logging drs_exam output
        fw = open("tmpout", "wb")
        fr = open("tmpout", "r")
        self.p = subprocess.Popen("/home/midas/KimWork/drs-5.0.3/drs_exam",
            stdin=subprocess.PIPE, stderr=fw,stdout=fw, bufsize=1)
        if self.p:
            print '>>> DRS4 running alright!'


def main():
    app = wx.App()
    window = MainApp(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

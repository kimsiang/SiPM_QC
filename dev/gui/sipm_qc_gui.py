#!/usr/bin/python

# sipm_qc_gui.py

## Import serial for BK precision voltage control
import serial
ser1 = serial.Serial('/dev/ttyUSB0', 4800,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,timeout=1.0)
print ser1

## Import serial and labjack for I/O
from labjack import labjack
lj = labjack()


## Import wx, wxversion for GUI
import wx
#import wxversion
#wxversion.select("2.8")

## Import system process for process handling
import time, sys, subprocess, os, threading, signal
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
(out, err) = p.communicate()

## Kill any instances of drs4_exam
for line in out.splitlines():
    if 'drs_exam' in line:
        pid = int(line.split(None, 1)[0])
        os.kill(pid, signal.SIGKILL)

## logging drs_exam output
fw = open("tmpout", "wb")
fr = open("tmpout", "r")
p = subprocess.Popen("/home/midas/KimWork/drs-5.0.3/drs_exam",
    stdin=subprocess.PIPE, stderr=fw,stdout=fw, bufsize=1)

## initiaize SiPM #
sipm_no = 0

## Import time classes
from datetime import date,datetime,tzinfo,timedelta
from decimal import Decimal

## Import tools for fast plotting
from numpy import arange, sin, pi
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal
gaussian_numbers = normal(size=1000)
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


print 'Initializing SiPM QC (L0) Station Control Panel ......'

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):

        ## Add frame
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition,
                wx.Size(600, 800))
        self.formula = False

        #Panel for frame
        self.panel = wx.Panel(self)
        self.SetBackgroundColour('gray')

        ## Add menu bar
        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(22, '&Quit', 'Exit Panel Control')
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        wx.EVT_MENU(self, 22, self.OnClose)

        ## Add box
        sizer = wx.BoxSizer(wx.VERTICAL)

        ## Add figure
        self.figure1 = plt.figure(1, dpi=60)
        self.axes1 = self.figure1.add_subplot(111)
        self.canvas1 = FigureCanvas(self, -1, self.figure1)
        self.figure2 = plt.figure(2, dpi=60)
        self.axes2 = self.figure2.add_subplot(111)
        self.canvas2 = FigureCanvas(self, -1, self.figure2)

        ## Add display boxes
        self.label1 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label2 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label3 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label4 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label5 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label6 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label7 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))
        self.label8 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,40))

        self.display1 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display2 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display3 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display4 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display5 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display6 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display7 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))
        self.display8 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,40))

        ## Set font style and size for the text in the display box
        font1 = wx.Font(18, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.label1.SetFont(font1)
        self.label2.SetFont(font1)
        self.label3.SetFont(font1)
        self.label4.SetFont(font1)
        self.label5.SetFont(font1)
        self.label6.SetFont(font1)
        self.label7.SetFont(font1)
        self.label8.SetFont(font1)

        self.display1.SetFont(font1)
        self.display2.SetFont(font1)
        self.display3.SetFont(font1)
        self.display4.SetFont(font1)
        self.display5.SetFont(font1)
        self.display6.SetFont(font1)
        self.display7.SetFont(font1)
        self.display8.SetFont(font1)

        ## Set Label names
        self.label1.AppendText(' BK [V] ')
        self.label2.AppendText(' Gain [dB]')
        self.label3.AppendText(' T [' + u'\u2103] ')
        self.label4.AppendText(' SiPM # ')
        self.display4.AppendText('0')
        self.label5.AppendText(' LED # ')
        self.label6.AppendText(' V_amp [mV] ')
        self.label7.AppendText(' EEPROM [Write]')
        self.label8.AppendText(' EEPROM [Read]')

        gsdisplay = wx.GridSizer(8, 2, 5, 5)
        gsdisplay.AddMany([
            (self.label1, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display1, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label2, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display2, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label3, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display3, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label4, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display4, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label5, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display5, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label6, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display6, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label7, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display7, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.label8, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display8, 0, wx.CENTER | wx.TOP | wx.BOTTOM)])

        ## Create "Telephone" grid for controlling BK precision, temperature
        ## measurement, EEPROM R/W and LEDs
        gsbutton = wx.GridSizer(5, 4, 10, 10)
        gsbutton.AddMany([
                        (wx.Button(self, 24, 'Temp', size=(80,50)), 0, wx.EXPAND),
                        (wx.Button(self, 17, 'BK OFF'), 0, wx.EXPAND),
                        (wx.Button(self, 18, 'BK ON'), 0, wx.EXPAND),
                        (wx.Button(self, 19, 'Close'), 0, wx.EXPAND),
                        (wx.Button(self, 1, '1'), 0, wx.EXPAND),
                        (wx.Button(self, 2, '2'), 0, wx.EXPAND),
                        (wx.Button(self, 3, '3'), 0, wx.EXPAND),
                        (wx.Button(self, 4, '4'), 0, wx.EXPAND),
                        (wx.Button(self, 5, '5'), 0, wx.EXPAND),
                        (wx.Button(self, 6, '6'), 0, wx.EXPAND),
                        (wx.Button(self, 7, '7'), 0, wx.EXPAND),
                        (wx.Button(self, 8, '8'), 0, wx.EXPAND),
                        (wx.Button(self, 9, '9'), 0, wx.EXPAND),
                        (wx.Button(self, 10, '10'), 0, wx.EXPAND),
                        (wx.Button(self, 11, '11'), 0, wx.EXPAND),
                        (wx.Button(self, 12, '12'), 0, wx.EXPAND),
                        (wx.Button(self, 13, '13'), 0, wx.EXPAND),
                        (wx.Button(self, 14, '14'), 0, wx.EXPAND),
                        (wx.Button(self, 15, '15'), 0, wx.EXPAND),
                        (wx.Button(self, 16, '16'), 0, wx.EXPAND),
                        (wx.Button(self, 20, 'L = 10 dB'), 0, wx.EXPAND),
                        (wx.Button(self, 21, 'L = 16 dB'), 0, wx.EXPAND),
                        (wx.Button(self, 22, 'L = 20 dB'), 0, wx.EXPAND),
                        (wx.Button(self, 23, 'ALL'), 0, wx.EXPAND)
                        ])

        gs = wx.GridSizer(2,2,5,5)
        gs.AddMany([(self.canvas1, 0, wx.EXPAND),(self.canvas2, 0,
            wx.EXPAND), (gsdisplay, 1, wx.ALIGN_CENTER),(gsbutton, 1, wx.ALIGN_CENTER)])

        sizer.Add(gs, 1, wx.ALIGN_CENTER)

        self.SetSizer(sizer)
        self.Centre()

        self.SetSizerAndFit(sizer)
    def OnClose(self, event):
        self.Close()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'SiPM QC Station Control Panel')
        frame.Show(True)
        frame.display4.SetBackgroundColour("red")
        frame.label4.SetBackgroundColour("red")
        self.SetTopWindow(frame)
        return True

# ----- Main program -------

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

#!/usr/bin/python3.3

# LED.py

import serial
import gpib
from labjack import labjack
lj = labjack()

spi_conf_temp = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 14,
	"CLKPinNum": 15,
	"MISOPinNum": 17,
	"MOSIPinNum": 16
	}

spi_conf_pga = {
	"AutoCS": True,
	"DisableDirConfig": False,
	"SPIMode": 'C',
	"SPIClockFactor": 0,
	"CSPINNum": 18,
	"CLKPinNum": 15,
	"MISOPinNum": 19,
	"MOSIPinNum": 16
}

import wxversion
wxversion.select("2.8")
import wx

import time, sys, subprocess, os, threading, signal
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
(out, err) = p.communicate()

for line in out.splitlines():
    if 'drs_exam' in line:
        pid = int(line.split(None, 1)[0])
        os.kill(pid, signal.SIGKILL)

fw = open("tmpout", "wb")
fr = open("tmpout", "r")
p = subprocess.Popen("/home/midas/KimWork/drs-5.0.3/drs_exam",
    stdin=subprocess.PIPE, stderr=fw,stdout=fw, bufsize=1)
p.stdin.write("2000\n")
#out = fr.read()
#(output, err) = p.communicate()
#print output

from datetime import date,datetime,tzinfo,timedelta
from decimal import Decimal

from numpy import arange, sin, pi
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal
gaussian_numbers = normal(size=1000)
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure



print 'Initializing SiPM QC Station Control Panel ......'

ser1 = serial.Serial('/dev/ttyUSB0', 4800,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,timeout=1.0)
print ser1

#d = u3.U3 ()
#d = u3.U3 (debug=True)

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
        #self.figure = Figure(None, dpi=40)
        self.figure1 = plt.figure(1, dpi=60)
        self.axes1 = self.figure1.add_subplot(111)
        self.canvas1 = FigureCanvas(self, -1, self.figure1)
        self.figure2 = plt.figure(2, dpi=60)
        self.axes2 = self.figure2.add_subplot(111)
        self.canvas2 = FigureCanvas(self, -1, self.figure2)

       ## Add display boxes
        self.display1 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(350,50))
        self.display2 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(350,50))
        self.display3 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(350,50))
        self.display4 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(350,50))
        self.display5 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(350,50))

        ## Set font style and size for the text in the display box
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.display1.SetFont(font1)
        self.display2.SetFont(font1)
        self.display3.SetFont(font1)
        self.display4.SetFont(font1)
        self.display5.SetFont(font1)


        gsdisplay = wx.GridSizer(5, 1, 5, 5)
        gsdisplay.AddMany([(self.display1, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display2, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display3, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display4, 0, wx.CENTER | wx.TOP | wx.BOTTOM),
            (self.display5, 0, wx.CENTER | wx.TOP | wx.BOTTOM)])


        gsbutton = wx.GridSizer(5, 4, 10, 10)
        gsbutton.AddMany([
                        (wx.Button(self, 24, 'Temp'), 0, wx.EXPAND),
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
                        (wx.Button(self, 20, 'Gain 50'), 0, wx.EXPAND),
                        (wx.Button(self, 21, 'Gain 60'), 0, wx.EXPAND),
                        (wx.Button(self, 22, 'Gain 80'), 0, wx.EXPAND),
                        (wx.Button(self, 23, 'ALL'), 0, wx.EXPAND)
                        ])

        gs = wx.GridSizer(2,2,5,5)
        gs.AddMany([(self.canvas1, 0, wx.EXPAND),(self.canvas2, 0,
            wx.EXPAND), (gsdisplay, 1, wx.ALIGN_CENTER),(gsbutton, 1, wx.ALIGN_CENTER)])

        sizer.Add(gs, 1, wx.ALIGN_CENTER)

        self.SetSizer(sizer)
        self.Centre()

        self.Bind(wx.EVT_BUTTON, self.Led1, id=1)
        self.Bind(wx.EVT_BUTTON, self.Led2, id=2)
        self.Bind(wx.EVT_BUTTON, self.Led3, id=3)
        self.Bind(wx.EVT_BUTTON, self.Led4, id=4)
        self.Bind(wx.EVT_BUTTON, self.Led5, id=5)
        self.Bind(wx.EVT_BUTTON, self.Led6, id=6)
        self.Bind(wx.EVT_BUTTON, self.Led7, id=7)
        self.Bind(wx.EVT_BUTTON, self.Led8, id=8)
        self.Bind(wx.EVT_BUTTON, self.Led9, id=9)
        self.Bind(wx.EVT_BUTTON, self.Led10, id=10)
        self.Bind(wx.EVT_BUTTON, self.Led11, id=11)
        self.Bind(wx.EVT_BUTTON, self.Led12, id=12)
        self.Bind(wx.EVT_BUTTON, self.Led13, id=13)
        self.Bind(wx.EVT_BUTTON, self.Led14, id=14)
        self.Bind(wx.EVT_BUTTON, self.Led15, id=15)
        self.Bind(wx.EVT_BUTTON, self.Led16, id=16)
        self.Bind(wx.EVT_BUTTON, self.BKoff, id=17)
        self.Bind(wx.EVT_BUTTON, self.BKon, id=18)
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=19)
        self.Bind(wx.EVT_BUTTON, self.Gain50, id=20)
        self.Bind(wx.EVT_BUTTON, self.Gain60, id=21)
        self.Bind(wx.EVT_BUTTON, self.Gain80, id=22)
        self.Bind(wx.EVT_BUTTON, self.ReadTemp, id=24)
        self.Bind(wx.EVT_BUTTON, self.Led16, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led15, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led14, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led13, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led12, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led11, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led10, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led9, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led8, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led7, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led6, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led5, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led4, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led3, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led2, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led1, id=23)
        self.SetSizerAndFit(sizer)

#    def draw(self):
#        print 'draw ......'
#        t = arange(0.0, 3.0, 0.01)
#        s = sin(2 * pi * t)
#        self.axes.plot(t, s)
#        self.canvas.draw()

    def BKoff(self, event):
        ser1.write('OUTPUT OFF\n')
        ser1.write('SOUR:CURR 3mA\n')
        ser1.write('SOUR:VOLT 67.5V\n')
        time.sleep(1.0)
	ser1.write('MEAS:VOLT?\n')
	cur=ser1.read(64)
	self.display1.Clear()
        self.display1.AppendText('BK OFF: ')
        time.sleep(1)
        self.display1.AppendText(str(cur.split('\n',1)[0]))
        self.display1.AppendText(' V ')
        self.display1.SetBackgroundColour("red")

    def BKon(self, event):
        ser1.write('OUTPUT ON\n')
        time.sleep(1.0)
        ser1.write('MEAS:VOLT?\n')
	cur=ser1.read(64)
	self.display1.Clear()
        self.display1.AppendText('BK ON: ')
        self.display1.AppendText(str(cur.split('\n',1)[0]))
        self.display1.AppendText(' V ')
        self.display1.SetBackgroundColour("green")

    def Led1(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #1')
        self.calldrs4(1)
        self.callplotter(1)
        event.Skip()

    def Led2(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #2')
        self.calldrs4(2)
        self.callplotter(2)
        event.Skip()

    def Led3(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #3')
        self.calldrs4(3)
        self.callplotter(3)
        event.Skip()

    def Led4(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #4')
        self.calldrs4(4)
        self.callplotter(4)
        event.Skip()

    def Led5(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #5')
        self.calldrs4(5)
        self.callplotter(5)
        event.Skip()

    def Led6(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #6')
        self.calldrs4(6)
        self.callplotter(6)
        event.Skip()

    def Led7(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #7')
        self.calldrs4(7)
        self.callplotter(7)
        event.Skip()

    def Led8(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #8')
        self.calldrs4(8)
        self.callplotter(8)
        event.Skip()

    def Led9(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #9')
        self.calldrs4(9)
        self.callplotter(9)
        event.Skip()

    def Led10(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #10')
        self.calldrs4(10)
        self.callplotter(10)
        event.Skip()

    def Led11(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #11')
        self.calldrs4(11)
        self.callplotter(11)
        event.Skip()

    def Led12(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #12')
        self.calldrs4(12)
        self.callplotter(12)
        self.Update()
        event.Skip()

    def Led13(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #13')
        self.calldrs4(13)
        self.callplotter(13)
        event.Skip()

    def Led14(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #14')
        self.calldrs4(14)
        self.callplotter(14)
        event.Skip()

    def Led15(self, event):
	self.display4.Clear()
        self.display4.AppendText('LED #15')
        self.calldrs4(15)
        self.callplotter(15)
        event.Skip()

    def Led16(self, event):
        self.display4.Clear()
        self.display4.AppendText('LED #16')
        self.calldrs4(16)
        self.callplotter(16)
        event.Skip()

    def calldrs4(self, ledno):
        p.stdin.write("%d\n" % ledno)

    def callplotter(self, ledno):
        total = 0.0
        length = 0.0
        average = 0.0
        #Open the file
        while not os.path.isfile("./data/sipm_2000_%d.txt" % ledno):
            time.sleep(1)

        while True:
            infile = open("./data/sipm_2000_%d.txt" % ledno, 'r')
            for line in infile:
                amount = float(line)
                total += amount
                length = length + 1
            infile.close()
            if length == 500:
                print "LED #%d reached %d" % (ledno, length)
                with open("./data/sipm_2000_%d.txt" % ledno, 'r') as fileread:
                    floats = map(float, fileread)
                break
        average = total / length
        self.display5.Clear()
        self.display5.AppendText('V_max = ')
        self.display5.AppendText(str(average))
        self.display5.AppendText(' mV')
        if average > 50:
            self.display5.SetBackgroundColour("green")
        else:
            self.display5.SetBackgroundColour("red")
        self.axes1.clear()
        self.axes2.clear()
        plt.figure(2)
#        plt.axis([0, 500,0, 100])
        plt.hist(floats,20)
        plt.title("Amplitude Histogram")
        plt.xlabel("Amplitude [mV]")
        plt.ylabel("Frequency")
        self.canvas2.draw()
        plt.figure(1)
        data = np.loadtxt("./data/sipm_2000_%d_full.txt" % ledno)
        plt.plot(data[:,0],data[:,1],'ro')
        plt.title("SiPM traces")
        plt.ylabel("Amplitude [mV]")
        plt.xlabel("time [ns]")
        self.canvas1.draw()

    def OnClose(self, event):
        self.Close()
        ser1.write('OUTPUT OFF\n')
        p.stdin.write("exit\n")

    def ReadTemp(self, event):
        self.display3.Clear()
        self.display3.AppendText('T = ')
	self.display3.AppendText(str(lj.read_temperature()))
        self.display3.AppendText(' C')

    def ReadGain(self, event):
        self.display2.Clear()
        self.display2.AppendText('Gain = ')
        self.display2.AppendText(str(lj.read_gain()))

    def Gain50(self, event):
        lj.set_gain(50)
        self.display2.Clear()
        self.display2.AppendText('Gain = ')
        self.display2.AppendText(str(lj.read_gain()))

    def Gain60(self, event):
        lj.set_gain(60)
        self.display2.Clear()
        self.display2.AppendText('Gain = ')
        self.display2.AppendText(str(lj.read_gain()))

    def Gain80(self, event):
        lj.set_gain(80)
        self.display2.Clear()
        self.display2.AppendText('Gain = ')
        self.display2.AppendText(str(lj.read_gain()))


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'SiPM QC Station Control Panel')
        frame.Show(True)
        frame.BKoff(self)
        frame.ReadTemp(self)
        frame.ReadGain(self)
        self.SetTopWindow(frame)
        return True


# ----- Main program -------

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()


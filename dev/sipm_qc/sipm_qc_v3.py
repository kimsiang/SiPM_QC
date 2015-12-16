#!/usr/bin/python

# sipm_qc.py

import zmq
import random
port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

import serial
import gpib
from labjack import labjack
lj = labjack()

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
sipm_no = 0

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
        self.label1 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,50))
        self.label2 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,50))
        self.label3 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,50))
        self.label4 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,50))
        self.label5 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,50))
        self.label6 = wx.TextCtrl(self, -1, '',  style=wx.TE_RIGHT,
                size=(200,50))
        self.display1 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,50))
        self.display2 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,50))
        self.display3 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,50))
        self.display4 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,50))
        self.display5 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,50))
        self.display6 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER,
                size=(200,50))

        ## Set font style and size for the text in the display box
        font1 = wx.Font(20, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.label1.SetFont(font1)
        self.label2.SetFont(font1)
        self.label3.SetFont(font1)
        self.label4.SetFont(font1)
        self.label5.SetFont(font1)
        self.label6.SetFont(font1)
        self.display1.SetFont(font1)
        self.display2.SetFont(font1)
        self.display3.SetFont(font1)
        self.display4.SetFont(font1)
        self.display5.SetFont(font1)
        self.display6.SetFont(font1)

        self.label1.AppendText(' BK [V] ')
        self.label2.AppendText(' Gain [dB]')
        self.label3.AppendText(' T [' + u'\u2103] ')
        self.label4.AppendText(' SiPM # ')
        self.display4.AppendText('0')
        self.label5.AppendText(' LED # ')
        self.label6.AppendText(' V_amp [mV] ')

        gsdisplay = wx.GridSizer(6, 2, 5, 5)
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
            (self.display6, 0, wx.CENTER | wx.TOP | wx.BOTTOM)])


        gsbutton = wx.GridSizer(5, 4, 10, 10)
        gsbutton.AddMany([
                        (wx.Button(self, 24, 'Temp'), 0, wx.EXPAND),
                        #(wx.Button(self, 24, 'Temp', size=(45,45)), 0, wx.EXPAND),
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
        self.Bind(wx.EVT_BUTTON, self.Gain2, id=20)
        self.Bind(wx.EVT_BUTTON, self.Gain3, id=21)
        self.Bind(wx.EVT_BUTTON, self.Gain4, id=22)
        self.Bind(wx.EVT_BUTTON, self.ReadTemp, id=24)
        self.Bind(wx.EVT_BUTTON, self.Led16_3, id=23)
        self.Bind(wx.EVT_BUTTON, self.Led16_2, id=23)
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

    def BKoff(self, event):
        ser1.write('OUTPUT OFF\n')
        ser1.write('SOUR:CURR 3mA\n')
        time.sleep(1.0)
	ser1.write('MEAS:VOLT?\n')
	cur=ser1.read(64)
	self.display1.Clear()
        time.sleep(1)
        self.display1.AppendText(str(cur.split('\n',1)[0]))
        self.display1.SetBackgroundColour("red")
        self.label1.SetBackgroundColour("red")

    def BKon(self, event):
        ser1.write('OUTPUT ON\n')
        ser1.write('SOUR:CURR 3mA\n')
        ser1.write('SOUR:VOLT 66.2V\n')
        time.sleep(1.0)
        ser1.write('MEAS:VOLT?\n')
	cur=ser1.read(64)
	self.display1.Clear()
        self.display1.AppendText(str(cur.split('\n',1)[0]))
        self.display1.SetBackgroundColour("green")
        self.label1.SetBackgroundColour("green")

    def Led1(self, event):
        self.display5.Clear()
        self.display5.AppendText('1')
        self.Update()
        self.calldrs4(1)
        event.Skip()

    def Led2(self, event):
	self.display5.Clear()
        self.display5.AppendText('2')
        self.calldrs4(2)
        event.Skip()

    def Led3(self, event):
	self.display5.Clear()
        self.display5.AppendText('3')
        self.calldrs4(3)
        event.Skip()

    def Led4(self, event):
	self.display5.Clear()
        self.display5.AppendText('4')
        self.calldrs4(4)
        self.Update()
        event.Skip()

    def Led5(self, event):
	self.display5.Clear()
        self.display5.AppendText('5')
        self.calldrs4(5)
        event.Skip()

    def Led6(self, event):
	self.display5.Clear()
        self.display5.AppendText('6')
        self.calldrs4(6)
        event.Skip()

    def Led7(self, event):
	self.display5.Clear()
        self.display5.AppendText('7')
        self.calldrs4(7)
        event.Skip()

    def Led8(self, event):
	self.display5.Clear()
        self.display5.AppendText('8')
        self.calldrs4(8)
        event.Skip()

    def Led9(self, event):
	self.display5.Clear()
        self.display5.AppendText('9')
        self.calldrs4(9)
        event.Skip()

    def Led10(self, event):
	self.display5.Clear()
        self.display5.AppendText('10')
        self.calldrs4(10)
        event.Skip()

    def Led11(self, event):
	self.display5.Clear()
        self.display5.AppendText('11')
        self.calldrs4(11)
        event.Skip()

    def Led12(self, event):
	self.display5.Clear()
        self.display5.AppendText('12')
        self.calldrs4(12)
        event.Skip()

    def Led13(self, event):
	self.display5.Clear()
        self.display5.AppendText('13')
        self.calldrs4(13)
        event.Skip()

    def Led14(self, event):
	self.display5.Clear()
        self.display5.AppendText('14')
        self.calldrs4(14)
        event.Skip()

    def Led15(self, event):
	self.display5.Clear()
        self.display5.AppendText('15')
        self.calldrs4(15)
        event.Skip()

    def Led16(self, event):
        self.display5.Clear()
        self.display5.AppendText('16')
        self.calldrs4(16)
        event.Skip()

    def Led16_2(self, event):
        lj.set_gain(66)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        self.display5.Clear()
        self.display5.AppendText('16_2')
        self.Update()
        self.calldrs4(17)
        event.Skip()

    def Led16_3(self, event):
        lj.set_gain(56)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        self.display5.Clear()
        self.display5.AppendText('16_3')
        self.Update()
        self.calldrs4(18)
        event.Skip()

    def calldrs4(self, led_no):
        try:
            sipm_no = int(self.display4.GetValue())
            if led_no == 1:
                print "Checking SiPM #%d" % sipm_no
            self.display4.SetBackgroundColour("white")
            self.label4.SetBackgroundColour("white")
            if led_no > 16:
                lj.set_led(16)
            p.stdin.write("%d\n" % sipm_no)
            time.sleep(0.1)
            p.stdin.write("%d\n" % led_no)
            self.callplotter(led_no)
        except ValueError:
            print '!!!! please insert SiPM # !!!!'
            self.display4.SetBackgroundColour("red")
            self.label4.SetBackgroundColour("red")

    def callplotter(self, led_no):
        sipm_no = int(self.display4.GetValue())
        total = 0.0
        length = 0.0
        average = 0.0
        #Open the file
        while not os.path.isfile("./data/sipm_%d/sipm_%d_%d.txt" % (sipm_no,
            sipm_no, led_no)):
            time.sleep(1)

        while True:
            infile = open("./data/sipm_%d/sipm_%d_%d.txt" % (sipm_no, sipm_no,
                led_no), 'r+')
            for line in infile:
                amount = float(line)
                total += amount
                length = length + 1
            infile.close()
            if length == 500:
                with open("./data/sipm_%d/sipm_%d_%d.txt" % (sipm_no, sipm_no,
                    led_no), 'r+') as fileread:
                    floats = map(float, fileread)
                break
        average = total / length + 100
        print "LED #%d V_amp %.2f" % (led_no, average)
        self.display6.Clear()
        self.display6.AppendText(str(average))
        if average > 40:
            self.display6.SetBackgroundColour("green")
            self.label6.SetBackgroundColour("green")
        else:
            self.display6.SetBackgroundColour("red")
            self.label6.SetBackgroundColour("red")
        self.axes1.clear()
        self.axes2.clear()
        plt.figure(2)
        plt.hist(floats,25)
        plt.title("Amplitude Histogram")
        plt.xlabel("Amplitude [mV]")
        plt.ylabel("Frequency")
        self.canvas2.draw()
        plt.figure(1)
        data = np.loadtxt("./data/sipm_%d/sipm_%d_%d_full.txt" % (sipm_no,
            sipm_no, led_no) )
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
        temp = lj.read_temperature()
        self.display3.Clear()
	self.display3.AppendText(str(temp))
        if 20 <= float(temp) <= 40:
            self.display3.SetBackgroundColour("green")
            self.label3.SetBackgroundColour("green")
        else:
            self.display3.SetBackgroundColour("red")
            self.label3.SetBackgroundColour("red")

    def ReadGain(self, event):
        lj.set_gain(80)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))

    def Gain2(self, event):
        lj.set_gain(64)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))

    def Gain3(self, event):
        lj.set_gain(40)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))

    def Gain4(self, event):
        lj.set_gain(24)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'SiPM QC Station Control Panel')
        msg = socket.recv()
        print msg
        socket.send("client message to server")
        frame.Show(True)
        frame.BKoff(self)
        frame.ReadTemp(self)
        frame.ReadGain(self)
        frame.display4.SetBackgroundColour("red")
        frame.label4.SetBackgroundColour("red")
        self.SetTopWindow(frame)
        return True


# ----- Main program -------

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()


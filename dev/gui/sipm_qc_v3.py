#!/usr/bin/python

# sipm_qc_v3.py

print '##########################################################'

## Import serial for BK precision voltage control
from bk_precision import BKPrecision
bk = BKPrecision('/dev/ttyUSB0')

## Import serial and labjack for I/O
from labjack import labjack
lj = labjack()

## Import wx, wxversion for GUI
import wx
#import wxversion
#wxversion.select("2.8")
import glob

## Import system process for process handling
import time, sys, subprocess, os, threading, signal

p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, shell=True)
(out, err) = p.communicate()
p_status = p.wait()

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
if p:
    print '>>> DRS4 running alright!'

print '##########################################################'
## initiaize SiPM #
sipm_no = 0
v_setpoint = 0

## Import time classes
from datetime import date,datetime,tzinfo,timedelta
from decimal import Decimal

## Import tools for fast plotting
import matplotlib
matplotlib.use('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from scipy.optimize import curve_fit
from numpy import arange, sin, pi
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal
gaussian_numbers = normal(size=1000)

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

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
        font2 = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

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
        self.display7.SetFont(font2)
        self.display8.SetFont(font2)

        ## Set Label names
        self.label1.AppendText(' BK [V] ')
        self.label2.AppendText(' Gain [dB]')
        self.label3.AppendText(' T [' + u'\u2103] ')
        self.label4.AppendText(' SiPM # ')
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
        gsbutton = wx.GridSizer(6, 4, 10, 10)
        gsbutton.AddMany([
                        (wx.Button(self, 24, 'Update T', size=(80,50)), 0, wx.EXPAND),
                        (wx.Button(self, 17, 'BK OFF'), 0, wx.EXPAND),
                        (wx.Button(self, 18, 'BK ON'), 0, wx.EXPAND),
                        (wx.Button(self, 19, 'Update'), 0, wx.EXPAND),
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

        ## Binding buttons to their respective actions
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
        self.Bind(wx.EVT_BUTTON, self.Update, id=19)
        self.Bind(wx.EVT_BUTTON, self.SetGain1, id=20)
        self.Bind(wx.EVT_BUTTON, self.SetGain2, id=21)
        self.Bind(wx.EVT_BUTTON, self.SetGain3, id=22)
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

        ## Switch off BK precision output after setting HV to 0 V
    def BKoff(self, event):
        global v_setpoint
        v_setpoint = float(bk.meas_volt()[:4])
        print "Saving V_setpoint ...... V_setpoint = %f" % v_setpoint
        bk.set_volt(0.0)
        bk.power_off()
        bk.set_curr(0.005)
        time.sleep(2)
	self.display1.Clear()
        self.display1.AppendText(bk.meas_volt())
        self.display1.SetBackgroundColour("red")
        self.label1.SetBackgroundColour("red")

        ## Switch on BK precision output. set current limit to 5 mA
    def BKon(self, event):
        bk.power_on()
        print "Current V_setpoint ...... V_setpoint = %f" % v_setpoint
        bk.set_volt(v_setpoint)
        time.sleep(2)
        print "Current HV: %f ......" % float(bk.meas_volt())
        self.SetGain1(self)
        self.ReadGain(self)
        self.ReadTemp(self)
        self.display1.Clear()
        self.display1.AppendText(bk.meas_volt())
        self.display1.SetBackgroundColour("green")
        self.label1.SetBackgroundColour("green")
#	self.display4.Clear()
#        self.display4.AppendText(self.check_serial())

    def Update(self, event):
        print 'Updating HV and EEPROM ......'
        self.SetGain1(self)
        if float(self.display1.GetValue()) > -0.01 and float(self.display1.GetValue()) < 70.01:
            bk.set_volt(float(self.display1.GetValue()))
            time.sleep(2)
            self.display1.Clear()
            self.display1.AppendText(bk.meas_volt())
        else:
            print "HV out of range!!! (0 - 70 V)"
        self.enter_serial()

        ## Switch on LED 1
    def Led1(self, event):
        self.display5.Clear()
        self.display5.AppendText('1')
        self.calldrs4(1)
        event.Skip()

        ## Switch on LED 2
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
        lj.set_gain(40)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        self.display5.Clear()
        self.display5.AppendText('16_Gain2')
        self.calldrs4(17)
        event.Skip()

    def Led16_3(self, event):
        lj.set_gain(24)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        self.display5.Clear()
        self.display5.AppendText('16_Gain3')
        self.calldrs4(18)
        event.Skip()

    def eeprom_read(self):
        eeprom_read_int = lj.read_eeprom(1)
        er_array = [chr(i) for i in eeprom_read_int]
        er_string = ''.join(er_array)
        er_array = er_string.split(' ')
        self.display8.Clear()
        self.display8.AppendText(er_string)
        self.display8.SetBackgroundColour("green")
        self.label8.SetBackgroundColour("green")
        return er_array[1]

    def check_serial(self):
        print 'Checking SiPM Serial# ......'
        eeprom_read_int = lj.read_eeprom(1)
        er_array = [chr(i) for i in eeprom_read_int]
        er_string = ''.join(er_array)
        er_array = er_string.split(' ')
        if len(er_array) == 3 and er_array[0] == er_array[2] and er_array[1] == 'UWSiPM':
            self.display4.SetBackgroundColour("green")
            self.label4.SetBackgroundColour("green")
            print 'Serial# found! It is %s ......' % str(int(er_array[0]))
            self.display4.Clear()
            self.display4.AppendText(str(int(er_array[0])))
            return str(int(er_array[0]))
        else:
            self.display4.SetBackgroundColour("red")
            self.label4.SetBackgroundColour("red")
            print 'Unknown SiPM#. Please insert a SiPM# .......'
            return 'Unknown'

    def enter_serial(self):
        sn = int(self.display4.GetValue())
        if self.eeprom_read() == 'UWSiPM':
            print 'Serial number exist !!!'
            self.display4.SetBackgroundColour("green")
            self.label4.SetBackgroundColour("green")
        elif sn > 0 and sn < 1500:
            sn_string = ('%04d UWSiPM %04d') % (sn, sn)
            sn_list = list(sn_string)
            sn_int_array = [ord(s) for s in sn_list]
            lj.write_eeprom(1, sn_int_array)
            self.display7.Clear()
            self.display7.AppendText(sn_string)
            self.display7.SetBackgroundColour("green")
            self.label7.SetBackgroundColour("green")
            self.display4.SetBackgroundColour("green")
            self.label4.SetBackgroundColour("green")
            self.eeprom_read()
        else:
            print 'Invalid serial number!!!'


      #      if eeprom_read == sipm_no:
      #          self.display8.Clear()
      #          self.display8.AppendText(str(eeprom_read))
      #          self.display8.SetBackgroundColour("green")
      #          self.label8.SetBackgroundColour("green")

        ## Run drs4_exam and write SiPM # into EEPROM
    def calldrs4(self, led_no):
        try:
            sipm_no = int(self.display4.GetValue())
            if sipm_no > 0:
                print ">>> Checking SiPM #%d LED #%d" % (sipm_no, led_no)
            self.display5.SetBackgroundColour("green")
            self.label5.SetBackgroundColour("green")
            self.display4.SetBackgroundColour("green")
            self.label4.SetBackgroundColour("green")
            self.display7.SetBackgroundColour("green")
            self.label7.SetBackgroundColour("green")
            #self.display7.Clear()
            #self.display7.AppendText(str(sipm_no))

            lj.set_led(led_no)
            #self.display4.SetBackgroundColour("white")
            #self.label4.SetBackgroundColour("white")
            if led_no > 16:
                lj.set_led(16)
            time.sleep(0.1)
            p.stdin.write("%d\n" % sipm_no)
            time.sleep(0.1)
            p.stdin.write("%d\n" % led_no)
            time.sleep(0.5)
            self.callanalyzer(led_no)
        except ValueError:
            print '!!!! please insert SiPM # !!!!'
            self.display4.SetBackgroundColour("red")
            self.label4.SetBackgroundColour("red")

        ## Plot traces and amplitude historgram after each LED flashes and store data
    def callanalyzer(self, led_no):
        sipm_no = int(self.display4.GetValue())
        total = 0.0
        length = 0
        average = 0.0
        test_no = -1

        for name in glob.glob("./data/sipm_%d_*" % sipm_no):
            test_no = test_no + 1

        print 'Plotting traces from SiPM #%d, test #%d, LED #%d' % (sipm_no,
                test_no, led_no)


        while os.path.isfile("./data/sipm_%d_%02d/sipm_%d_%d.txt" % (sipm_no,
            test_no, sipm_no, led_no)):
            infile = open("./data/sipm_%d_%02d/sipm_%d_%d.txt" % (sipm_no,
                test_no, sipm_no,
                led_no), 'r+')
            for line in infile:
                amount = float(line)
                total += amount
                length = length + 1
            infile.close()
            if length == 300:
                with open("./data/sipm_%d_%02d/sipm_%d_%d.txt" % (sipm_no,
                    test_no, sipm_no,
                    led_no), 'r+') as fileread:
                    floats = map(float, fileread)
                break
        average = total / length
        print "LED #%d V_amp %.2f" % (led_no, average)

        ## storing data for traveler in a file
        f_data = open("./data/sipm_%d_%02d/sipm_%d.txt" % (sipm_no, test_no, sipm_no),'a+')
        if led_no == 1:
            f_data.write("%d\n" % sipm_no)
            self.SetGain1(self)
            time.sleep(0.1)
            f_data.write("%f\n" % self.ReadGain(self))
            self.SetGain2(self)
            time.sleep(0.1)
            f_data.write("%f\n" % self.ReadGain(self))
            self.SetGain3(self)
            time.sleep(0.1)
            f_data.write("%f\n" % self.ReadGain(self))
            self.SetGain1(self)
            time.sleep(0.1)
            f_data.write("%.3f\n" % float(bk.meas_volt()))
            f_data.write("%.3f\n" % float(bk.meas_curr()))
            f_data.write("%.3f\n" % self.ReadTemp(self))

        ## storing average amplitudes of a measurement
        f_data.write("%.2f\n" % average)
        f_data.close()
        self.display6.Clear()
        self.display6.AppendText(str(average))
        if average > 30:
            self.display6.SetBackgroundColour("green")
            self.label6.SetBackgroundColour("green")
        else:
            self.display6.SetBackgroundColour("red")
            self.label6.SetBackgroundColour("red")
        self.axes1.clear()
        self.axes2.clear()
        plt.figure(2)
        if False:
            n, bins, patches = plt.hist(floats,25)
            bin_centres = (bins[:-1] + bins[1:])/2
            # p0 is the initial guess for the fitting coefficients (A, mu and sigma
            # above)
            coeff, var_matrix = curve_fit(gauss, bin_centres, n, p0=[100.,average,5.])
            hist_fit = gauss(bin_centres, *coeff)
            plt.plot(bin_centres, hist_fit, label='Fitted data', linewidth=2)
            print 'Fitted mean = ', coeff[1]
            print 'Fitted standard deviation = ', coeff[2]
            fdata = open("vbd.txt", "a+")
            print >> fdata, float(bk.meas_volt()), ' ', coeff[1], ' ', coeff[2]
        plt.title("Amplitude Histogram")
        plt.xlabel("Amplitude [mV]")
        plt.ylabel("Frequency")
        self.canvas2.draw()
        plt.figure(1)
        data = np.loadtxt("./data/sipm_%d_%02d/sipm_%d_%d_full.txt" % (sipm_no,
            test_no, sipm_no, led_no) )
        plt.plot(data[:,0],data[:,1],'ro')
        plt.title("SiPM traces")
        plt.ylabel("Amplitude [mV]")
        plt.xlabel("time [ns]")
        self.canvas1.draw()
        if led_no == 18:
            print ">>> Measurement completed!"

    def OnClose(self, event):
        bk.power_off()
        p.stdin.write("exit\n")
        self.Close()

        ## Read temperature from the SiPM board T-sensor
    def ReadTemp(self, event):
        temp = lj.read_temperature()
        self.display3.Clear()
	self.display3.AppendText(str(temp))
        if 20 <= float(temp) <= 45:
            self.display3.SetBackgroundColour("green")
            self.label3.SetBackgroundColour("green")
        else:
            self.display3.SetBackgroundColour("red")
            self.label3.SetBackgroundColour("red")
        return float(temp)

        ## Read gain from the SiPM board PGA
    def ReadGain(self, event):
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        if int(lj.read_gain()) == 10:
            self.display2.SetBackgroundColour("green")
            self.label2.SetBackgroundColour("green")
        else:
            self.display2.SetBackgroundColour("red")
            self.label2.SetBackgroundColour("red")
        return lj.read_gain()

        ## Set gain 10 dB on the SiPM board PGA
    def SetGain1(self, event):
        lj.set_gain(10)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        if int(lj.read_gain()) == 10:
            self.display2.SetBackgroundColour("green")
            self.label2.SetBackgroundColour("green")
        else:
            self.display2.SetBackgroundColour("red")
            self.label2.SetBackgroundColour("red")

        ## Set gain 16 dB on the SiPM board PGA
    def SetGain2(self, event):
        lj.set_gain(16)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        if int(lj.read_gain()) == 16:
            self.display2.SetBackgroundColour("green")
            self.label2.SetBackgroundColour("green")
        else:
            self.display2.SetBackgroundColour("red")
            self.label2.SetBackgroundColour("red")

        ## Set gain 20 dB on the SiPM board PGA
    def SetGain3(self, event):
        lj.set_gain(20)
        self.display2.Clear()
        self.display2.AppendText(str(lj.read_gain()))
        if int(lj.read_gain()) == 20:
            self.display2.SetBackgroundColour("green")
            self.label2.SetBackgroundColour("green")
        else:
            self.display2.SetBackgroundColour("red")
            self.label2.SetBackgroundColour("red")

class MyApp(wx.App):
    def OnInit(self):
        print 'Initializing SiPM QC (L0) Station Control Panel ......'
        frame = MyFrame(None, -1, 'SiPM QC Station Control Panel')
        frame.Show(True)
        frame.BKoff(self)
        frame.ReadTemp(self)
        frame.SetGain1(self)
        frame.ReadGain(self)
        frame.display4.SetBackgroundColour("red")
        frame.label4.SetBackgroundColour("red")
        frame.check_serial()
        self.SetTopWindow(frame)
        return True


# ----- Main program -------

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()


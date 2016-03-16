import wx
import matplotlib
matplotlib.use('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.dates import strpdate2num
import matplotlib.dates as mdates
import numpy as np
from scipy.optimize import curve_fit
from Gnuplot import Gnuplot
from datetime import date, datetime, tzinfo, timedelta
import time
import os
import signal
import sqlite3 as sqlite
# print wx.__file__


def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

# Define logger panel here


class sql_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer()
        self.SetBackgroundColour("Light Grey")

        # for allowing sorting in descending order
        self.oldC = -1
        self.reverse = False
        self.command = "SELECT * FROM runlog ORDER by date DESC"

        self.database = wx.ListCtrl(self, -1,
                                    style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()
        self.setupDB()

    def __do_layout(self):
        self.Bind(wx.EVT_LIST_COL_CLICK, self.setupSort, self.database)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.database, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def __set_properties(self):
        self.database.InsertColumn(0, "Amp_Avg")
        self.database.InsertColumn(1, "Current")
        self.database.InsertColumn(2, "Datetime")
        self.database.InsertColumn(3, "Gain")
        self.database.InsertColumn(4, "Run_No")
        self.database.InsertColumn(5, "Serial_No")
        self.database.InsertColumn(6, "Subrun_No")
        self.database.InsertColumn(7, "Temperature")
        self.database.InsertColumn(8, "Type")
        self.database.InsertColumn(9, "Voltage")
        self.database.SetColumnWidth(0, 80)
        self.database.SetColumnWidth(1, 80)
        self.database.SetColumnWidth(2, 150)
        self.database.SetColumnWidth(3, 100)
        self.database.SetColumnWidth(4, 100)
        self.database.SetColumnWidth(5, 100)
        self.database.SetColumnWidth(6, 100)
        self.database.SetColumnWidth(7, 100)
        self.database.SetColumnWidth(8, 100)
        self.database.SetColumnWidth(9, 100)

    def setupDB(self):
        self.con = sqlite.connect("runlog.db")
        c = self.con.cursor()
        string = 'amp_avg, curr, date, gain, run_no, ' \
                 'serial_no, subrun_no, temp, run_type, volt'
        c.execute('create table if not exists runlog ({})'.format(string))
        self.fillDB()

    def setupSort(self, event):
        """Sets the command for filling the list control, based on
        what column is clicked
        """
        c = event.GetColumn()  # get the column that was clicked on

        if c == 0:
            # order by first column
            self.command = "SELECT * FROM runlog ORDER BY amp_avg"
        elif c == 1:
            # order by second column
            self.command = "SELECT * FROM runlog ORDER BY curr"
        elif c == 2:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY date"
        elif c == 3:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY gain"
        elif c == 4:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY run_no"
        elif c == 5:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY serial_no"
        elif c == 6:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY subrun_no"
        elif c == 7:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY temp"
        elif c == 8:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY run_type"
        elif c == 9:
            # order by third column
            self.command = "SELECT * FROM runlog ORDER BY volt"

        # Toggle reverse
        if c == self.oldC:
            self.reverse = not self.reverse
        else:
            self.reverse = False

        # if reverse, append "DESC" to the select command
        if self.reverse:
            self.command += " DESC"

        self.oldC = c
        self.fillDB()
        event.Skip()

    def fillDB(self):
        self.database.DeleteAllItems()  # since we're sorting, must delete all
        # then get a list of tuples of all the data
        data = self.con.execute(self.command).fetchall()
        for i in data:
            # loop through and add it
            self.database.Append(i[0:])


class logger_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer()
        self.SetBackgroundColour("Light Grey")

        # a multiline TextCtrl for logging purpose
        self.logger = wx.TextCtrl(self, size=(500, 1000),
                style=wx.TE_MULTILINE | wx.TE_READONLY |wx.TE_RICH2 | wx.BORDER_SUNKEN)

        # set black background and white fonts
        self.logger.SetBackgroundColour("Black")
        self.logger.SetForegroundColour("White")

        sizer.Add(self.logger, 0, wx.ALL, 5)
        self.SetSizerAndFit(sizer)

    def __del__(self):
        pass

# Define display panel here


class display_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("Light Grey")

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # add figure
        self.figure3 = plt.figure(3, dpi=60)
        self.figure4 = plt.figure(4, dpi=60)
        self.figure5 = plt.figure(5, dpi=60)
        self.figure6 = plt.figure(6, dpi=60)

        self.axes3 = self.figure3.add_subplot(111)
        self.axes4 = self.figure4.add_subplot(111)
        self.axes5 = self.figure5.add_subplot(111)
        self.axes6 = self.figure6.add_subplot(111)

        self.canvas3 = FigureCanvas(self, -1, self.figure3)
        self.canvas4 = FigureCanvas(self, -1, self.figure4)
        self.canvas5 = FigureCanvas(self, -1, self.figure5)
        self.canvas6 = FigureCanvas(self, -1, self.figure6)

        hSizer1.Add(self.canvas3, 0, wx.EXPAND, 5)
        hSizer1.AddSpacer(10)
        hSizer1.Add(self.canvas4, 0, wx.EXPAND, 5)

        hSizer2.Add(self.canvas5, 0, wx.EXPAND, 5)
        hSizer2.AddSpacer(10)
        hSizer2.Add(self.canvas6, 0, wx.EXPAND, 5)

        mainSizer.Add(hSizer1, 0, wx.ALL, 5)
        mainSizer.Add(hSizer2, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

    def plot_temp(self, _filename):
        if os.path.isfile(_filename):

            readout = np.loadtxt(_filename, usecols=(1, 2, 3, 4, 5),
                                 converters={1: strpdate2num('%H:%M:%S')},
                                 unpack=True)
            time, temp, volt, curr, gain = readout

            self.axes3.clear()
            plt.figure(3)
            plt.plot(time[-5000:], temp[-5000:], lw=2)
            plt.title("Temperature")
            plt.ylabel("T [C]")
            plt.xlabel("time [hh:mm]")
            xfmt = mdates.DateFormatter('%H:%M')
            self.axes3.xaxis.set_major_formatter(xfmt)
            self.axes3.grid(True, linewidth=1)
            self.canvas3.draw()

            self.axes4.clear()
            plt.figure(4)
            plt.plot(time[-5000:], gain[-5000:], lw=2)
            plt.title("Gain")
            plt.ylabel("G [dB]")
            plt.xlabel("time [hh:mm]")
            plt.grid(True)
            self.axes4.xaxis.set_major_formatter(xfmt)
            self.axes4.grid(True, linewidth=1)
            self.canvas4.draw()

            self.axes5.clear()
            plt.figure(5)
            plt.plot(time[-5000:], volt[-5000:], lw=2)
            plt.title("Volt")
            plt.ylabel("V [V]")
            plt.xlabel("time [hh:mm]")
            plt.grid(True)
            self.axes5.xaxis.set_major_formatter(xfmt)
            self.axes5.grid(True, linewidth=1)
            self.canvas5.draw()

            self.axes6.clear()
            plt.figure(6)
            plt.plot(time[-5000:], curr[-5000:], lw=2)
            plt.title("Current")
            plt.ylabel("I [mA]")
            plt.xlabel("time [hh:mm]")
            plt.grid(True)
            self.axes6.xaxis.set_major_formatter(xfmt)
            self.axes6.grid(True, linewidth=1)
            self.canvas6.draw()

    def __del__(self):
        pass

# Define control panel here


class control_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._single_gauge_max = 1
        self._led_gauge_max = 18
        self._volt_gauge_max = 16

        # add figure
        self.figure1 = plt.figure(1, dpi=55)
        self.axes1 = self.figure1.add_subplot(111)
        self.canvas1 = FigureCanvas(self, -1, self.figure1)
        self.figure2 = plt.figure(2, dpi=55)
        self.axes2 = self.figure2.add_subplot(111)
        self.canvas2 = FigureCanvas(self, -1, self.figure2)

        # bk precision PS Label
        self.quote1 = wx.StaticText(self, label="BK Precision")

        # bk status
        self.lbl9 = wx.StaticText(self, label="Status")
        self.lbl9r = wx.StaticText(self, label="NO")
        self.lbl9w = wx.StaticText(self, label="")

        # bk output
        self.lbl1 = wx.StaticText(self, label='OUTPUT')
        self.lbl1r = wx.StaticText(self, label='OFF')
        self.lbl1w = wx.StaticText(self, label="")
        self.lbl1s = wx.Button(self, label="Set ON")

        # bk V[V]
        self.lbl2 = wx.StaticText(self, label='V [V]')
        self.lbl2r = wx.StaticText(self, label='0.00')
        self.lbl2w = wx.SpinCtrlDouble(
            self, value='0.00', name="Roll V [V]")
        self.lbl2s = wx.Button(self, label="Set V")

        # bk I[A]
        self.lbl3 = wx.StaticText(self, label='I [mA]')
        self.lbl3r = wx.StaticText(self, label='0.00')
        self.lbl3w = wx.SpinCtrl(self, value='5.00', name="Roll I [mA]")
        self.lbl3s = wx.Button(self, label="Set I")

        # sipm Board Label
        self.quote2 = wx.StaticText(self, label="SiPM Board")

        # sipm status
        self.lbl8 = wx.StaticText(self, label="Status")
        self.lbl8r = wx.StaticText(self, label="NO")
        self.lbl8w = wx.StaticText(self, label="")

        # sipm number
        self.lbl4 = wx.StaticText(self, label="SiPM#")
        self.lbl4r = wx.StaticText(self, label="1")
        self.lbl4w = wx.SpinCtrl(self, value='1', name="Roll SiPM#")
        self.lbl4s = wx.Button(self, label="Set SiPM#")

        # T [C]
        self.lbl5 = wx.StaticText(self, label='T [' + u'\u2103]')
        self.lbl5r = wx.StaticText(self, label="25.00")
        self.lbl5w = wx.StaticText(self, label="")

        # gain [dB]
        self.lbl6 = wx.StaticText(self, label='Gain [dB]')
        self.lbl6r = wx.StaticText(self, label="10.0")
        self.lbl6w = wx.SpinCtrl(self, value='10', name="Roll Gain [dB]")
        self.lbl6s = wx.Button(self, label="Set Gain")

        # led Board Label
        self.quote3 = wx.StaticText(self, label="LED Board")

        # led #
        self.lbl7 = wx.StaticText(self, label="LED#")
        self.lbl7r = wx.StaticText(self, label="1")
        self.lbl7w = wx.SpinCtrl(self, value='1', name="Roll LED#")
        self.lbl7s = wx.Button(self, label="Set LED#")

        # end of grid1

        # sipm Board Label
        self.quote4 = wx.StaticText(self, label="SiPM Board")
        self.btn1 = wx.Button(self, label="Gain10")
        self.btn2 = wx.Button(self, label="Gain16")
        self.btn3 = wx.Button(self, label="Gain20")
        self.btn4 = wx.Button(self, label="Gain26")

        # led Board Label
        self.quote5 = wx.StaticText(self, label="LED Board")
        self.led1 = wx.Button(self, label="LED1")
        self.led2 = wx.Button(self, label="LED2")
        self.led3 = wx.Button(self, label="LED3")
        self.led4 = wx.Button(self, label="LED4")
        self.led5 = wx.Button(self, label="LED5")
        self.led6 = wx.Button(self, label="LED6")
        self.led7 = wx.Button(self, label="LED7")
        self.led8 = wx.Button(self, label="LED8")
        self.led9 = wx.Button(self, label="LED9")
        self.led10 = wx.Button(self, label="LED10")
        self.led11 = wx.Button(self, label="LED11")
        self.led12 = wx.Button(self, label="LED12")
        self.led13 = wx.Button(self, label="LED13")
        self.led14 = wx.Button(self, label="LED14")
        self.led15 = wx.Button(self, label="LED15")
        self.led16 = wx.Button(self, label="LED16")

        # drs4 board label
        self.quote6 = wx.StaticText(self, label="DRS 4 Board")

        #  daq buttons
        self.drs4_button = wx.Button(self, label="Run DRS4")
        self.led_scan_button = wx.Button(self, label="Run LED Scan")
        self.volt_scan_button = wx.Button(self, label="Run Voltage Scan")

        self.gaugelbl1 = wx.StaticText(self, label="Single")
        self.gaugelbl2 = wx.StaticText(self, label="LED")
        self.gaugelbl3 = wx.StaticText(self, label="Bias")

        self.single_gauge = wx.Gauge(self,
                                     range=self._single_gauge_max,
                                     size=(250, 25))
        self.led_gauge = wx.Gauge(self, range=self._led_gauge_max,
                                  size=(250, 25))
        self.volt_gauge = wx.Gauge(self, range=self._volt_gauge_max,
                                   size=(250, 25))

        # implement the settings in 3 other functions
        self.set_properties()
        self.do_layout()

    def set_properties(self):
        # set the properties of the items created
        self.lbl2w.SetDigits(1)
        self.lbl2w.SetRange(0.0, 70.0)
        self.lbl2w.SetIncrement(0.1)

        self.lbl3w.SetRange(0, 5)
        self.lbl4w.SetRange(1, 1500)
        self.lbl6w.SetRange(6, 26)
        self.lbl7w.SetRange(1, 16)

        _font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                        False, u'Consolas')
        _bold_font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.BOLD,
                             False, u'Consolas')
        _big_font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.BOLD,
                            False, u'Consolas')

        self.drs4_button.SetFont(_big_font)
        self.led_scan_button.SetFont(_big_font)
        self.volt_scan_button.SetFont(_big_font)

        self.quote1.SetFont(_big_font)
        self.quote2.SetFont(_big_font)
        self.quote3.SetFont(_big_font)
        self.quote4.SetFont(_big_font)
        self.quote5.SetFont(_big_font)
        self.quote6.SetFont(_big_font)

        self.lbl9.SetFont(_font)
        self.lbl9r.SetFont(_bold_font)
        self.lbl9w.SetFont(_font)

        self.lbl1.SetFont(_font)
        self.lbl1r.SetFont(_bold_font)
        self.lbl1w.SetFont(_font)
        self.lbl1s.SetFont(_font)

        self.lbl2.SetFont(_font)
        self.lbl2r.SetFont(_bold_font)
        self.lbl2w.SetFont(_font)
        self.lbl2s.SetFont(_font)

        self.lbl3.SetFont(_font)
        self.lbl3r.SetFont(_bold_font)
        self.lbl3w.SetFont(_font)
        self.lbl3s.SetFont(_font)

        self.lbl8.SetFont(_font)
        self.lbl8r.SetFont(_bold_font)
        self.lbl8w.SetFont(_font)

        self.lbl4.SetFont(_font)
        self.lbl4r.SetFont(_bold_font)
        self.lbl4w.SetFont(_font)
        self.lbl4s.SetFont(_font)

        self.lbl5.SetFont(_font)
        self.lbl5r.SetFont(_bold_font)
        self.lbl5w.SetFont(_font)

        self.lbl6.SetFont(_font)
        self.lbl6r.SetFont(_bold_font)
        self.lbl6w.SetFont(_font)
        self.lbl6s.SetFont(_font)

        self.lbl7.SetFont(_font)
        self.lbl7r.SetFont(_bold_font)
        self.lbl7w.SetFont(_font)
        self.lbl7s.SetFont(_font)

        self.btn1.SetFont(_font)
        self.btn2.SetFont(_font)
        self.btn3.SetFont(_font)
        self.btn4.SetFont(_font)

        self.led1.SetFont(_font)
        self.led2.SetFont(_font)
        self.led3.SetFont(_font)
        self.led4.SetFont(_font)

        self.led5.SetFont(_font)
        self.led6.SetFont(_font)
        self.led7.SetFont(_font)
        self.led8.SetFont(_font)

        self.led9.SetFont(_font)
        self.led10.SetFont(_font)
        self.led11.SetFont(_font)
        self.led12.SetFont(_font)

        self.led13.SetFont(_font)
        self.led14.SetFont(_font)
        self.led15.SetFont(_font)
        self.led16.SetFont(_font)

        self.gaugelbl1.SetFont(_font)
        self.gaugelbl2.SetFont(_font)
        self.gaugelbl3.SetFont(_font)

    def do_layout(self):
        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=10, vgap=10)
        grid2 = wx.GridBagSizer(hgap=10, vgap=10)
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        # start of grid1
        grid.Add(self.quote1, pos=(0, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lbl9, pos=(1, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl9r, pos=(1, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl9w, pos=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lbl1, pos=(2, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl1r, pos=(2, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl1w, pos=(2, 2), flag=wx.TE_CENTER)
        grid.Add(self.lbl1s, pos=(2, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.lbl2, pos=(3, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl2r, pos=(3, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl2w, pos=(3, 2), flag=wx.TE_CENTER)
        grid.Add(self.lbl2s, pos=(3, 3), flag=wx.TE_CENTER)

        grid.Add(self.lbl3, pos=(4, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl3r, pos=(4, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl3w, pos=(4, 2), flag=wx.TE_CENTER)
        grid.Add(self.lbl3s, pos=(4, 3), flag=wx.TE_CENTER)

        grid.Add(self.quote2, pos=(5, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lbl8, pos=(6, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl8r, pos=(6, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl8w, pos=(6, 2), flag=wx.TE_CENTER)

        grid.Add(self.lbl4, pos=(7, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl4r, pos=(7, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl4w, pos=(7, 2), flag=wx.TE_CENTER)
        grid.Add(self.lbl4s, pos=(7, 3), flag=wx.TE_CENTER)

        grid.Add(self.lbl5, pos=(8, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl5r, pos=(8, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl5w, pos=(8, 2), flag=wx.TE_CENTER)

        grid.Add(self.lbl6, pos=(9, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl6r, pos=(9, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl6w, pos=(9, 2), flag=wx.TE_CENTER)
        grid.Add(self.lbl6s, pos=(9, 3), flag=wx.TE_CENTER)

        grid.Add(self.quote3, pos=(10, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lbl7, pos=(11, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.lbl7r, pos=(11, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lbl7w, pos=(11, 2), flag=wx.TE_CENTER)
        grid.Add(self.lbl7s, pos=(11, 3), flag=wx.TE_CENTER)
        # end of grid1

        # start of grid2
        grid2.Add(self.quote4, pos=(0, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid2.Add(self.btn1, pos=(1, 0), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid2.Add(self.btn2, pos=(1, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid2.Add(self.btn3, pos=(1, 2), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid2.Add(self.btn4, pos=(1, 3), flag=wx.TE_CENTER | wx.ALIGN_CENTER)

        grid2.Add(self.quote5, pos=(2, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid2.Add(self.led1, pos=(3, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led2, pos=(3, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led3, pos=(3, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led4, pos=(3, 3), flag=wx.TE_CENTER)
        grid2.Add(self.led5, pos=(4, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led6, pos=(4, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led7, pos=(4, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led8, pos=(4, 3), flag=wx.TE_CENTER)
        grid2.Add(self.led9, pos=(5, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led10, pos=(5, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led11, pos=(5, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led12, pos=(5, 3), flag=wx.TE_CENTER)
        grid2.Add(self.led13, pos=(6, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led14, pos=(6, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led15, pos=(6, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led16, pos=(6, 3), flag=wx.TE_CENTER)

        grid2.Add(self.quote6, pos=(7, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid2.Add(self.gaugelbl1, pos=(8, 0), flag=wx.EXPAND)
        grid2.Add(self.gaugelbl2, pos=(9, 0), flag=wx.EXPAND)
        grid2.Add(self.gaugelbl3, pos=(10, 0), flag=wx.EXPAND)

        grid2.Add(self.single_gauge, pos=(8, 1), span=(1, 3), flag=wx.EXPAND)
        grid2.Add(self.led_gauge, pos=(9, 1), span=(1, 3), flag=wx.EXPAND)
        grid2.Add(self.volt_gauge, pos=(10, 1), span=(1, 3), flag=wx.EXPAND)
        # end of grid2

        hSizer1.Add(self.canvas1, 0, wx.EXPAND, 5)
        hSizer1.AddSpacer(5)
        hSizer1.Add(self.canvas2, 0, wx.EXPAND, 5)

        hSizer2.Add(grid, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)
        hSizer2.AddSpacer(10)
        hSizer2.Add(grid2, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)

        hSizer3.Add(self.drs4_button, 0, wx.CENTER)
        hSizer3.Add(self.led_scan_button, 0, wx.CENTER)
        hSizer3.Add(self.volt_scan_button, 0, wx.CENTER)

        mainSizer.Add(hSizer1, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        mainSizer.Add(hSizer2, 0, wx.ALL, 5)
        mainSizer.Add(hSizer3, 0, wx.ALIGN_CENTER, 5)

        self.SetSizerAndFit(mainSizer)
        mainSizer.Layout()

    def plot_waveform(self, _filename):
        self.axes1.clear()
        infile = np.loadtxt(_filename)
        plt.figure(1)
        #plt.plot(data[:,0], data[:,1],'ro')
        plt.plot(infile[:500, 0], infile[:500, 1])
        plt.title("SiPM traces")
        plt.ylabel("Amplitude [mV]")
        plt.xlabel("time [ns]")
        self.canvas1.draw()

    def get_amp_avg(self, _filename):
        total = 0.0
        length = 0
        self.average = 0.0
        while os.path.isfile(_filename):
            infile = open(_filename, 'r+')
            for line in infile:
                total += float(line)
                length = length + 1
            infile.close()
            if length == 500:
                with open(_filename, 'r+') as data:
                    floats = map(float, data)
            break
        self.average = total / length
        print "V_amp %.2f" % self.average
        self.axes2.clear()
        plt.figure(2)
        plt.hist(floats, 25)
        plt.title("Amplitude Histogram")
        plt.xlabel("Amplitude [mV]")
        plt.ylabel("Frequency")
        self.canvas2.draw()
        # self.fit_gaussian(floats)
        return self.average

    def plot_led_scan(self):
        pass

    def plot_volt_scan(self):
        pass

    def fit_gaussian(self, _floats):
        n, bins, patches = plt.hist(_floats, 25)
        bin_centres = (bins[:-1] + bins[1:])/2
        # p0 is the initial guess for the fitting coefficients (A, mu and
        # sigma# above)
        results = curve_fit(gauss, bin_centres, n,
                            p0=[100., self.average, 0.05*self.average])
        self.coeff, var_matrix = results
        hist_fit = gauss(bin_centres, *self.coeff)
        plt.plot(bin_centres, hist_fit, label='Fitted data', linewidth=2)
        print 'Fitted mean = ', self.coeff[1]
        print 'Fitted standard deviation = ', self.coeff[2]

    def get_fit_result(self):
        return self.coeff

    def __del__(self):
        pass

# define EEPROM Panel here


class eeprom_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # eeprom Memory Map
        self.quote1 = wx.StaticText(self, label="EEPROM Map")

        self.mem1 = wx.StaticText(self, label='Page1')
        self.mem2 = wx.StaticText(self, label='Page2')
        self.mem3 = wx.StaticText(self, label='Page3')
        self.mem4 = wx.StaticText(self, label='Page4')
        self.mem5 = wx.StaticText(self, label='Page5')
        self.mem6 = wx.StaticText(self, label='Page6')
        self.mem7 = wx.StaticText(self, label='Page7')
        self.mem8 = wx.StaticText(self, label='Page8')

        self.mem1r = wx.StaticText(self, label='')
        self.mem2r = wx.StaticText(self, label='')
        self.mem3r = wx.StaticText(self, label='')
        self.mem4r = wx.StaticText(self, label='')
        self.mem5r = wx.StaticText(self, label='')
        self.mem6r = wx.StaticText(self, label='')
        self.mem7r = wx.StaticText(self, label='')
        self.mem8r = wx.StaticText(self, label='')

        self.mem1w = wx.TextCtrl(self, value='', size=(280, 40))
        self.mem2w = wx.TextCtrl(self, value='')
        self.mem3w = wx.TextCtrl(self, value='')
        self.mem4w = wx.TextCtrl(self, value='')
        self.mem5w = wx.TextCtrl(self, value='')
        self.mem6w = wx.TextCtrl(self, value='')
        self.mem7w = wx.TextCtrl(self, value='')
        self.mem8w = wx.TextCtrl(self, value='')

        self.mem1s = wx.Button(self, label="Set Page1")
        self.mem2s = wx.Button(self, label="Set Page2")
        self.mem3s = wx.Button(self, label="Set Page3")
        self.mem4s = wx.Button(self, label="Set Page4")
        self.mem5s = wx.Button(self, label="Set Page5")
        self.mem6s = wx.Button(self, label="Set Page6")
        self.mem7s = wx.Button(self, label="Set Page7")
        self.mem8s = wx.Button(self, label="Set Page8")

        # implement the settings in 3 other functions
        self.set_properties()
        self.do_layout()

    def set_properties(self):

        self.SetBackgroundColour("Light Grey")
        _font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                        False, u'Consolas')
        _bold_font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                             False, u'Consolas')
        _big_font = wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL,
                            False, u'Consolas')

        self.quote1.SetFont(_big_font)

        self.mem1.SetFont(_font)
        self.mem1r.SetFont(_bold_font)
        self.mem1w.SetFont(_font)
        self.mem1s.SetFont(_font)

        self.mem2.SetFont(_font)
        self.mem2r.SetFont(_bold_font)
        self.mem2w.SetFont(_font)
        self.mem2s.SetFont(_font)

        self.mem3.SetFont(_font)
        self.mem3r.SetFont(_bold_font)
        self.mem3w.SetFont(_font)
        self.mem3s.SetFont(_font)

        self.mem4.SetFont(_font)
        self.mem4r.SetFont(_bold_font)
        self.mem4w.SetFont(_font)
        self.mem4s.SetFont(_font)

        self.mem5.SetFont(_font)
        self.mem5r.SetFont(_bold_font)
        self.mem5w.SetFont(_font)
        self.mem5s.SetFont(_font)

        self.mem6.SetFont(_font)
        self.mem6r.SetFont(_bold_font)
        self.mem6w.SetFont(_font)
        self.mem6s.SetFont(_font)

        self.mem7.SetFont(_font)
        self.mem7r.SetFont(_bold_font)
        self.mem7w.SetFont(_font)
        self.mem7s.SetFont(_font)

        self.mem8.SetFont(_font)
        self.mem8r.SetFont(_bold_font)
        self.mem8w.SetFont(_font)
        self.mem8s.SetFont(_font)

    def do_layout(self):

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=20, vgap=20)

        # start of grid
        grid.Add(self.mem1, pos=(1, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem1r, pos=(1, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem1w, pos=(1, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem1s, pos=(1, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem2,  pos=(2, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem2r, pos=(2, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem2w, pos=(2, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem2s, pos=(2, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem3, pos=(3, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem3r, pos=(3, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem3w, pos=(3, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem3s, pos=(3, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem4, pos=(4, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem4r, pos=(4, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem4w, pos=(4, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem4s, pos=(4, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem5, pos=(5, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem5r, pos=(5, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem5w, pos=(5, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem5s, pos=(5, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem6, pos=(6, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem6r, pos=(6, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem6w, pos=(6, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem6s, pos=(6, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem7, pos=(7, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem7r, pos=(7, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem7w, pos=(7, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem7s, pos=(7, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.mem8, pos=(8, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(self.mem8r, pos=(8, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.mem8w, pos=(8, 2), flag=wx.TE_CENTER | wx.EXPAND)
        grid.Add(self.mem8s, pos=(8, 3), flag=wx.TE_CENTER | wx.EXPAND)

        mainSizer.Add(self.quote1, 0, flag=wx.TE_CENTER)
        mainSizer.Add(grid, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)

        self.SetSizerAndFit(mainSizer)
        self.Layout()

    def __del__(self):
        pass

import wx
import matplotlib
matplotlib.use('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from datetime import date, datetime, tzinfo, timedelta
# print wx.__file__

## Define display panel here
class display_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("Silver")

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button2 = wx.Button(self, wx.ID_ANY, "Control Panel",
                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3 = wx.Button(self, wx.ID_ANY, "EEPROM Panel",
                wx.DefaultPosition, wx.DefaultSize, 0)

        boxSizer.Add(self.m_button2, 0, wx.ALL, 5)
        boxSizer.Add(self.m_button3, 0, wx.ALL, 5)

        # connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.changeIntroPanel)
        self.m_button3.Bind(wx.EVT_BUTTON, self.changeIntroPanel)

        mainSizer.Add(boxSizer, 0, wx.ALL, 5)

        # add figure
        self.figure1 = plt.figure(1, dpi=60)
        self.axes1 = self.figure1.add_subplot(111)
        self.canvas1 = FigureCanvas(self, -1, self.figure1)
        self.figure2 = plt.figure(2, dpi=60)
        self.axes2 = self.figure2.add_subplot(111)
        self.canvas2 = FigureCanvas(self, -1, self.figure2)

        hSizer.Add(self.canvas1, 0, wx.EXPAND, 5)
        hSizer.AddSpacer(10)
        hSizer.Add(self.canvas2, 0, wx.EXPAND, 5)

        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        self.SetSizerAndFit(mainSizer)

    def __del__(self):
        pass

    # virtual event handlers, overide them in your derived class
    def changeIntroPanel(self, event):
        event.Skip()


## Define control panel here
class control_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        ## Define buttons for panel switching
        self.m_button2 = wx.Button(self, wx.ID_ANY, "Display Panel",
                wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3 = wx.Button(self, wx.ID_ANY, "EEPROM Panel",
                wx.DefaultPosition, wx.DefaultSize, 0)

        # a save button
        self.button = wx.Button(self, label="Save")

        # bk precision PS Label
        self.quote1 = wx.StaticText(self, label="BK Precision")

        # bk Status
        self.lblname1 = wx.StaticText(self, label='Status')
        self.lblname1r = wx.StaticText(self, label='OFF')
        self.lblname1w = wx.StaticText(self, label="")
        self.lblname1s = wx.Button(self, label="Turn ON")

        # bk V[V]
        self.lblname2 = wx.StaticText(self, label='V [V]')
        self.lblname2r = wx.StaticText(self, label='0.00')
        self.lblname2w = wx.SpinCtrlDouble(
                self, value='0.00', name="Roll V [V]")
        self.lblname2s = wx.Button(self, label="Set V")

        # bk I[A]
        self.lblname3 = wx.StaticText(self, label='I [mA]')
        self.lblname3r = wx.StaticText(self, label='0.00')
        self.lblname3w = wx.SpinCtrl(self, value='5.00', name="Roll I [mA]")
        self.lblname3s = wx.Button(self, label="Set I")

        # sipm Board Label
        self.quote2 = wx.StaticText(self, label="SiPM Board")

        # sipm #
        self.lblname4 = wx.StaticText(self, label="SiPM#")
        self.lblname4r = wx.StaticText(self, label="1")
        self.lblname4w = wx.SpinCtrl(self, value='1', name="Roll SiPM#")
        self.lblname4s = wx.Button(self, label="Set SiPM#")

        # T [C]
        self.lblname5 = wx.StaticText(self, label='T [' + u'\u2103]')
        self.lblname5r = wx.StaticText(self, label="25.00")
        self.lblname5w = wx.StaticText(self, label="")

        # gain [dB]
        self.lblname6 = wx.StaticText(self, label='Gain [dB]')
        self.lblname6r = wx.StaticText(self, label="10")
        self.lblname6w = wx.SpinCtrl(self, value='10', name="Roll Gain [dB]")
        self.lblname6s = wx.Button(self, label="Set Gain")

        # led Board Label
        self.quote3 = wx.StaticText(self, label="LED Board")

        # led #
        self.lblname7 = wx.StaticText(self, label="LED#")
        self.lblname7r = wx.StaticText(self, label="1")
        self.lblname7w = wx.SpinCtrl(self, value='1', name="Roll LED#")
        self.lblname7s = wx.Button(self, label="Set LED#")

        # end of grid1

        # bk precision PS Label
        self.quote4 = wx.StaticText(self, label="BK Precision")

        self.button1 = wx.Button(self, label="OFF")
        self.button2 = wx.Button(self, label="ON")
        self.button3 = wx.Button(self, label="Update")
        self.button4 = wx.Button(self, label="OFF")

        # sipm Board Label
        self.quote5 = wx.StaticText(self, label="SiPM Board")
        self.button5 = wx.Button(self, label="Gain10")
        self.button6 = wx.Button(self, label="Gain16")
        self.button7 = wx.Button(self, label="Gain20")
        self.button8 = wx.Button(self, label="Gain26")

        # led Board Label
        self.quote6 = wx.StaticText(self, label="LED Board")
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

        # a multiline TextCtrl for logging purpose
        self.logger = wx.TextCtrl(
                self, size=(400, 600), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.BORDER_SUNKEN)

        ## implement the settings in 3 other functions
        self.__set_properties()
        self.__do_layout()
        self.__do_binding()

    def __set_properties(self):

        # set the properties of the items created
        self.logger.SetBackgroundColour("Black")
        self.logger.SetForegroundColour("White")

        self.lblname2w.SetDigits(1)
        self.lblname2w.SetRange(0.0, 70.0)
        self.lblname2w.SetIncrement(0.1)

        self.lblname3w.SetRange(0, 5)
        self.lblname4w.SetRange(1, 1500)
        self.lblname6w.SetRange(6, 26)
        self.lblname7w.SetRange(1, 16)

        font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        bigfont = wx.Font(
                20, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.quote1.SetFont(bigfont)
        self.quote2.SetFont(bigfont)
        self.quote3.SetFont(bigfont)
        self.quote4.SetFont(bigfont)
        self.quote5.SetFont(bigfont)
        self.quote6.SetFont(bigfont)

        self.lblname1.SetFont(font)
        self.lblname1r.SetFont(font)
        self.lblname1w.SetFont(font)
        self.lblname1s.SetFont(font)

        self.lblname2.SetFont(font)
        self.lblname2r.SetFont(font)
        self.lblname2w.SetFont(font)
        self.lblname2s.SetFont(font)

        self.lblname3.SetFont(font)
        self.lblname3r.SetFont(font)
        self.lblname3w.SetFont(font)
        self.lblname3s.SetFont(font)

        self.lblname4.SetFont(font)
        self.lblname4r.SetFont(font)
        self.lblname4w.SetFont(font)
        self.lblname4s.SetFont(font)

        self.lblname5.SetFont(font)
        self.lblname5r.SetFont(font)
        self.lblname5w.SetFont(font)

        self.lblname6.SetFont(font)
        self.lblname6r.SetFont(font)
        self.lblname6w.SetFont(font)
        self.lblname6s.SetFont(font)

        self.lblname7.SetFont(font)
        self.lblname7r.SetFont(font)
        self.lblname7w.SetFont(font)
        self.lblname7s.SetFont(font)

        self.button1.SetFont(font)
        self.button2.SetFont(font)
        self.button3.SetFont(font)
        self.button4.SetFont(font)

        self.button5.SetFont(font)
        self.button6.SetFont(font)
        self.button7.SetFont(font)
        self.button8.SetFont(font)

        self.led1.SetFont(font)
        self.led2.SetFont(font)
        self.led3.SetFont(font)
        self.led4.SetFont(font)

        self.led5.SetFont(font)
        self.led6.SetFont(font)
        self.led7.SetFont(font)
        self.led8.SetFont(font)

        self.led9.SetFont(font)
        self.led10.SetFont(font)
        self.led11.SetFont(font)
        self.led12.SetFont(font)

        self.led13.SetFont(font)
        self.led14.SetFont(font)
        self.led15.SetFont(font)
        self.led16.SetFont(font)

    def __do_layout(self):

        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=10, vgap=10)
        grid2 = wx.GridBagSizer(hgap=10, vgap=10)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)

        boxSizer.Add(self.m_button2, 0, wx.ALL, 5)
        boxSizer.Add(self.m_button3, 0, wx.ALL, 5)

        mainSizer.Add(boxSizer, 0, wx.ALL, 5)

        # start of grid1
        grid.Add(self.quote1, pos=(0, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lblname1, pos=(1, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname1r, pos=(1, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname1w, pos=(1, 2), flag=wx.TE_CENTER)
        grid.Add(self.lblname1s, pos=(1, 3), flag=wx.TE_CENTER | wx.EXPAND)

        grid.Add(self.lblname2, pos=(2, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname2r, pos=(2, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname2w, pos=(2, 2), flag=wx.TE_CENTER)
        grid.Add(self.lblname2s, pos=(2, 3), flag=wx.TE_CENTER)

        grid.Add(self.lblname3, pos=(3, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname3r, pos=(3, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname3w, pos=(3, 2), flag=wx.TE_CENTER)
        grid.Add(self.lblname3s, pos=(3, 3), flag=wx.TE_CENTER)

        grid.Add(self.quote2, pos=(4, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lblname4, pos=(5, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname4r, pos=(5, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname4w, pos=(5, 2), flag=wx.TE_CENTER)
        grid.Add(self.lblname4s, pos=(5, 3), flag=wx.TE_CENTER)

        grid.Add(self.lblname5, pos=(6, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname5r, pos=(6, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname5w, pos=(6, 2), flag=wx.TE_CENTER)

        grid.Add(self.lblname6, pos=(7, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname6r, pos=(7, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname6w, pos=(7, 2), flag=wx.TE_CENTER)
        grid.Add(self.lblname6s, pos=(7, 3), flag=wx.TE_CENTER)

        grid.Add(self.quote3, pos=(8, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid.Add(self.lblname7, pos=(9, 0), flag=wx.TE_RIGHT | wx.ALIGN_CENTER)
        grid.Add(
                self.lblname7r, pos=(9, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid.Add(self.lblname7w, pos=(9, 2), flag=wx.TE_CENTER)
        grid.Add(self.lblname7s, pos=(9, 3), flag=wx.TE_CENTER)
        # end of grid1

        # start of grid2
        grid2.Add(self.quote4, pos=(0, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid2.Add(self.button1, pos=(1, 0), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid2.Add(self.button2, pos=(1, 1), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid2.Add(self.button3, pos=(1, 2), flag=wx.TE_CENTER | wx.ALIGN_CENTER)
        grid2.Add(self.button4, pos=(1, 3), flag=wx.TE_CENTER | wx.ALIGN_CENTER)

        grid2.Add(self.quote5, pos=(2, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid2.Add(self.button5, pos=(3, 0), flag=wx.TE_CENTER)
        grid2.Add(self.button6, pos=(3, 1), flag=wx.TE_CENTER)
        grid2.Add(self.button7, pos=(3, 2), flag=wx.TE_CENTER)
        grid2.Add(self.button8, pos=(3, 3), flag=wx.TE_CENTER)

        grid2.Add(self.quote6, pos=(4, 1), span=(1, 2), flag=wx.TE_CENTER)

        grid2.Add(self.led1, pos=(5, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led2, pos=(5, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led3, pos=(5, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led4, pos=(5, 3), flag=wx.TE_CENTER)
        grid2.Add(self.led5, pos=(6, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led6, pos=(6, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led7, pos=(6, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led8, pos=(6, 3), flag=wx.TE_CENTER)
        grid2.Add(self.led9, pos=(7, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led10, pos=(7, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led11, pos=(7, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led12, pos=(7, 3), flag=wx.TE_CENTER)
        grid2.Add(self.led13, pos=(8, 0), flag=wx.TE_CENTER)
        grid2.Add(self.led14, pos=(8, 1), flag=wx.TE_CENTER)
        grid2.Add(self.led15, pos=(8, 2), flag=wx.TE_CENTER)
        grid2.Add(self.led16, pos=(8, 3), flag=wx.TE_CENTER)
        # end of grid2

        hSizer.Add(grid, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)
        hSizer.Add(grid2, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)
        hSizer.Add(self.logger, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)
        mainSizer.Add(hSizer, 0, wx.ALL, 10)
        mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def __do_binding(self):

        # do all the event binding here
        self.Bind(wx.EVT_BUTTON, self.changeIntroPanel, self.m_button2)
        self.Bind(wx.EVT_BUTTON, self.changeIntroPanel, self.m_button3)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.EvtSpinText, self.lblname2w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.lblname3w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.lblname4w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.lblname6w)
        self.Bind(wx.EVT_SPINCTRL, self.EvtSpinText, self.lblname7w)

        self.Bind(wx.EVT_BUTTON, self.OnSwitch, self.lblname1s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.lblname2s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.lblname3s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.lblname4s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.lblname6s)
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.lblname7s)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button4)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button5)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button6)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button7)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button8)

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led1)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led2)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led3)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led4)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led5)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led6)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led7)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led8)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led9)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led10)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led11)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led12)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led13)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led14)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led15)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.led16)

    def get_time(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
        event.Skip()

    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
        event.Skip()

    def OnSwitch(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.logger.AppendText("[%s] Clicked on %s\n" % (self.get_time(), labeltext))
        if labeltext == 'Turn ON':
            self.lblname1r.SetLabel('ON')
            self.lblname1s.SetLabel('Turn OFF')
        if labeltext == 'Turn OFF':
            self.lblname1r.SetLabel('OFF')
            self.lblname1s.SetLabel('Turn ON')
        event.Skip()

    def OnClick(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        self.logger.AppendText("[%s] Clicked on %s\n" % (self.get_time(), labeltext))
        event.Skip()

    def OnSet(self, event):
        labeltext = event.GetEventObject().GetLabelText()
        if labeltext == 'Set V':
            value = self.lblname2w.GetValue()
            unit = 'V'
        elif labeltext == 'Set I':
            value = self.lblname3w.GetValue()
            unit = 'mA'
        elif labeltext == 'Set SiPM#':
            value = self.lblname4w.GetValue()
            unit = ''
        elif labeltext == 'Set Gain':
            value = self.lblname6w.GetValue()
            unit = 'dB'
        elif labeltext == 'Set LED#':
            value = self.lblname7w.GetValue()
            unit = ''
        self.logger.AppendText("[%s] %s to %.1f %s\n" % (self.get_time(), labeltext, value, unit))
        event.Skip()

    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
        event.Skip()

    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
        event.Skip()

    def EvtSpinText(self, event):
        self.logger.AppendText(
                '[%s] %s to %.1f\n' % (self.get_time(), event.GetEventObject().GetName(),event.GetValue()))
        event.Skip()

    def __del__(self):
        pass

    # virtual event handlers, overide them in your derived class
    def changeIntroPanel(self, event):
        event.Skip()

## define EEPROM Panel here
class eeprom_panel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.m_button2 = wx.Button(self, wx.ID_ANY, "Control Panel",
                wx.DefaultPosition, wx.DefaultSize, 0)

        self.m_button3 = wx.Button(self, wx.ID_ANY, "Display Panel",
                wx.DefaultPosition, wx.DefaultSize, 0)

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

        self.mem1r = wx.StaticText(self, label='UWSiPM 1000 UWSiPM')
        self.mem2r = wx.StaticText(self, label='UWSiPM 2000 UWSiPM')
        self.mem3r = wx.StaticText(self, label='UWSiPM 3000 UWSiPM')
        self.mem4r = wx.StaticText(self, label='UWSiPM 4000 UWSiPM')
        self.mem5r = wx.StaticText(self, label='UWSiPM 5000 UWSiPM')
        self.mem6r = wx.StaticText(self, label='UWSiPM 6000 UWSiPM')
        self.mem7r = wx.StaticText(self, label='UWSiPM 7000 UWSiPM')
        self.mem8r = wx.StaticText(self, label='UWSiPM 8000 UWSiPM')

        self.mem1w = wx.TextCtrl(self, value='UWSiPM 1000 UWSiPM', size=(280, 40))
        self.mem2w = wx.TextCtrl(self, value='UWSiPM 2000 UWSiPM')
        self.mem3w = wx.TextCtrl(self, value='UWSiPM 3000 UWSiPM')
        self.mem4w = wx.TextCtrl(self, value='UWSiPM 4000 UWSiPM')
        self.mem5w = wx.TextCtrl(self, value='UWSiPM 5000 UWSiPM')
        self.mem6w = wx.TextCtrl(self, value='UWSiPM 6000 UWSiPM')
        self.mem7w = wx.TextCtrl(self, value='UWSiPM 7000 UWSiPM')
        self.mem8w = wx.TextCtrl(self, value='UWSiPM 8000 UWSiPM')

        self.mem1s = wx.Button(self, label="Set Page1")
        self.mem2s = wx.Button(self, label="Set Page2")
        self.mem3s = wx.Button(self, label="Set Page3")
        self.mem4s = wx.Button(self, label="Set Page4")
        self.mem5s = wx.Button(self, label="Set Page5")
        self.mem6s = wx.Button(self, label="Set Page6")
        self.mem7s = wx.Button(self, label="Set Page7")
        self.mem8s = wx.Button(self, label="Set Page8")

        ## implement the settings in 3 other functions
        self.__set_properties()
        self.__do_layout()
        self.__do_binding()

    def __set_properties(self):

        self.SetBackgroundColour("Silver")
        font = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        bigfont = wx.Font(
                20, wx.ROMAN, wx.NORMAL, wx.NORMAL, False, u'Consolas')

        self.quote1.SetFont(bigfont)

        self.mem1.SetFont(font)
        self.mem1r.SetFont(font)
        self.mem1w.SetFont(font)
        self.mem1s.SetFont(font)

        self.mem2.SetFont(font)
        self.mem2r.SetFont(font)
        self.mem2w.SetFont(font)
        self.mem2s.SetFont(font)

        self.mem3.SetFont(font)
        self.mem3r.SetFont(font)
        self.mem3w.SetFont(font)
        self.mem3s.SetFont(font)

        self.mem4.SetFont(font)
        self.mem4r.SetFont(font)
        self.mem4w.SetFont(font)
        self.mem4s.SetFont(font)

        self.mem5.SetFont(font)
        self.mem5r.SetFont(font)
        self.mem5w.SetFont(font)
        self.mem5s.SetFont(font)

        self.mem6.SetFont(font)
        self.mem6r.SetFont(font)
        self.mem6w.SetFont(font)
        self.mem6s.SetFont(font)

        self.mem7.SetFont(font)
        self.mem7r.SetFont(font)
        self.mem7w.SetFont(font)
        self.mem7s.SetFont(font)

        self.mem8.SetFont(font)
        self.mem8r.SetFont(font)
        self.mem8w.SetFont(font)
        self.mem8s.SetFont(font)


    def __do_layout(self):

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=20, vgap=20)
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)

        boxSizer.Add(self.m_button2, 0, wx.ALL, 5)
        boxSizer.Add(self.m_button3, 0, wx.ALL, 5)

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

        mainSizer.Add(boxSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.quote1, 0, flag=wx.TE_CENTER)
        mainSizer.Add(grid, 0, wx.ALL | wx.EXPAND | wx.CENTER, 10)

        self.SetSizerAndFit(mainSizer)

    def __do_binding(self):
        # connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.changeIntroPanel)
        self.m_button3.Bind(wx.EVT_BUTTON, self.changeIntroPanel)

    def __del__(self):
        pass
    # virtual event handlers, overide them in your derived class

    def changeIntroPanel(self, event):
        event.Skip()


#!/usr/local/bin/python3.5

# gui.py

import wx
from numpy import arange, sin, pi
import numpy as np
import matplotlib.pyplot as plt
#from numpy.random import normal
#gaussian_numbers = normal(size=1000)
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


class MainFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( bSizer1 )
        self.Layout()

        # self.panelOne = panel_one(self)
        # self.panelTwo = panel_two(self)
        # self.panelTwo.Hide()
        self.Centre( wx.BOTH )
    def __del__( self ):
        pass

class panel_waveform ( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 400,300 ), style = wx.TAB_TRAVERSAL )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        ## Add figure
        self.figure1 = plt.figure(1, dpi=60)
        self.axes1 = self.figure1.add_subplot(111)
        self.canvas1 = FigureCanvas(self, -1, self.figure1)
        bSizer1.Add(self.canvas1, 0, wx.EXPAND)

class panel_histogram ( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 400,300 ), style = wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        ## Add figure
        self.figure2 = plt.figure(2, dpi=60)
        self.axes2 = self.figure2.add_subplot(111)
        self.canvas2 = FigureCanvas(self, -1, self.figure2)
        bSizer2.Add(self.canvas2, 0, wx.EXPAND)

class panel_one ( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        # create a button to switch to 2nd panel
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"panel 1 button", wx.DefaultPosition, wx.DefaultSize, 0 )

        # Connect the button to the event to switch to 2nd panel
        self.m_button2.Bind( wx.EVT_BUTTON, self.changeIntroPanel )

        ## Add variable labels
        self.label1 = wx.StaticText(self, -1, 'BK_V [V]',  style=wx.TE_RIGHT, size=(250,40))
        self.label2 = wx.StaticText(self, -1, 'BK_I [A]',  style=wx.TE_RIGHT, size=(250,40))
        self.label3 = wx.StaticText(self, -1, 'Gain [dB]',  style=wx.TE_RIGHT, size=(250,40))
        self.label4 = wx.StaticText(self, -1, 'T [' + u'\u2103]',  style=wx.TE_RIGHT, size=(250,40))
        self.label5 = wx.StaticText(self, -1, 'SiPM #',  style=wx.TE_RIGHT, size=(250,40))
        self.label6 = wx.StaticText(self, -1, 'LED #',  style=wx.TE_RIGHT, size=(250,40))
        self.label7 = wx.StaticText(self, -1, 'V_amp [mV]',  style=wx.TE_RIGHT, size=(250,40))

        ## Add variable value boxes
        self.display1 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))
        self.display2 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))
        self.display3 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))
        self.display4 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))
        self.display5 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))
        self.display6 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))
        self.display7 = wx.TextCtrl(self, -1, '',  style=wx.TE_CENTER, size=(150,40))

        ## Set font style and size for the text in the display box
        font_style = wx.Font(25, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.label1.SetFont(font_style)
        self.label2.SetFont(font_style)
        self.label3.SetFont(font_style)
        self.label4.SetFont(font_style)
        self.label5.SetFont(font_style)
        self.label6.SetFont(font_style)
        self.label7.SetFont(font_style)
        self.display1.SetFont(font_style)
        self.display2.SetFont(font_style)
        self.display3.SetFont(font_style)
        self.display4.SetFont(font_style)
        self.display5.SetFont(font_style)
        self.display6.SetFont(font_style)
        self.display7.SetFont(font_style)

        self.display4.AppendText('0')

        gsdisplay = wx.GridSizer(7, 2, 5, 5)
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
            (self.display7, 0, wx.CENTER | wx.TOP | wx.BOTTOM)])

        gs = wx.GridSizer(2,1,5,5)
        gs.AddMany([ (self.m_button2, 0, wx.CENTER), (gsdisplay, 1, wx.ALIGN_CENTER)])

        bSizer5.Add(gs, 1, wx.ALIGN_CENTER)

        self.SetSizer(bSizer5)
        self.Layout()

    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def changeIntroPanel( self, event ):
        event.Skip()

class panel_two ( wx.Panel ):
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"panel 2 button ", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button2, 0, wx.ALL, 5 )
        self.SetSizer( bSizer5 )
        self.Layout()
        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.changeIntroPanel )

    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def changeIntroPanel( self, event ):
        event.Skip()

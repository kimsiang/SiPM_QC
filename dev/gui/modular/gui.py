#!/usr/local/bin/python3.5

# gui.py

import wx
from numpy import arange, sin, pi
import numpy as np


class MainFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title =
                wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(
                    1000,750 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
#        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
#        bSizer1 = wx.BoxSizer( wx.VERTICAL )
#        self.SetSizer( bSizer1 )
#        self.Layout()

 #       splitter = wx.SplitterWindow(self)
 #       leftP = panel_waveform(splitter)
 #       rightP = panel_histogram(splitter)

        # split the window
  #      splitter.SplitVertically(leftP, rightP)
  #      splitter.SetMinimumPaneSize(20)

        # self.panelOne = panel_one(self)
        # self.panelTwo = panel_two(self)
        # self.panelTwo.Hide()
#        self.Centre( wx.BOTH )
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
        #bSizer5 = wx.BoxSizer( wx.VERTICAL )

        # create a button to switch to 2nd panel
        #self.m_button2 = wx.Button( self, wx.ID_ANY, u"panel 1 button", wx.DefaultPosition, wx.DefaultSize, 0 )

        # Connect the button to the event to switch to 2nd panel
        #self.m_button2.Bind( wx.EVT_BUTTON, self.changeIntroPanel )

        self.label1 = wx.StaticText(self, wx.ID_ANY, 'Display',
                style=wx.TE_CENTER)
        self.label2 = wx.StaticText(self, wx.ID_ANY, 'BK Precision',
                style=wx.TE_CENTER)
        self.label3_1 = wx.StaticText(self, wx.ID_ANY, 'Vread [V]',
                style=wx.TE_CENTER)
        self.label3_2 = wx.StaticText(self, wx.ID_ANY, 'Vset [V]',
                style=wx.TE_CENTER)
        self.label3_3 = wx.StaticText(self, wx.ID_ANY, 'Iread [A]',
                style=wx.TE_CENTER)
        self.label3_4 = wx.StaticText(self, wx.ID_ANY, 'Iset [A]',
                style=wx.TE_CENTER)
        self.label4_1 = wx.StaticText(self, wx.ID_ANY, 'v_read',
                style=wx.TE_CENTER)
        self.label4_2 = wx.TextCtrl(self, wx.ID_ANY, 'v_set',
                style=wx.TE_CENTER)
        self.label4_3 = wx.StaticText(self, wx.ID_ANY, 'i_read',
                style=wx.TE_CENTER)
        self.label4_4 = wx.StaticText(self, wx.ID_ANY, 'i_set',
                style=wx.TE_CENTER)
        self.label5 = wx.StaticText(self, wx.ID_ANY, 'SiPM Board',
                style=wx.TE_CENTER)
        self.label6_1 = wx.StaticText(self, wx.ID_ANY, 'SiPM# (Read)',
                style=wx.TE_CENTER)
        self.label6_2 = wx.TextCtrl(self, wx.ID_ANY, 'SiPM# (Write)',
                style=wx.TE_CENTER)
        self.label6_3 = wx.StaticText(self, wx.ID_ANY, 'Gain (read)',
                style=wx.TE_CENTER)
        self.label6_4 = wx.StaticText(self, wx.ID_ANY, 'Gain (write)',
                style=wx.TE_CENTER)
        self.label7_1 = wx.StaticText(self, wx.ID_ANY, 'sipm_read',
                style=wx.TE_CENTER)
        self.label7_2 = wx.TextCtrl(self, wx.ID_ANY, 'sipm_write',
                style=wx.TE_CENTER)
        self.label7_3 = wx.StaticText(self, wx.ID_ANY, 'gain_read',
                style=wx.TE_CENTER)
        self.label7_4 = wx.TextCtrl(self, wx.ID_ANY, 'gain_write',
                style=wx.TE_CENTER)
        self.label8_1 = wx.StaticText(self, wx.ID_ANY, 'T [C]',
                style=wx.TE_CENTER)
        self.label8_2 = wx.StaticText(self, wx.ID_ANY, 'EEPROM_1',
                style=wx.TE_CENTER)
        self.label8_3 = wx.StaticText(self, wx.ID_ANY, 'EEPROM_2',
                style=wx.TE_CENTER)
        self.label8_4 = wx.StaticText(self, wx.ID_ANY, 'EEPROM_3',
                style=wx.TE_CENTER)
        self.label9_1 = wx.StaticText(self, wx.ID_ANY, 'T [C]',
                style=wx.TE_CENTER)
        self.label9_2 = wx.StaticText(self, wx.ID_ANY, 'EEPROM_1',
                style=wx.TE_CENTER)
        self.label9_3 = wx.StaticText(self, wx.ID_ANY, 'EEPROM_2',
                style=wx.TE_CENTER)
        self.label9_4 = wx.StaticText(self, wx.ID_ANY, 'EEPROM_3',
                style=wx.TE_CENTER)
        self.label10 = wx.StaticText(self, wx.ID_ANY, 'LED Board',
                style=wx.TE_CENTER)
        self.label11_1 = wx.StaticText(self, wx.ID_ANY, 'LED#',
                style=wx.TE_CENTER)
        self.label12_1 = wx.StaticText(self, wx.ID_ANY, '16',
                style=wx.TE_CENTER)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        # begin wxGlade: MyPanel.__set_properties
        self.SetSize((500, 600))
        self.label1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        #self.label1.SetMinSize((100, 50))

    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        sizer = wx.BoxSizer(wx.VERTICAL)

        gs3 = wx.BoxSizer(wx.HORIZONTAL)
        gs3.AddMany([
            (self.label3_1, 0, wx.CENTER),
            (self.label3_2, 0, wx.CENTER),
            (self.label3_3, 0, wx.CENTER),
            (self.label3_4, 0, wx.CENTER)])

        gs4 = wx.BoxSizer(wx.HORIZONTAL)
        gs4.AddMany([
            (self.label4_1, 0, wx.CENTER),
            (self.label4_2, 0, wx.CENTER),
            (self.label4_3, 0, wx.CENTER),
            (self.label4_4, 0, wx.CENTER)])

        gs6 = wx.BoxSizer(wx.HORIZONTAL)
        gs6.AddMany([
            (self.label6_1, 0, wx.CENTER),
            (self.label6_2, 0, wx.CENTER),
            (self.label6_3, 0, wx.CENTER),
            (self.label6_4, 0, wx.CENTER)])

        gs7 = wx.BoxSizer(wx.HORIZONTAL)
        gs7.AddMany([
            (self.label7_1, 0, wx.CENTER),
            (self.label7_2, 0, wx.CENTER),
            (self.label7_3, 0, wx.CENTER),
            (self.label7_4, 0, wx.CENTER)])

        gs8 = wx.BoxSizer(wx.HORIZONTAL)
        gs8.AddMany([
            (self.label8_1, 0, wx.CENTER),
            (self.label8_2, 0, wx.CENTER),
            (self.label8_3, 0, wx.CENTER),
            (self.label8_4, 0, wx.CENTER)])

        gs9 = wx.BoxSizer(wx.HORIZONTAL)
        gs9.AddMany([
            (self.label9_1, 0, wx.CENTER),
            (self.label9_2, 0, wx.CENTER),
            (self.label9_3, 0, wx.CENTER),
            (self.label9_4, 0, wx.CENTER)])

        gs11 = wx.GridSizer(1, 4, 5, 5)
        gs11.AddMany([
            (self.label11_1, 0, wx.CENTER)])

        gs12 = wx.GridSizer(1, 4, 5, 5)
        gs12.AddMany([
            (self.label12_1, 0, wx.CENTER)])

        sizer.Add(self.label1, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(self.label2, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs3, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs4, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(self.label5, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs6, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs7, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs8, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs9, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(self.label10, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs11, 1, wx.ALIGN_CENTER, 1)
        sizer.Add(gs12, 1, wx.ALIGN_CENTER, 1)

        self.SetSizer(sizer)
        self.Centre()
        self.Layout()
        # end wxGlade


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

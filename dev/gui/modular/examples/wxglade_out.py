#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.1 on Thu Feb 18 14:47:51 2016
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.Display = wx.StaticText(self, wx.ID_ANY, _("Display"), style=wx.ALIGN_CENTER)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("BK Precision"), style=wx.ALIGN_CENTER)
        self.label_2 = wx.StaticText(self, wx.ID_ANY, _("Vread [V]"), style=wx.ALIGN_CENTER)
        self.label_3 = wx.StaticText(self, wx.ID_ANY, _("Vset [V]"), style=wx.ALIGN_CENTER)
        self.label_4 = wx.StaticText(self, wx.ID_ANY, _("label_4"))
        self.label_5 = wx.StaticText(self, wx.ID_ANY, _("label_5"))
        self.label_6 = wx.StaticText(self, wx.ID_ANY, _("label_6"))
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_7 = wx.StaticText(self, wx.ID_ANY, _("label_7"))
        self.label_8 = wx.StaticText(self, wx.ID_ANY, _("label_8"))
        self.label_9 = wx.StaticText(self, wx.ID_ANY, _("SiPM Board"), style=wx.ALIGN_CENTER)
        self.label_10 = wx.StaticText(self, wx.ID_ANY, _("SiPM #"))
        self.label_11 = wx.StaticText(self, wx.ID_ANY, _("label_11"))
        self.label_12 = wx.StaticText(self, wx.ID_ANY, _("Gain (read)"))
        self.label_13 = wx.StaticText(self, wx.ID_ANY, _("Gain (write)"))
        self.label_14 = wx.StaticText(self, wx.ID_ANY, _("label_14"))
        self.text_ctrl_2 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_15 = wx.StaticText(self, wx.ID_ANY, _("label_15"))
        self.text_ctrl_3 = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_16 = wx.StaticText(self, wx.ID_ANY, _("T [C]"), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.label_17 = wx.StaticText(self, wx.ID_ANY, _("EEPROM_1"), style=wx.ALIGN_CENTER)
        self.label_18 = wx.StaticText(self, wx.ID_ANY, _("EEPROM_2"))
        self.label_19 = wx.StaticText(self, wx.ID_ANY, _("EEPROM_3"))
        self.label_20 = wx.StaticText(self, wx.ID_ANY, _("LED Board"))
        self.label_21 = wx.StaticText(self, wx.ID_ANY, _("LED#"), style=wx.ALIGN_CENTER_HORIZONTAL)
        self.label_22 = wx.StaticText(self, wx.ID_ANY, _("16"), style=wx.ALIGN_CENTER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyPanel.__set_properties
        self.SetSize((402, 602))
        self.Display.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu"))
        self.label_2.SetMinSize((100, 50))
        self.label_6.SetMinSize((100, 50))
        self.label_14.SetMinSize((100, 50))
        self.text_ctrl_2.SetMinSize((100, 50))
        self.label_15.SetMinSize((100, 50))
        self.text_ctrl_3.SetMinSize((100, 50))
        self.label_16.SetMinSize((100, 50))
        self.label_17.SetMinSize((100, 50))
        self.label_21.SetMinSize((100, 50))
        self.label_22.SetMinSize((100, 50))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.Display, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.label_2, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.label_3, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.label_4, 0, wx.ALIGN_CENTER, 0)
        sizer_2.Add(self.label_5, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(sizer_2, 1, wx.ALL | wx.EXPAND, 1)
        sizer_3.Add(self.label_6, 0, 0, 0)
        sizer_3.Add(self.text_ctrl_1, 0, 0, 0)
        sizer_3.Add(self.label_7, 0, 0, 0)
        sizer_3.Add(self.label_8, 0, 0, 0)
        sizer_1.Add(sizer_3, 1, 0, 0)
        sizer_1.Add(self.label_9, 0, wx.ALIGN_CENTER, 0)
        sizer_4.Add(self.label_10, 0, 0, 0)
        sizer_4.Add(self.label_11, 0, 0, 0)
        sizer_4.Add(self.label_12, 0, 0, 0)
        sizer_4.Add(self.label_13, 0, 0, 0)
        sizer_1.Add(sizer_4, 1, 0, 0)
        sizer_5.Add(self.label_14, 0, 0, 0)
        sizer_5.Add(self.text_ctrl_2, 0, 0, 0)
        sizer_5.Add(self.label_15, 0, 0, 0)
        sizer_5.Add(self.text_ctrl_3, 0, 0, 0)
        sizer_1.Add(sizer_5, 1, 0, 0)
        sizer_6.Add(self.label_16, 0, wx.ALIGN_CENTER, 4)
        sizer_6.Add(self.label_17, 0, wx.ALIGN_CENTER, 0)
        sizer_6.Add(self.label_18, 0, wx.ALIGN_CENTER, 0)
        sizer_6.Add(self.label_19, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(sizer_6, 1, 0, 0)
        sizer_1.Add(self.label_20, 0, wx.ALIGN_CENTER, 0)
        sizer_7.Add(self.label_21, 0, wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_1.Add(sizer_7, 1, 0, 0)
        sizer_8.Add(self.label_22, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(sizer_8, 1, 0, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class MyPanel

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("frame_1"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_9)
        sizer_9.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame
class MyApp(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
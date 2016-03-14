import settings
import wx
import wx.lib.agw.flatnotebook as fnb
from threading import Thread, Event
from sipm_qc_gui import control_panel, display_panel, eeprom_panel, logger_panel
import time, sys, subprocess, os, threading, signal
from datetime import date, datetime, tzinfo, timedelta
import zmq
from multiprocessing import Process

class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=wx.EmptyString,
                          pos=wx.DefaultPosition,
                          size=wx.Size(1000, 700),
                          style=wx.DEFAULT_FRAME_STYLE |
                          wx.TAB_TRAVERSAL)


        self.display = display_panel(self)
        self.display.Layout()

    def __del__(self):
        pass


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        t1=Thread(target=self.update_frame,args=())
        t1.start()

        return True

    def update_frame(self):
        while True:
            wx.CallAfter(self.frame.display.plot_temp,'./data/log/slowctrl2.log')
            time.sleep(5)

# ----- Main program -------

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()


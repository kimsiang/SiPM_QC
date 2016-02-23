import


class MainFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          title=wx.EmptyString,
                          pos=wx.DefaultPosition,
                          size=wx.Size(1350, 700),
                          style=wx.DEFAULT_FRAME_STYLE |
                          wx.TAB_TRAVERSAL)

        #self.panelOne = ControlPanel(self)
        #self.panelTwo = DisplayPanel(self)
        # self.panelTwo.Hide()
        self.Centre(wx.BOTH)

    def __del__(self):
        pass


class Panel1(control_panel):

    def __init__(self, parent):
        control_panel.__init__(self, parent)
        self.parent = parent
        self.parent.SetTitle("SiPM QC Station - L0 (Control Panel)")
        self.SetBackgroundColour('silver')

    def changeIntroPanel(self, event):
        if self.IsShown():
            self.parent.SetTitle("SiPM QC Station - L0 (Display Panel)")
            self.Hide()
            self.parent.panelTwo.Show()


class Panel2(display_panel):

    def __init__(self, parent):
        display_panel.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel(self, event):
        if self.IsShown():
            self.parent.SetTitle("SiPM QC Station - L0 (Control Panel)")
            self.parent.panelOne.Show()
            self.Hide()


class MainApp(MainFrame):

    def __init__(self, parent):
        MainFrame.__init__(self, parent)

        self.panelOne = Panel1(self)
        self.panelTwo = Panel2(self)
        self.panelTwo.Hide()


def main():
    app = wx.App()
    window = MainApp(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

import wx
import gui

class MainApp(gui.MainFrame):
    def __init__(self, parent):
        gui.MainFrame.__init__(self, parent)

        self.panelOne = Panel1(self)
        self.panelTwo = Panel2(self)
        self.panelTwo.Hide()

class Panel1(gui.panel_one):
    def __init__(self, parent):
        gui.panel_one.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel( self, event ):
        if self.IsShown():
            self.parent.SetTitle("Panel Two Showing")
            self.Hide()
            self.parent.panelTwo.Show()


class Panel2(gui.panel_two):
    def __init__(self, parent):
        gui.panel_two.__init__(self, parent)
        self.parent = parent

    def changeIntroPanel( self, event ):
        if self.IsShown():
            self.parent.SetTitle("Panel One Showing")
            self.parent.panelOne.Show()
            self.Hide()

def main():
    app = wx.App()
    window = MainApp(None)
    window.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()
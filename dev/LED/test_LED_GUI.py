import  wx

import u3
import time

d = u3.U3()

def led1():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,0))

def led2():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,0))

def led3():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,1))

def led4():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,1))

def led5():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,0))

def led6():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,0))

def led7():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,1))

def led8():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,1))

def led9():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,0))

def led10():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,0))

def led11():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,1))

def led12():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,1))

def led13():
	d.getFeedback(u3.BitStateWrite(10,0))
	d.getFeedback(u3.BitStateWrite(11,0))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,1))

def led14():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,0))

def led15():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,0))
	d.getFeedback(u3.BitStateWrite(13,1))

def led16():
	d.getFeedback(u3.BitStateWrite(10,1))
	d.getFeedback(u3.BitStateWrite(11,1))
	d.getFeedback(u3.BitStateWrite(12,1))
	d.getFeedback(u3.BitStateWrite(13,1))

 
class ExampleApp(wx.Frame):
    def __init__(self):
        # Every wx app must create one App object
        # before it does anything else using wx.
        self.app = wx.App()
 
        # Set up the main window
        wx.Frame.__init__(self,
                          parent=None,
                          title='wxPython Example',
                          size=(300, 200))
 
        # The greetings available
        #self.greetings = ['hello', 'goodbye', 'heyo']
        self.greetings = ['LED #1', 'LED #2', 'LED #3', 'LED #4', 'LED #5', 'LED #6', 'LED #7', 'LED #8', 'LED #9', 'LED #10', 'LED #11', 'LED #12', 'LED #13', 'LED #14', 'LED #15', ]
 
        # Layout panel and hbox
        self.panel = wx.Panel(self, size=(300, 200))
        self.box = wx.BoxSizer(wx.VERTICAL)
 
        # Greeting combobox
        self.greeting = wx.ComboBox(parent=self.panel,
                                    value='LED #1',
                                    size=(280, -1),
                                    choices=self.greetings)
 
        # Add the greeting combo to the hbox
        self.box.Add(self.greeting, 0, wx.TOP)
        self.box.Add((-1, 10))
 
        # Recipient entry
        self.recipient = wx.TextCtrl(parent=self.panel,
                                     size=(280, -1),
                                     value='world')
 
        # Add the greeting combo to the hbox
        self.box.Add(self.recipient, 0, wx.TOP)
 
        # Add padding to lower the button position
        self.box.Add((-1, 100))
 
        # The go button
        self.go_button = wx.Button(self.panel, 10, '&Go')
 
        # Bind an event for the button
        self.Bind(wx.EVT_BUTTON, self.print_result, self.go_button)
 
        # Make the button the default action for the form
        self.go_button.SetDefault()
 
        # Add the button to the hbox
        self.box.Add(self.go_button, 0, flag=wx.ALIGN_RIGHT|wx.BOTTOM)
 
        # Tell the panel to use the hbox
        self.panel.SetSizer(self.box)
 
#    def print_result(self, *args):
#        ''' Print a greeting constructed from
#            the selections made by the user. '''
#        print('%s, %s!' % (self.greeting.GetValue().title(),
#                           self.recipient.GetValue()))
    def print_result(self, *args):
	print self.greeting.GetValue().title()
        if self.greeting.GetValue().title()=='Led #1':
   	    	led1()
		print 'hello LED #1' 
        if self.greeting.GetValue().title()=='Led #2':
   	    	led2() 
        if self.greeting.GetValue().title()=='Led #3':
   	    	led3() 
        if self.greeting.GetValue().title()=='Led #4':
   	    	led4() 

    def run(self):
        ''' Run the app '''
        self.Show()
        self.app.MainLoop()
 
# Instantiate and run
app = ExampleApp()
app.run()

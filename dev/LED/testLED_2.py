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

led16()

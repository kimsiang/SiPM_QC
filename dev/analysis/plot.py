#! /usr/bin/python
import Gnuplot

g = Gnuplot.Gnuplot()
g.title('My Systems Plot')
g.xlabel('Date')
g.ylabel('Value')
g('set term png')
g('set out "output.png"')
#proc = open("response","r")
#databuff = Gnuplot.Data(proc.read(), title="test")

databuff = Gnuplot.File('../data/sipm_0007/sipm_0007_volt_31_00031_full.txt', using='1:2')
g.plot(databuff)


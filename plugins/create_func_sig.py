from idaapi import *
from graph import *
from signature import *

print "\n--------------------\ncreate_func_sig.py has been started"

sig = signature()
G = graph()		
		
ea = ScreenEA()
fc = FlowChart(get_func(ea))

sig.generate(fc, G)

sig.printSig()
		
print "create_func_sig.py has completed\n--------------------\n"
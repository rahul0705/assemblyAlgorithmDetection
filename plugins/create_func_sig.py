from idaapi import *
from graph import *
from signature import *

print "\n--------------------\ncreate_func_sig.py has been started"

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
sig = signature(fc, G)

#sig = signature(None, None)
#sig.load()
#sig.printSig()
#sig.save()
		
print "create_func_sig.py has completed\n--------------------\n"
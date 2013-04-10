from idaapi import *
from graph import *
from signature import *

print "\n--------------------\ncompare_func_sig.py has been started"

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
sig = signature(fc, G)

sigLoaded = signature(None, None)
sigLoaded.load()

similarity = sigLoaded.compare(sig)

print similarity
		
print "compare_func_sig.py has completed\n--------------------\n"
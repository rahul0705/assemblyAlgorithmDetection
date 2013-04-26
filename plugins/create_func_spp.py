from idaapi import *
from graph import *
from function import *

print "\n--------------------\ncreate_func_spp.py has been started"

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
func = function_block(fc, G)
func.printSPP()
func.save()
		
print "create_func_spp.py has completed\n--------------------\n"
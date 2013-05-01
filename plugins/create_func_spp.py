from idaapi import *
from graph import *
from function import *

OLDDIR = os.getcwd()
DIR = ".\\.."

print "\n--------------------\ncreate_func_spp.py has been started"
os.chdir(DIR)

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
func = function_block(fc, G)
func.printSPP()
func.save()
		
print "create_func_spp.py has completed\n--------------------\n"
os.chdir(OLDDIR)
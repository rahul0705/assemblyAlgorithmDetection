from idaapi import *
from graph import *
from signature import *

OLDDIR = os.getcwd()
DIR = ".\\.."

print "\n--------------------\ncreate_func_sig.py has been started"
os.chdir(DIR)

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
sig = signature(fc, G, False)
sig.printSig()
sig.save()
		
print "create_func_sig.py has completed\n--------------------\n"
os.chdir(OLDDIR)
from idaapi import *
from graph import *
from signature import *

threshold = 0.85;

print "\n--------------------\ncompare_func_sig.py has been started"

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
sig = signature(fc, G)

similarities = sig.compare()

similarities.sort()

print '_____Results ( Similarity > ' + str('%') + '%0.2f )_____' % (float(threshold * 100.0))

for item in similarities:
	if item.sim >= threshold:
		print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (item.alg, item.cmp, item.opt)
		print 'Similarity: %0.2f\n' % (float(item.sim))
		
print "compare_func_sig.py has completed\n--------------------\n"
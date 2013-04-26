from idaapi import *
from graph import *
from signature import *

print "\n--------------------\ncompare_func_sig.py has been started"

ea = ScreenEA()
fc = FlowChart(get_func(ea))

G = graph(fc)	
sig = signature(fc, G)

#sigLoaded = signature(None, None)
#sigLoaded.load("filename")

#sigLoaded.printSig()
#similarity = sigLoaded.compareLoaded(sig)

#print "\nSimilarity: %f\n" % (similarity)

similarities = sig.compare()

for result in similarities:
	print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (result[0], result[1], result[2])
	print 'Similarity with current function: %f\n' % (float(result[3]))
		
print "compare_func_sig.py has completed\n--------------------\n"
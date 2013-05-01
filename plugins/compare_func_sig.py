from idaapi import *
from graph import *
from signature import *

threshold = 0.85;

print "\n--------------------\ncompare_func_sig.py has been started\n"
ea = ScreenEA()

for function in Functions(SegStart(ea), SegEnd(ea)):
	func = get_func(function)
	fc = FlowChart(func)

	G = graph(fc)	
	sig = signature(fc, G, True)

	similarities = sig.compare()

	similarities.sort()

	print '_____Results of function at %x (Threshold = %0.2f)_____' % (func.startEA, float(threshold * 100.0))

	for item in similarities:
		if item.sim >= threshold:
			print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (item.alg, item.cmp, item.opt)
			print 'Similarity: %0.2f\n' % (float(item.sim))
			
	del G
	del sig
	del similarities
	del fc
	

"""ea = ScreenEA()	
func = get_func(ea)
fc = FlowChart(func)

G = graph(fc)	
sig = signature(fc, G, True)

similarities = sig.compare()

similarities.sort()

print '_____Results of function at %x (Threshold = %0.3f)_____' % (func.startEA, float(threshold))

for item in similarities:
	if item.sim >= threshold:
		print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (item.alg, item.cmp, item.opt)
		print 'Similarity: %0.3f\n' % (float(item.sim))
		
del G
del sig
del similarities
del fc"""
	
print "compare_func_sig.py has completed\n--------------------\n"
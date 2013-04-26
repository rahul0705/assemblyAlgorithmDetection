from idaapi import *
from idc import *
from idautils import *
from string import *
from graph import *
from function import *

threshold = 1

print "\n--------------------\nSPP.py has been started"

ea = ScreenEA()

# Loop through all the functions
for function_ea in Functions(SegStart(ea), SegEnd(ea)):
	fc = FlowChart(get_func(function_ea))
	G = graph(fc)
	func = function_block(fc, G, False)
	similarities = func.compare(threshold)
	
	for key in similarities.keys():
		print hex(function_ea), GetFunctionName(function_ea)
		file_components = split(similarities[key][1], ' ')
		algorithm = file_components[0]
		compiler = (split(file_components[2], '.'))[0]
		optimization = file_components[1]
		print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (algorithm, compiler, optimization)
		print 'Similarity: %0.2f\n' % (float(similarities[key][0]))
			
	#del G
	#del sig
	#del similarities
	#del fc
print "SPP.py has completed\n--------------------\n"
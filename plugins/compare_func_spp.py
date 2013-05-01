from idaapi import *
from idc import *
from idautils import *
from string import *
from graph import *
from function import *

OLDDIR = os.getcwd()
DIR = ".\\.."
print "\n--------------------\ncompare_func_spp.py has been started"
os.chdir(DIR)
ea = ScreenEA()

# Loop through all the functions
for function_ea in Functions(SegStart(ea), SegEnd(ea)):
	fc = FlowChart(get_func(function_ea))
	G = graph(fc)
	func = function_block(fc, G, False)
	exact = func.exactCompare()
	similarities = func.compare()
	
	for key in exact.keys():
		print hex(function_ea), GetFunctionName(function_ea)
		file_components = split(exact[key][1], ' ')
		algorithm = file_components[0]
		compiler = file_components[1]
		optimization = file_components[2]
		print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (algorithm, compiler, optimization)
		print 'Similarity: %0.2f\n' % (float(exact[key][0]))
	
	for key in similarities.keys():
		print hex(function_ea), GetFunctionName(function_ea)
		file_components = split(similarities[key][1], ' ')
		algorithm = file_components[0]
		compiler = file_components[1]
		optimization = file_components[2]
		print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (algorithm, compiler, optimization)
		print '%d possible extra or missing instructions\n' % (similarities[key][0])
			
	del G
	del func
	del similarities
	del fc
print "compare_func_spp.py has completed\n--------------------\n"
os.chdir(OLDDIR)
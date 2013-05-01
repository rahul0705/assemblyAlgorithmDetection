from idaapi import *
from idc import *
from idautils import *
from string import *
from graph import *
from function import *

print "\n--------------------\nmatch_blocks_spp.py has been started"

ea = ScreenEA()

# Loop through all the functions
for function_ea in Functions(SegStart(ea), SegEnd(ea)):
	fc = FlowChart(get_func(function_ea))
	G = graph(fc)
	func = function_block(fc, G, False)
	matchingBlocks = func.compareBlocks()
	
	for key in matchingBlocks.keys():
		print hex(function_ea), GetFunctionName(function_ea)
		file_components = split(matchingBlocks[key][1], ' ')
		algorithm = file_components[0]
		compiler = file_components[1]
		optimization = file_components[2]
		print 'Algorithm: %s, Compiler: %s, Optimization: %s' % (algorithm, compiler, optimization)
		print 'Number of matching blocks: %d\n' % matchingBlocks[key][0]
			
	del G
	del func
	del matchingBlocks
	del fc
print "match_blocks_spp.py has completed\n--------------------\n"
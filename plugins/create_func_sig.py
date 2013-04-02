from idaapi import *
from graph import *
from signature import *

print "\n--------------------\ncreate_func_sig.py has been started"

sig = signature()
G = graph()		
		
ea = ScreenEA()
fc = FlowChart(get_func(ea))

for block in fc:
	G.addVertex(vertex(block))
	
	for head in Heads(block.startEA, block.endEA):
		mnem = GetMnem(head)
		
		if mnem not in sig.instr_count:
			sig.instr_count[mnem] = 1
		else:
			sig.instr_count[mnem] = sig.instr_count[mnem] + 1
			
G.genereateEdges()
DFS(G, G.V[0], 1)

sig.block_count = len(G.V)
sig.edge_count = len(G.E)

for e in G.E:
	if e.status is 2:
		sig.back_edge_count =  sig.back_edge_count + 1

sig.printSig()
		
print "create_func_sig.py has completed\n--------------------\n"
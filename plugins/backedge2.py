from idaapi import *
from graph import *

print "\n--------------------\nbackedge2.py has been started"
		
def DFS(G, v, l):
	v.status = 1
	v.level = l
	
	for edge in v.adjList:
		if edge.status is 0:
			w = edge.dstV
			if w.status is 0:
				edge.status = 1
				l = l + 1
				DFS(G, w, l)
			elif w.status is 1 and w.level is not 0 and w.level <= v.level:
				edge.status = 2

				
G = graph()
fc = FlowChart(get_func(get_screen_ea()))
for block in fc:
	G.addVertex(vertex(block))
G.genereateEdges()	
#G.printGraph()
DFS(G, G.V[0], 1)

for e in G.E:
	if e.status is 2:
		e.printEdge()
		
		if e.srcV.block.id is e.dstV.block.id:
			for head in Heads(e.srcV.block.startEA, e.srcV.block.endEA):
				SetColor(head, CIC_ITEM, 0xFF0000)
		else:
			for head in Heads(e.srcV.block.startEA, e.srcV.block.endEA):
				SetColor(head, CIC_ITEM, 0x0000FF)
				
			for head in Heads(e.dstV.block.startEA, e.dstV.block.endEA):
				SetColor(head, CIC_ITEM, 0x00FF00)

print "\n--------------------\nbackedge2.py has been completed"

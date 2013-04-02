from idaapi import *

print "\n--------------------\nbackedge2.py has been started"

#status = 0 -> Unexplored
#status = 1 -> Explored		
class vertex:
	def __init__(self, block):
		self.block = block
		self.status = 0
		self.level = 0
		self.adjList = []
			
	def printVertex(self):
		print "Vertex ID: %d Start: %x End: %x" % (self.block.id, self.block.startEA, self.block.endEA)
		
		for edge in self.adjList:
			print "\tSuccessor ID: %d Start: %x End: %x" % (edge.dstV.block.id, edge.dstV.block.startEA, edge.dstV.block.endEA)
			
		print ""

#status = 0 -> Unexplored
#status = 1 -> Discovery Edge
#status = 2 -> Back Edge
class edge:
	def __init__(self, srcV, dstV):
		self.srcV = srcV
		self.dstV = dstV
		self.status = 0
		
	def printEdge(self):
		print "Source ID: %d Start: %x" % (self.srcV.block.id, self.srcV.block.startEA)
		print "Destination ID: %d Start: %x" % (self.dstV.block.id, self.dstV.block.startEA)
		print ""

class graph:
	def __init__(self):
		self.V = []
		self.E = []
	
	def addVertex(self, vertex):
		self.V.append(vertex)
	
	def genereateEdges(self):
		for v in self.V:
			for b in v.block.succs():
				e = edge(v, self.V[b.id])
				self.E.append(e)
				v.adjList.append(e)
	
	def printGraph(self):
		print "_____Verticies_____"
		for v in self.V:
			v.printVertex()
		
		print "_____Edges_____"
		for e in self.E:
			e.printEdge()
		
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

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
		print "Source ID: %d Address: %x" % (self.srcV.block.id, self.srcV.block.startEA)
		print "Destination ID: %d Address: %x" % (self.dstV.block.id, self.dstV.block.startEA)
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
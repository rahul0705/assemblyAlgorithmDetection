from idaapi import *
from idc import *
from idautils import *

#status = 0 -> Unexplored
#status = 1 -> Explored

#label = 0 -> Normal
#label = 1 -> Source of back edge
#label = 2 -> Dest of back edge	
class vertex:
	def __init__(self, block):
		self.block = block
		self.status = 0
		self.level = 0
		self.label = 0
		self.adjList = []
		self.backAdjList = []

	def printVertex(self):
		print "Vertex ID: %d Start: %x End: %x" % (self.block.id, self.block.startEA, self.block.endEA)
		
		for edge in self.adjList:
			print "\tSuccessor ID: %d Start: %x End: %x" % (edge.dstV.block.id, edge.dstV.block.startEA, edge.dstV.block.endEA)
			
		for edge in self.backAdjList:
			print "\tPredecessor ID: %d Start: %x End: %x" % (edge.dstV.block.id, edge.dstV.block.startEA, edge.dstV.block.endEA)
			
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
	def __init__(self, FC):
		self.V = []
		self.E = []
		self.RE = []
		
		for block in FC:
			self.addVertex(vertex(block))
			
		self.genereateEdges()
	
	def addVertex(self, vertex):
		self.V.append(vertex)
	
	def genereateEdges(self):
		for v in self.V:
			for b in v.block.succs():
				e = edge(v, self.V[b.id])
				self.E.append(e)
				v.adjList.append(e)
				e = edge(self.V[b.id], v)
				self.RE.append(e)
				self.V[b.id].backAdjList.append(e)
	
	def printGraph(self):
		print "_____Verticies_____"
		for v in self.V:
			v.printVertex()
		
		print "_____Edges_____"
		for e in self.E:
			e.printEdge()
			
		print "_____Reverse Edges_____"
		for e in self.RE:
			e.printEdge()
			
	def labelEdges(self, v, level):
		v.status = 1
		v.level = level
		
		for edge in v.adjList:
			if edge.status is 0:
				w = edge.dstV
				if w.status is 0:
					edge.status = 1
					level = level + 1
					self.labelEdges(w, level)
					level = level - 1
				elif w.status is 1 and w.level is not 0 and w.level <= v.level:
					edge.status = 2
					edge.srcV.label = 1
					edge.dstV.label = 2
					
					for e in edge.dstV.backAdjList:
						if e.dstV == edge.srcV:
							e.status = 2
					
	def colorBackEdges(self):
		for e in self.E:
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
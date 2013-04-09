from idaapi import *
from idautils import *
from idc import *
from string import *

class signature:
	def __init__(self, FC, G):
		self.sigVector = {}
		
		if FC is not None and G is not None:
			for block in FC:
				for head in Heads(block.startEA, block.endEA):
					item = GetMnem(head)
					
					if item not in self.sigVector:
						self.sigVector[item] = 1
					else:
						self.sigVector[item] = self.sigVector[item] + 1

			G.labelEdges(G.V[0], 1)
			
			self.sigVector['block_count'] = len(G.V)
			self.sigVector['edge_count'] = len(G.E)
			
			self.sigVector['back_edge_count'] = 0
			for e in G.E:
				if e.status is 2:
					self.sigVector['back_edge_count'] = self.sigVector['back_edge_count'] + 1
		
	def save(self):
		f = open("sig.txt", "w")
		
		for item in self.sigVector:
			f.write(item + " " + str(self.sigVector[item]) + "\n")
		
		f.close()
		
	def load(self):
		f = open("sig.txt", "r")
		lines = f.readlines()
		f.close()
		
		i = 0
		
		#while lines[i] != "\n":
		#	words = split(lines[i])
		#	self.sigVector[words[0]] = int(words[1])
		#	i = i + 1
		
		for line in lines:
			words = split(line)
			self.sigVector[words[0]] = int(words[1])
			i = i + 1
			
	def printSig(self):
		for item in self.sigVector:
			print "%s: %d" % (item, self.sigVector[item])

		
	def compare(self, sig):
		selfCombinedVector = {}
		otherCombinedVector = {}
		
		for item in self.sigVector:
			selfCombinedVector[item] = self.sigVector[item]
			otherCombinedVector[item] = 0
				
		for item in sig.sigVector:
			if item not in selfCombinedVector:
				selfCombinedVector[item] = 0
			otherCombinedVector[item] = sig.sigVector[item]
			
		for item in selfCombinedVector:
			print "%s: %d" % (item, selfCombinedVector[item])
		
		print "\n"
			
		for item in otherCombinedVector:
			print "%s: %d" % (item, otherCombinedVector[item])
		
		#for item in self.instr_count:
		#	combinedVector[item] = -1;
			
		#for item in sig.instr_count:
		#	combinedVector[item] = -1;
			
		#for item in combinedVector:
		#	print "%s: %d" % (item, combinedVector[item]) 
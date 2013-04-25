from idaapi import *
from idautils import *
from idc import *
from string import *
from math import *
from sys import *

class signature:
	def __init__(self, FC, G):
		self.sigVector = {}
		self.algorithm = ""
		self.compiler = ""
		self.optimization = ""
		
		
		if FC is not None and G is not None:
			for block in FC:
				for head in Heads(block.startEA, block.endEA):
					item = GetMnem(head)
					
					if item != 'mov':
						if item not in self.sigVector:
							self.sigVector[item] = 1
						else:
							self.sigVector[item] = self.sigVector[item] + 1

			G.labelEdges(G.V[0], 1)
			
			#self.sigVector['block_count'] = len(G.V)
			#self.sigVector['edge_count'] = len(G.E)
			
			self.sigVector['block_to_edge_ratio'] = float(len(G.V)) / len(G.E)
			
			self.sigVector['back_edge_count'] = 0
			for e in G.E:
				if e.status is 2:
					self.sigVector['back_edge_count'] = self.sigVector['back_edge_count'] + 1
			
	def save(self):
		f = open("../sig.txt", "w")
		
		for item in self.sigVector:
			f.write(item + " " + str(self.sigVector[item]) + "\n")
		
		f.close()
		
	def load(self):
		f = open("../sig.txt", "r")
		lines = f.readlines()
		f.close()
		
		i = 0
		
		#while lines[i] != "\n":
		#	words = split(lines[i])
		#	self.sigVector[words[0]] = int(words[1])
		#	i = i + 1
		
		for line in lines:
			words = split(line)
			self.sigVector[words[0]] = float(words[1])
			i = i + 1
			
	def printSig(self):
		for item in self.sigVector:
			print "%s: %f" % (item, self.sigVector[item])

		
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
			
		scale = 1
		
		dotProduct = 0
		for item in selfCombinedVector:
			print "%s: Self: %f, Other: %f" % (item, selfCombinedVector[item], otherCombinedVector[item])
			dotProduct = dotProduct + float(selfCombinedVector[item]) * float(otherCombinedVector[item])
			
		print "Dot Product: %f" % dotProduct
		
		mag1 = 0
		mag2 = 0
		
		for item in selfCombinedVector:
			mag1 = mag1 + float(selfCombinedVector[item]) * float(selfCombinedVector[item])
			mag2 = mag2 + float(otherCombinedVector[item]) * float(otherCombinedVector[item])
		
		mag1 = sqrt(mag1)
		mag2 = sqrt(mag2)
		
		print "mag1: %f, mag2: %f" % (mag1, mag2)
		
		similarity = dotProduct / (mag1 * mag2)
		
		return similarity
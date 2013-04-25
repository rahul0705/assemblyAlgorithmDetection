from idaapi import *
from idautils import *
from idc import *
from string import *
from math import *
from sys import *

DIR = "C:\\Users\\gbrinzea\\Desktop\\CS490PRE\\repo\\trunk\\plugins"



class signature:
	def __init__(self, FC, G):
		self.sigVector = {}
		self.algorithm = ""
		self.compiler = ""
		self.optimization = ""
		
		if FC is not None and G is not None:
			filename = get_root_filename()
		
			file_components = split(filename, '-')
			
			self.algorithm = file_components[0]
			self.compiler = (split(file_components[2], '.'))[0]
			self.optimization = file_components[1]
			
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
		os.chdir(DIR)
		
		f = open("signatures/" + self.algorithm + "-" + self.optimization + "-" + self.compiler + ".txt", "w")
		
		f.write("Algorithm " + self.algorithm + "\n")
		f.write("Compiler " + self.compiler + "\n")
		f.write("Optimization " + self.optimization + "\n\n")
		
		for item in self.sigVector:
			f.write(item + " " + str(self.sigVector[item]) + "\n")
		
		f.close()
		
	def load(self):
		os.chdir(DIR)
	
		f = open("../sig.txt", "r")
		lines = f.readlines()
		f.close()
		
		i = 0
		
		for line in lines:
			words = split(line)
			
			if i is 0:
				self.algorithm = words[1]
			elif i is 1:
				self.compiler = words[1]
			elif i is 2:
				self.optimization = words[1]
			elif i > 3:
				self.sigVector[words[0]] = float(words[1])
			
			i = i + 1			
			
	def printSig(self):
		print "Algorithm: %s" % (self.algorithm)
		print "Compiler: %s" % (self.compiler)
		print "Optimization: %s\n" % (self.optimization)
		
		print "_____Signature Vector_____"
		for item in self.sigVector:
			print "%s: %f" % (item, self.sigVector[item])

		
	def compare(self, other):
		selfCombinedVector = {}
		otherCombinedVector = {}
		
		for item in self.sigVector:
			selfCombinedVector[item] = self.sigVector[item]
			otherCombinedVector[item] = 0
				
		for item in other.sigVector:
			if item not in selfCombinedVector:
				selfCombinedVector[item] = 0
			otherCombinedVector[item] = other.sigVector[item]
			
		scale = 1
		
		dotProduct = 0
		for item in selfCombinedVector:
			print "%s:\nLoaded: %f, Current: %f" % (item, selfCombinedVector[item], otherCombinedVector[item])
			dotProduct = dotProduct + float(selfCombinedVector[item]) * float(otherCombinedVector[item])
			
		print "\nDot Product: %f" % dotProduct
		
		mag1 = 0
		mag2 = 0
		
		for item in selfCombinedVector:
			mag1 = mag1 + float(selfCombinedVector[item]) * float(selfCombinedVector[item])
			mag2 = mag2 + float(otherCombinedVector[item]) * float(otherCombinedVector[item])
		
		mag1 = sqrt(mag1)
		mag2 = sqrt(mag2)
		
		print "Loaded magnitude: %f, Current magnitude: %f" % (mag1, mag2)
		
		similarity = dotProduct / (mag1 * mag2)
		
		return similarity
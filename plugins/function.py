from __future__ import division
from idaapi import *
from idc import *
from idautils import *
from graph import *
from json import *
from string import *
from math import *
from sys import *
from fractions import *

def nextPrime(currentPrime):
	nextPrime = currentPrime + 1
	if nextPrime%2 == 0:
		nextPrime += 1
	while not isPrime(nextPrime):
		nextPrime += 2
	return nextPrime

def isPrime(n):
	ret = True
	if n%2 == 0:
		ret = False
	else:
		for i in range(3, int(sqrt(n) + 1)):
			if n%i == 0:
				ret = False
	return ret

class block:
	def __init__(self, block, ops, currentPrime):
		self.prime = 1
		self.instructions = 0
		self.lastPrime = currentPrime
		self.ops = ops
		verOps = {}
		for head in Heads(block.startEA, block.endEA):
			self.instructions += 1
			op = GetMnem(head)
			self.lastPrime = currentPrime
			if op not in self.ops:
				self.ops[op] = currentPrime
				currentPrime = nextPrime(currentPrime)
			if op not in verOps:
				verOps[op] = 1
			else:
				verOps[op] += 1
		for key in verOps.keys():
			self.prime *= (self.ops[key] ** verOps[key])
	
	def getPrime(self):
		return self.prime
		
	def getInstructions(self):
		return self.instructions
		
	def getLastPrime(self):
		return self.lastPrime
	
	def getOps(self):
		return self.ops

class function_block:
	def __init__(self, FC, G, flag = True):
		self.ops = load(open("primes/ops.txt"))
		self.instructions = 0
		currentPrime = 2;
		for key in self.ops.keys():
			if self.ops[key] > currentPrime:
				currentPrime = self.ops[key]
		currentPrime = nextPrime(currentPrime)
		self.blocks = {}
		self.algorithm = ""
		self.compiler = ""
		self.optimization = ""
		self.prime = 1
		
		if FC is not None and G is not None:
			if flag:
				filename = get_root_filename()
				file_components = split(filename, '-')
				self.algorithm = file_components[0]
				self.compiler = (split(file_components[2], '.'))[0]
				self.optimization = file_components[1]
			for node in FC:
				blk = block(node, self.ops, currentPrime)
				self.ops = blk.getOps()
				currentPrime = nextPrime(blk.getLastPrime())
				self.blocks[node.id] = blk.getPrime()
				self.instructions += blk.getInstructions()
			for id in self.blocks:
				self.prime *= self.blocks[id]
	
	def save(self):
		spp = load(open("primes/spp.txt"))
		spp[str(self)] = [self.prime, self.blocks, self.instructions]
		dump(self.ops, open("primes/ops.txt", "w"), sort_keys = True, indent = 2)
		dump(spp, open("primes/spp.txt", "w"), sort_keys = True, indent = 2)

	def printSPP(self):
		print "Algorithm: %s" % (self.algorithm)
		print "Compiler: %s" % (self.compiler)
		print "Optimization: %s\n" % (self.optimization)
		
		print "_____Function SPP_____"
		print self.prime
		
		print "\n_____Block SPP_____"
		for item in self.blocks:
			print "%s: %d" % (item, self.blocks[item])

	def exactCompare(self):
		spp = load(open("primes/spp.txt"))
		ret = {}
		for key in spp.keys():
			diff = 0.0
			if spp[key][0] < self.prime:
				diff = spp[key][0]/self.prime
			elif spp[key][0] > self.prime:
				diff = self.prime/spp[key][0]
			else:
				diff = 1
			if diff == 1:
				ret[key] = [diff, key]
		return ret

	def compare(self, threshold=.10):
		spp = load(open("primes/spp.txt"))
		ops = load(open("primes/ops.txt"))
		avgPrime = 0
		for key in ops.keys():
			avgPrime += ops[key]
		avgPrime = int(ceil(avgPrime/len(ops)))
		ret = {}
		for key in spp.keys():
			bounds = int(ceil(spp[key][2] * threshold) * avgPrime)
			if spp[key][0] < (self.prime * bounds) and spp[key][0] > (self.prime // bounds):
				ret[key] = [ceil(spp[key][2]*threshold), key]
		return ret
		
	def compareBlocks(self, threshold=.55):
		spp = load(open("primes/spp.txt"))
		ret = {}
		for key in spp.keys():
			blocks = spp[key][1]
			length = len(blocks)
			temp = self.blocks.copy()
			count = 0
			for sblock in temp.keys():
				for oblock in blocks.keys():
					if(temp[sblock] == blocks[oblock]):
						del blocks[oblock]
						del temp[sblock]
						count += 1
						break
			temp.clear()
			blocks.clear()
			if count > int(floor((length-2) * threshold)):
				ret[key] = [count, key]
		return ret
			
	def __repr__(self):
		return self.algorithm + " " + self.compiler + " " + self.optimization

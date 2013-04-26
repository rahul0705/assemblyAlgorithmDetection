from idaapi import *
from idc import *
from idautils import *
from graph import *
from json import *
from string import *
from math import *
from sys import *

def nextPrime(currentPrime):
	nextPrime = currentPrime + 1
	if nextPrime%2 == 0:
		nextPrime += 1
	while not isPrime(nextPrime):
		nextPrime += 2
	return nextPrime

def isPrime(num):
	ret = True
	if num%2 == 0:
		ret = False
	else:
		for i in range(3, int(sqrt(num) + 1)):
			if num%i == 0:
				ret = False
	return ret

class block:
	def __init__(self, block, ops, currentPrime):
		self.prime = 1
		verOps = {}
		for head in Heads(block.startEA, block.endEA):
			op = GetMnem(head)
			if op not in ops:
				ops[op] = currentPrime
				currentPrime = nextPrime(currentPrime)
			if op not in verOps:
				verOps[op] = 1
			else:
				verOps[op] += 1
		for key in verOps.keys():
			self.prime *= (ops[key] ** verOps[key])
	
	def getPrime(self):
		return self.prime

class function_block:
	def __init__(self, FC, G, flag = True):
		self.ops = load(open("../ops.txt"))
		
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
				self.blocks[node.id] = blk.getPrime()
			for id in self.blocks:
				self.prime *= self.blocks[id]
	
	def save(self):
		spp = load(open("../spp.txt"))
		spp[str(self)] = [self.prime, self.blocks]
		dump(self.ops, open("../ops.txt", "w"), sort_keys = True, indent = 2)
		dump(spp, open("../spp.txt", "w"), sort_keys = True, indent = 2)

	def printSPP(self):
		print "Algorithm: %s" % (self.algorithm)
		print "Compiler: %s" % (self.compiler)
		print "Optimization: %s\n" % (self.optimization)
		
		print "_____Function SPP_____"
		print self.prime
		
		print "\n_____Block SPP_____"
		for item in self.blocks:
			print "%s: %d" % (item, self.blocks[item])

	def compare(self, threshold):
		spp = load(open("../spp.txt"))
		ret = {}
		for key in spp.keys():
			diff = 0.0
			if spp[key][0] < self.prime:
				diff = Decimal(spp[key][0])/Decimal(self.prime)
			elif spp[key][0] > self.prime:
				diff = Decimal(self.prime)/Decimal(spp[key][0])
			else:
				diff = 1
			if diff >= threshold:
				ret[key] = [diff, key]
		return ret
			
	def __repr__(self):
		return self.algorithm + " " + self.compiler + " " + self.optimization
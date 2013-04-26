from idaapi import *
from idc import *
from idautils import *
from graph import *
import json
import math

def nextPrime(currentPrime):
	nextPrime = currentPrime + 1
	if nextPrime%2 == 0:
		nextPrime += 1
	while isPrime(nextPrime) is not True:
		nextPrime += 2
	return nextPrime

def isPrime(num):
	ret = True
	if num%2 == 0:
		ret = False
	else:
		for i in range(3, int(math.sqrt(num) + 1)):
			if num%i == 0:
				ret = False
	return ret

print "\n--------------------\nSPP.py has been started"
	
ops = json.load(open("../ops.txt"))
spp = json.load(open("../spp.txt"))
currentPrime = 2;
for key in ops.keys():
	if ops[key] > currentPrime:
		currentPrime = ops[key]
currentPrime = nextPrime(currentPrime)

ea = ScreenEA()
fc = FlowChart(get_func(ea))
G = graph(fc)

graphPrime = 1
for v in G.V:
	verOps = {}
	for head in Heads(v.block.startEA, v.block.endEA):
		op = GetMnem(head)
		if op not in ops:
			ops[op] = currentPrime
			currentPrime = nextPrime(currentPrime)
		if op not in verOps:
			verOps[op] = 1
		else:
			verOps[op] += 1
	prime = 1
	for key in verOps.keys():
		prime *= int(math.pow(ops[key],  verOps[key]))
	graphPrime *= prime
	name = get_root_filename() + " " + str(v.block.startEA)
	first = True
	for key in spp.keys():
		diff = 0.0
		if spp[key] < prime:
			diff = float(spp[key])/prime
		elif spp[key] > prime:
			diff = prime/float(spp[key])
		else:
			diff = 1
		if diff >= .85:
			if first:
				print name
				first = False
			difference = "%0.2f" % (diff*100)
			print "\tMatch with " + key + " only " + str(difference) + "% similarity"
	spp[name] = prime
name = get_root_filename()
spp[name] = graphPrime
first = True
for key in spp.keys():
		diff = 0.0
		if spp[key] < graphPrime:
			diff = float(spp[key])/graphPrime
		elif spp[key] > graphPrime:
			diff = graphPrime/float(spp[key])
		else:
			diff = 1
		if diff >= .65:
			if first:
				print name
				first = False
			difference = "%0.2f" % (diff*100)
			print "\tMatch with " + key + " only " + str(difference) + "% similarity"
json.dump(ops, open("../ops.txt", "w"), sort_keys = True, indent = 2)
json.dump(spp, open("../spp.txt", "w"), sort_keys = True, indent = 2)
print "SPP.py has completed\n--------------------\n"
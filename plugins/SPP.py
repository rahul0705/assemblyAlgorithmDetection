from idaapi import *
from idc import *
from idautils import *
import json

currentPrime = 

def nextPrime():
	nextPrime = currentPrime + 1
	if nextPrime%2 == 0:
		nextPrime+=1
	while !isPrime(nextPrime):
		nextPrime+=
	

ops = json.load(open("../ops.txt"))

ea = ScreenEA()
fc = FlowChart(get_func(ea))
G = graph(fc)

for v in G.V:
	for op in v.getNextOp()
		if op in ops:
			ops[op][1]++
		else:
			ops[op] = [nextPrime(), 1]
	break

json.dump(d, open("../ops.txt", "w"))
print "\n--------------------\ncompare_instr_count.py has been started"

from string import *
from math import *

instr_sig = {'default' : -1}

ea = ScreenEA()
fc = FlowChart(get_func(ea))

for block in fc:
	for head in Heads(block.startEA, block.endEA):
		mnem = GetMnem(head)
		
		if mnem not in instr_sig:
			instr_sig[mnem] = 1
		else:
			instr_sig[mnem] = instr_sig[mnem] + 1
	
total_instr = 0
f = open("../../plugins/sig.txt", "r");

loaded_sig = {'default' : -1}

for line in f:
	words = split(line)
	loaded_sig[words[0]] = int(words[1])

differences = 0
unmatched_instrs = 0;
	
for mnem in instr_sig:
	if mnem != 'default':
		if mnem in loaded_sig:
			curr_count = instr_sig[mnem]
			loaded_count = loaded_sig[mnem]
			
			diff = fabs(curr_count - loaded_count)
			differences = differences + diff
		elif mnem not in loaded_sig:
			#differences = differences + instr_sig[mnem]
			unmatched_instrs = unmatched_instrs + 1
			print mnem

f.close();

print "Difference of amount between matched instrs: %d" % differences
print "Unmached instrs: %d" % unmatched_instrs
		
print "compare_instr_count.py has completed\n--------------------\n"
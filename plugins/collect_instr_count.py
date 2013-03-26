print "\n--------------------\ncollect_instr_count.py has been started"
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
f = open("../../plugins/sig.txt", "w");
for mnem in instr_sig:
	if mnem != 'default':
		if len(mnem) > 5:
			print "mnem: %s\tcount: %d" % (mnem, instr_sig[mnem])
		else:
			print "mnem: %s\t\tcount: %d" % (mnem, instr_sig[mnem])
			
		f.write(mnem + " " + str(instr_sig[mnem]) + "\n")	
			
		total_instr = total_instr + instr_sig[mnem]

print "Total instructions: %d" % (total_instr)

f.close();
		
print "8===========Dcollect_instr_count.py has completed\n--------------------\n"
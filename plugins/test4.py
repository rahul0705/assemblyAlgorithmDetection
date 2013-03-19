print "\n--------------------\ntest4.py has been started"

#ea = ScreenEA()

#for function in Functions(SegStart(ea), SegEnd(ea)):

fc = FlowChart(get_func(ScreenEA()))

for block in fc:
	print "BLOCK: %x - %x [%d]:" % (block.startEA, block.endEA, block.id)
		
	for head in Heads(block.startEA, block.endEA):
		print "\t%s %s %s" % (GetMnem(head), GetOpnd(head, 0), GetOpnd(head, 1))
			
print "test4.py has completed\n--------------------\n"
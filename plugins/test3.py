print "\n--------------------\ntest3.py has been started"

ea = ScreenEA()

for function in Functions(SegStart(ea), SegEnd(ea)):

	fc = FlowChart(get_func(function))

	for block in fc:
		print "BLOCK: %x - %x [%d]:" % (block.startEA, block.endEA, block.id)
			
		movCount = 0
		for head in Heads(block.startEA, block.endEA):
			if GetMnem(head) == 'mov':
				movCount = movCount + 1
			
		if movCount >= 2:
			for head in Heads(block.startEA, block.endEA):
				SetColor(head, CIC_ITEM, 0xBFFFBF)
	
		
print "test3.py has completed\n--------------------\n"
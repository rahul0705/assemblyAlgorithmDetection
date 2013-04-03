from idaapi import *

print "\n--------------------\nResetting node colors in current segment"

ea = ScreenEA()

for function in Functions(SegStart(ea), SegEnd(ea)):

	fc = FlowChart(get_func(function))

	for block in fc:
		print "BLOCK: %x - %x [%d]:" % (block.startEA, block.endEA, block.id)
			
		for head in Heads(block.startEA, block.endEA):
			SetColor(head, CIC_ITEM, 0xFFFFFF)
	
		
print "Node colors have been reset\n--------------------\n"
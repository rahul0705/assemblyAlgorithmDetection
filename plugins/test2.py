
print "\n--------------------\ntest2.py has been started"

func = idaapi.get_func(idaapi.get_screen_ea())
fc = idaapi.FlowChart(func)

for block in fc:
	print "BLOCK: %x - %x [%d]:" % (block.startEA, block.endEA, block.id)
	
	'''for succ_block in block.succs():
		print "\tSUCC: %x - %x [%d]:" % (succ_block.startEA, succ_block.endEA, succ_block.id)
		
	for pred_block in block.preds():
		print "\tPRED: %x - %x [%d]:" % (pred_block.startEA, pred_block.endEA, pred_block.id)'''
		
	for head in Heads(block.startEA, block.endEA):
		print GetMnem(head)
	
		
print "test2.py has completed\n--------------------\n"

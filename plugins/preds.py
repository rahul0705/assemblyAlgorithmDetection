from idaapi import *
from idc import *
from idautils import *

func= get_func(get_screen_ea())
fc= idaapi.FlowChart(func)

for block in fc:
    print "%x -%x [%d]:" % (block.startEA, block.endEA, block.id)

    for pred_block in block.preds():
        print " %x -%x [%d]:" % (pred_block.startEA, pred_block.endEA, pred_block.id)

    print "\n"

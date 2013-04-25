def color_block (bb, color):
    for ea in Heads(bb.startEA, bb.endEA):
        SetColor(ea, CIC_ITEM, color)

func = idaapi.get_func(idaapi.get_screen_ea())
fc = idaapi.FlowChart(func)

for block in fc:
    color_block(block, 0xFFFFFF)

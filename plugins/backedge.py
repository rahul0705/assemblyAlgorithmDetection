func = idaapi.get_func(idaapi.get_screen_ea())
fc = idaapi.FlowChart(func)

def contains (lst, s1, s2):
    for x in lst:
        if (x[0] == s1 and x[1] == s2):
            return True
        elif (x[0] == s2 and x[1] == s1):
            return True
    return False
        
block_dfs = {}
backedgelist = []
def dfs(graph, block):
    block_dfs[block.id] = 2
    set = block.succs()
    for edge in set:
        if not block_dfs.has_key(edge.id):
            dfs(graph, edge)
        else:
            if (not contains(backedgelist, block.startEA, edge.startEA)):
                backedgelist.append((block.startEA, edge.startEA))
            
for block in fc:
    dfs(block_dfs, block)
    break

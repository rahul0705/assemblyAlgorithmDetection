print "\n--------------------\nbackedge.py has been started"
func = idaapi.get_func(idaapi.get_screen_ea())
fc = idaapi.FlowChart(func)

#def contains (lst, s1, s2):
#    for x in lst:
#        if (x[0] == s1 and x[1] == s2):
#            return True
#        elif (x[0] == s2 and x[1] == s1):
#            return True
#    return False
        
#block_dfs = {}
#backedgelist = []
#def dfs(graph, block):
#    block_dfs[block.id] = 2
#    set = block.succs()
#    for edge in set:
#        if not block_dfs.has_key(edge.id):
#            dfs(graph, edge)
#        else:
#            if (not contains(backedgelist, block.startEA, edge.startEA)):
#                backedgelist.append((block.startEA, edge.startEA))
# http://www.cs.nyu.edu/courses/summer04/G22.1170-001/6a-Graphs-More.pdf
		
graph = {}
edges = {}
for block in fc:
	adjList = []
	for node in block.succs():
		adjList.append(node.id)
		edges[str(block.id) + str(node.id)] = [0, 0, block, node]
	graph[block.id] = [adjList, 0]
	#print(edges)

def dfs(graph, vertex):
	graph[vertex][1] = 1
	for node in graph[vertex][0]:
		if edges[str(vertex) + str(node)][0] is 0:
			if graph[node][1] is 0:
				edges[str(vertex) + str(node)][0]
				dfs(graph, node)
			elif graph[node][1] is 1:	
				edges[str(vertex) + str(node)][1] = 1
for block in fc:
	dfs(graph, block.id)
	break
for edge in edges:
	#print(edges[edge][1])
	if edges[edge][1] is 1:
		print "BLOCK: %x - %x [%d]:" % (edges[edge][2].startEA, edges[edge][3].startEA, edges[edge][2].id)
		#print "BLOCK: %x - %x [%d]:" % (edges[edge][3].startEA, edges[edge][3].endEA, edges[edge][3].id)

print "\n--------------------\nbackedge.py has been completed"

from idaapi import *
from graph import *

print "\n--------------------\nbackedge2.py has been started"

fc = FlowChart(get_func(get_screen_ea()))
G = graph(fc)

G.printGraph();
G.labelEdges(G.V[0], 1)
G.colorBackEdges()

print "\n--------------------\nbackedge2.py has been completed"

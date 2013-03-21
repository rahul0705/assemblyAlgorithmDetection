from itertools import chain
               
reg = {} #Store all the registers
graph = {} #Magical Shit here
registerList = ["eax", "ebx", "ecx", "edx", "edi", "esi"] # ebp/esp not needed

def color_block (bb, color):
    for ea in Heads(bb.startEA, bb.endEA):
        SetColor(ea, CIC_ITEM, color)


def replaceRegisters(str):
    for x in registerList:
        if (str.find(x) != -1):
            str = str.replace(x, getRegister(x))
    return str


def printRegisters():
    for x in registerList:
        print "\t" + x + " = " + getRegister(x)


def isRegister(str):
    for x in registerList:
        if (x == str):
            return True
    return False


def setRegister(str, val):
    reg[str] = replaceRegisters(val)


def getRegister(str):
    if (reg.has_key(str)):
        return reg[str]
    return str


def addNode(node, val):
    if (graph.has_key(node)):
        (graph[node]).append(val)
    else:
        graph[node] = [val]

#From the magical land of the internet
def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None

    

func = idaapi.get_func(idaapi.get_screen_ea())
fc = idaapi.FlowChart(func)

for block in fc:

        it = chain(Heads(block.startEA, block.endEA))
        head = last = None
        while True:
            try:
                head = it.next()

                mnem = GetMnem(head)
                op1 = GetOpnd(head, 0)
                op2 = GetOpnd(head, 1)

            except StopIteration:
                if (last != None and GetMnem(last) != "mov"):
                    break
            
                if (graph == {}):
                    break
                
                op1 = GetOpnd(last, 0)
                op2 = GetOpnd(last, 1)
                
                op1 = replaceRegisters(getRegister(op1))
                op2 = replaceRegisters(getRegister(op2))
                #print op1 + " " + op2
                if (op1 != op2 and find_path(graph, op1, op2) != None and find_path(graph, op2, op1) != None):
                    print "\nBLOCK: %x - %x [%d]: Is a Swap" % (block.startEA, block.endEA, block.id)
                    color_block(block, 0xAEBAEB)
                    print GetDisasm(last)
                    print graph
                    printRegisters()

                graph = {}
                break

           # print GetDisasm(head)

            if (mnem == "mov"):
                if (isRegister(op1)):
                    setRegister(op1, op2)
                else:
                    if (isRegister(op2)):
                        last = head
                        op1 = replaceRegisters(getRegister(op1))
                        op2 = replaceRegisters(getRegister(op2))
                        #print graph
                        #print "Adding Node Between" + op1 + " " + op2
                        addNode(op1, op2)
                        #printRegisters()


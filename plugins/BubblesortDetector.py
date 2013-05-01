from itertools import chain
from graph import *


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


def modifyRegister(str, modify):
    reg[str] = reg[str] + modify

def getRegister(str):
    if (reg.has_key(str)):
        return reg[str]
    return str

def addNode(node, val):
    if (graphy.has_key(node)):
        (graphy[node]).append(val)
    else:
        graphy[node] = [val]

def nested_count(G, block_id, count = 0):
    for e in G.V[block_id].backAdjList:
        if e.status == 2:
            continue        
        
        parent = e.dstV
        
        #Green
        if parent.label == 2:
            count = count + 1

        if parent.label == 1:
            return count

        if count == 2:
            return count
            
        return nested_count(G, parent.block.id, count)


def find_path(graphy, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graphy.has_key(start):
        return None
    for node in graphy[start]:
        if node not in path:
            newpath = find_path(graphy, node, end, path)
            if newpath: return newpath
    return None

ea = ScreenEA()
for function in Functions(SegStart(ea), SegEnd(ea)):
    cmp_op1 = cmp_op2 = cmp_blk = None
    func = get_func(function)
    fc = idaapi.FlowChart(func)

    reg = {} #Store all the registers
    graphy = {} 
    registerList = ["eax", "ebx", "ecx", "edx", "edi", "esi"] # ebp/esp not needed

    G = graph(fc)
    G.labelEdges(G.V[0], 1)

    detected = False
    #print "Funcation : " + GetFunctionName(func.startEA)
    #Swap Code
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
					
                if (graphy == {}):
                    break

                op1 = GetOpnd(last, 0)
                op2 = GetOpnd(last, 1)

                op1 = replaceRegisters(getRegister(op1))
                op2 = replaceRegisters(getRegister(op2))
                                
                if (op1 != op2 and find_path(graphy, op1, op2) != None and find_path(graphy, op2, op1) != None):
                    #print "\nBLOCK: %x [%d]: Is a Swap" % (block.startEA, block.id)
                    color_block(block, 0xAEBAEB)
					
                    if (cmp_op1 != cmp_op2 and graphy.has_key(cmp_op1) and graphy.has_key(cmp_op2)):
                        if (find_path(graphy, cmp_op1, cmp_op2) and find_path(graphy, cmp_op2, cmp_op1)):
                            color_block(cmp_blk, 0xCCFA38)
							
                            count = nested_count(G, block.id)
                            if (count == 2):
                                detected = True
								
                graphy = {}
                break
				
            # print GetDisasm(head)
            if (mnem == "cmp"):
                cmp_op1 = replaceRegisters(getRegister(op1))
                cmp_op2 = replaceRegisters(getRegister(op2))
                cmp_blk = block
                #print cmp_op1 + ", " + cmp_op2

            elif (mnem == "mov"):
                if (isRegister(op1)):
                    op2 = replaceRegisters(op2)

                    if (op2[0] == '[' and op1 == "eax" and op2.find("eax") != -1):
                        setRegister(op1, op1)
                    else:
                        setRegister(op1, op2)
						
                else:
                    if (isRegister(op2)):
                        last = head
                        op1 = replaceRegisters(getRegister(op1))
                        op2 = replaceRegisters(getRegister(op2))

                        addNode(op1, op2)
                        #printRegisters()
						
            elif (mnem == "add"):
                setRegister(op1, op1 + "+" + op2)
            elif (mnem == "sub"):
                setRegister(op1, op1 + "-" + op2)
            elif (mnem == "shl"):
                valint = 1
                #valint = int(GetOperandValue(head, 1)) * 2
                valstr = str(valint)
                setRegister(op1, op1 + "*" + valstr)
            elif (mnem == "lea"):
                op2 = replaceRegisters(getRegister(op2))
                setRegister(op1, op2)


    if detected:
        print "Bubble Sort Detected : " + GetFunctionName(func.startEA)

        for e in G.E:
            if e.status is 2:
                #e.printEdge()
                #color_block(e.srcV.block, 0x0000FF)
                #color_block(e.dstV.block, 0x00FF00)
			
                if e.srcV.block.id is e.dstV.block.id:
                    for head in Heads(e.srcV.block.startEA, e.srcV.block.endEA):
                        SetColor(head, CIC_ITEM, 0xFF0000)
                else:
                    for head in Heads(e.srcV.block.startEA, e.srcV.block.endEA):
                        SetColor(head, CIC_ITEM, 0x0000FF)
                        
                    for head in Heads(e.dstV.block.startEA, e.dstV.block.endEA):
                        SetColor(head, CIC_ITEM, 0x00FF00)

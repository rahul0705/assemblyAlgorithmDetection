from itertools import chain
from graph import *

reg = {} #Store all the registers
graphy = {} #Magical Shit here
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

#From the magical land of the internet
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

def find_all_successor(fc, block, set=[]):
    for x in set:
        if x.id == block.id:
            return set
    set = set + [block]
    for succ_block in block.succs():
        set =  find_all_successor(fc, succ_block, set)
        
    return set


def find_loop_endings(fc, block, G, set=[]):
    for succ_blk in block.succs():
        id = succ_blk.id
        if (G.V[id].label == 1):
            set = set + [succ_blk]

        if (G.V[id].label != 2):
            set = find_loop_endings(fc, succ_blk, G, set)

    return set

def dominates(start, end, look, done = 0):
    
    for succ_blk in start.succs():
        ids = succ_blk.id
        if succ_blk.id == look.id:
            done = 1

        if (end.id == succ_blk.id):
            return True, done
    
        if (G.V[ids].label != 1):
            return dominates(succ_blk, end, look, done)

        return False, done

func = idaapi.get_func(idaapi.get_screen_ea())
fc = idaapi.FlowChart(func)

cmp_op1 = cmp_op2 = cmp_blk = None

G = graph(fc)
G.labelEdges(G.V[0], 1)

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
            #print op1 + " " + op2
            if (op1 != op2 and find_path(graphy, op1, op2) != None and find_path(graphy, op2, op1) != None):
                print "\nBLOCK: %x [%d]: Is a Swap" % (block.startEA, block.id)
                color_block(block, 0xAEBAEB)
                
                #printRegisters()
                #print GetDisasm(last)
                #print graphy
                
                if (cmp_op1 != cmp_op2 and graphy.has_key(cmp_op1) and graphy.has_key(cmp_op2)):
                    if (find_path(graphy, cmp_op1, cmp_op2) and find_path(graphy, cmp_op2, cmp_op1)):
                        color_block(cmp_blk, 0xCCFA38)

                        #Now that a compare and a swap has been found check if the swap is inside of two nested loops
                        loop_starts = []
                        loop_endings = find_loop_endings(fc, block, G)

                        for x in loop_endings:
                            for e in G.E:
                                if e.status is 2 and e.srcV.block.id == x.id:
                                    loop_starts = loop_starts + [e.dstV.block]

                        index = 0
                        for blk in loop_starts:
                            print "Starts Loop: %x [%d] -> Ends Loop:%x [%d]" % (loop_endings[index].startEA, loop_endings[index].id, blk.startEA, blk.id,)
                            index = index + 1



                        loopcount = 0
                        i = 0
                        for ends in loop_endings: 
                            flag = 1
                            failed = 0
                            for blk in block.succs():
                                tup = dominates(loop_starts[i], blk, block)
                                if (tup[1] == 1):
                                    flag = 0
                                    if (tup[0] == False):
                                        failed = 1

                            if flag == 0 and failed == 0:
                                loopcount = loopcount + 1
                        
                            i = i + 1

                        if (loopcount == 2):
                            print "Bubblesort Found\n"
                        
                        
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
                setRegister(op1, op2)
            else:
                if (isRegister(op2)):
                    last = head
                    op1 = replaceRegisters(getRegister(op1))
                    op2 = replaceRegisters(getRegister(op2))
                    #print graphy
                    #print "Adding Node Between" + op1 + " " + op2
                    addNode(op1, op2)
                    #printRegisters()
        elif (mnem == "add"):
            setRegister(op1, op1 + "+" + op2)
        elif (mnem == "sub"):
            setRegister(op1, op1 + "-" + op2)
        elif (mnem == "shl"):
            valint = int(op2) * 2
            valstr = str(valint)
            setRegister(op1, op1 + "*" + valstr)


for e in G.E:
    if e.status is 2:
        #e.printEdge()
        color_block(e.srcV.block, 0x0000FF)
        color_block(e.dstV.block, 0x00FF00)

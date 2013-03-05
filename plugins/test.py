print "\n--------------------\ntest.py has been started"


### Nmemonics histogram
    
mnemonics = dict()

# For each of the segments
for seg_ea in Segments():

    # For each of the defined elements
    for head in Heads(seg_ea, SegEnd(seg_ea)):


        # If it's an instruction
        if isCode(GetFlags(head)):
        
            # Get the mnemonic and increment the mnemonic
            # count
            mnem = GetMnem(head)
            mnemonics[mnem] = mnemonics.get(mnem, 0)+1

# Sort the mnemonics by number of occurrences
sorted = map(lambda x:(x[1], x[0]), mnemonics.items())
sorted.sort()


# Print the sorted list
for mnemonic, count in sorted:
    print mnemonic, count


print "test.py has completed\n--------------------\n"
Algorithm Detection in Binaries
==========================

An IDA Pro plugin for detecting algorithms in assembly


Plugin List:


    backedge.py - Labels all backedges in current functions. Colors start blocks green, and end blocks red
    bubble_sort_detector.py - Used to detect bubblesort in the entire program. Outputs if successful
    compare_func_sig.py - Comapres all functions to stored signatures
    compare_func_spp.py - Compare all functions to our SPP profiles
    create_func_sig.py -  Creates a signature for the current function
    create_func_spp.py - Creates an SPP value for the current function
    function.py - Function object used for SPP
    graph.py - Graph object to represent IDA graph with more detail
    match_blocks_spp.py - Match blocks for every function with our SPP block profiles
    reset_node_colors.py - Resets all node colors back to white
    signature.py - Signature object used for Signature Approach

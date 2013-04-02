class signature:
	def __init__(self):
		self.instr_count = {}
		self.edge_count = 0
		self.back_edge_count = 0
		self.block_count = 0
		
	def save(self):
		f = open("sig.txt", "w")
		
		for mnem in self.instr_count:
			f.write(mnem + " " + str(self.instr_count[mnem]) + "\n")
		
		f.write("INSTR_COUNT_DONE\n")
		
		f.write("edge_count " + str(self.edge_count) + "\n")
		f.write("back_edge_count " + str(self.back_edge_count) + "\n")
		f.write("block_count " + str(self.block_count) + "\n")
		
		f.close()
		
	def load(self):
		f = open("sig.txt", "r")
		lines = f.readlines()
		f.close()
		
		i = 0
		
		while lines[i] is not "INSTR_COUNT_DONE":
			words = split(lines[i])
			self.instr_count[words[0]] = int(words[1])
			i = i + 1
			
		i = i + 1
		words = split(lines[i])
		self.edge_count = int(words[0])
		
		i = i + 1
		words = split(lines[i])
		self.back_edge_count = int(words[0])
		
		i = i + 1
		words = split(lines[i])
		self.block_count = int(words[0])
		
	def printSig(self):
		print "__Instructions__"
		
		for mnem in self.instr_count:
			print "%s: %d" % (mnem, self.instr_count[mnem])
			
		print "__Edges__"
		print "Edge Count: %d" % self.edge_count
		print "Backedge Count: %d" % self.back_edge_count
		
		print "__Blocks__"
		print "Block count: %d" % self.block_count
from idaapi import *

DIR = "C:\\Users\\gbrinzea\\Desktop\\CS490PRE\\repo\\trunk\\plugins"

print "\n--------------------\ntest.py has been started"

os.chdir(DIR)

for file in os.listdir("signatures"):
	if file[0] != '.':
		print file

print "test.py has completed\n--------------------\n"
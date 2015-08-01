# Kelly Peterson
# LING 575
# simple script to find out all files in two directories which share a common line
# this is used to find email data with the same Message-ID in raw data that was annotated by two different universities

import sys
import os
# this is for (hopefully) portable file copying
import shutil

def FindLinesStartingWith(path, targetString):
	print('Starting to scan through path : ' + path)
	matches = {}
	for root, dirs, files in os.walk(path):
		for filename in files:
			print(filename)
			filePath = os.path.join(root, filename)
			file = open(filePath)
			for line in file:
				if line.startswith(targetString):
					print('Found starting line : [' + filePath + ']')
					matches[line] = filePath
	return matches
	
targetString = 'Message-ID:'
pathDictA = FindLinesStartingWith(sys.argv[1], targetString)
pathDictB = FindLinesStartingWith(sys.argv[2], targetString)

# do we want to copy the files which match?
copyFiles = 0
if len(sys.argv) > 3 and sys.argv[3] == '--copy':
	copyFiles = 1


print('*************')
print('Done reading files.  Finding files with matching lines...')
# now that we have these dictionaries, let's find which files are in common here...
for key, value in pathDictA.items():
	if key in pathDictB:
		print('match : [' + key + '], match : ' + value)
		if copyFiles == 1:
			# let's get a path that we can copy this to
			targetAbsPath = os.path.abspath(os.path.join('.', os.path.basename(value)))
			print('Copying file from ' + value + ' to ' + targetAbsPath)
			shutil.copy (value, targetAbsPath)
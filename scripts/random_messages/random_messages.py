# Kelly Peterson
# LING 575
# script to pull N random files from a certain directory and copy them to a new directory as long as they are long enough

import sys
import os
# this is for (hopefully) portable file copying
import shutil
import random

def RandomCopyFiles(sourceDir, targetDir, randomTotal, minLines, maxLines):
	print('Working to get random files in folder : ' + sourceDir)
	randomList = []
	for root, dirs, files in os.walk(sourceDir):
		for filename in files:
			file = open(os.path.join(root, filename), 'r')
			lineCount = 0
			header = 1
			
			# let's count up the lines...
			for line in file:
				line = line.strip()
				if line.startswith('********************************************'):
					header = 0
				elif header == 0:
					if len(line) > 0:
						lineCount = lineCount + 1
						
			# is this one long enough?
			if lineCount >= int(minLines) and lineCount <= int(maxLines):
				randomList.append(os.path.join(root, filename))
			
	# now let's randomize the list : 
	random.shuffle(randomList)
	count = 0
	while count < int(randomTotal):
		# let's get a path that we can copy this to
		print('Copying file number : ' + str(count) + ' of ' + str(randomTotal))
		randomFilePath = randomList[count]
		targetAbsPath = os.path.join(targetDir, os.path.basename(randomFilePath))
		print('Copying file from ' + randomFilePath + ' to ' + targetAbsPath)
		shutil.copy (randomFilePath, targetAbsPath)
		count = count + 1
		
		
if len(sys.argv) != 6:
	print('Usage : python random_messages.py [sourceDir] [targetDir] [randomN] [minLines] [maxLines]')
	exit(-1)
	
sourceDir = sys.argv[1]
targetDir = sys.argv[2]
randomTotal = sys.argv[3]
minLines = sys.argv[4]
maxLines = sys.argv[5]

if not os.path.exists(targetDir):
    os.makedirs(targetDir)
	
RandomCopyFiles(sourceDir, targetDir, randomTotal, minLines, maxLines)
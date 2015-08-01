# Kelly Peterson
# LING 575
# Script to read in a CSV of messageIDs and copy them to a new file name with one of the values in the CSV

import sys
import os
import string

import shutil

def GetFileCountFromPath(path):
	count = 0
	
	for root, dirs, files in os.walk(path):
		for filename in files:
			count += 1
			
	return count
	
def ReadCSVFileToDict(filename):
	dict = {}
	
	file = open(filename, 'r')
	
	for line in file:
		line = line.strip()
		tokens = line.split(',')
		if len(tokens) == 2:
			key = tokens[1]
			value = tokens[0]
			dict[key] = value
		else:
			print('WHOA!  Unexpected number of tokens')
		
	return dict
	
def CopyFilesByDict(sourceDir, targetDir, messageDict):
	totalFileCount = GetFileCountFromPath(sourceDir)
	print('Reading [' + str(totalFileCount) + '] files from : ' + sourceDir)
	
	# keep track of message IDs we've already copied so we don't do it twice...
	messagesCopied = {}
	
	messageIDString = 'Message-ID:'
	finalHeaderLines = ['X-FileName:', '**************************']
	
	currentFileCount = 0
	for root, dirs, files in os.walk(sourceDir):
		for filename in files:
		
			currentFileCount += 1
		
			if len(messagesCopied) == len(messageDict):
				print('Copying complete.  All message IDs were accounted for.')
			
			# now let's start reading the file
			filePath = os.path.join(root, filename)
			file = open(filePath, 'r')
			
			print('Reading file [' + str(currentFileCount) + '/' + str(totalFileCount) + '] : ' + filename) 
			
			for line in file:
				stopReading = 0
				for finalLine in finalHeaderLines:
					if line.startswith(finalLine):
						stopReading = 1
				if stopReading == 1:
					print('Finished reading the header and never found the messageID')
					break
				
				if line.startswith(messageIDString):
					messageID = line[len(messageIDString):].strip()
					if messageID not in messagesCopied:
						print('Copying messageID : ' + messageID)
						messagesCopied[messageID] = 1
						# copy the file using the value in the other dictionary
						if messageID in messageDict:
							shutil.copy (filePath, os.path.join(targetDir, messageDict[messageID] + '.txt'))
						else:
							print('ERROR : Message ID [' + messageID + '] was not found in the MySQL database!!!')
					else:
						break
	
if len(sys.argv) != 4:
	print('Usage : python copy_by_messageid.py [sourceDir] [csvFile] [targetDir]')
	sys.exit(-1)
	
sourceDir = sys.argv[1]
csvFile = sys.argv[2]
targetDir = sys.argv[3]

if not os.path.exists(targetDir):
	os.makedirs(targetDir)

messageDict = ReadCSVFileToDict(csvFile)
CopyFilesByDict(sourceDir, targetDir, messageDict)
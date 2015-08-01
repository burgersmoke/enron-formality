# Kelly Peterson
# LING 575
# Script to clean up all messages in a folder and save them to a new location

import sys
import os

def CleanFolder(sourcePath, targetPath):
	print('Working to clean mails in folder : ' + sourcePath)
	for root, dirs, files in os.walk(sourcePath):
		for filename in files:
			if '.cats' not in filename:
				sourceFilePath = os.path.join(root, filename)
				targetFilePath = os.path.join(targetPath, filename)
				CleanFile(sourceFilePath, targetFilePath)

def CleanFile(sourceFilePath, targetFilePath):
	print('Working on file : ' + sourceFilePath)
	
	# variable to keep track if we are still in the header
	header = 1
	
	sourceFile = open(sourceFilePath, 'r')
	targetFile = open(targetFilePath, 'w')
	
	# variables to help clean this up...
	finalHeaderLine = 'X-FileName:'
	allowedStartList = [ 'Message-ID:', 'Subject: ']
	terminateContainsList = ['-Original Message','- Forwarded by']
	
	# TODO : is there any way to filter out previous messages that have this form : 
	#Jay Reitmeyer/ENRON@enronXgate 08/23/2001 07:12 AM 	   To: Paul T Lucci/NA/Enron@Enron, Theresa Staab/Corp/Enron@ENRON, Tyrell Harrison/NA/Enron@Enron  
	# cc: Mark Whitt/NA/Enron@Enron  Subject: Rockies Fundamentals
	
	# NOTE : '<MARKUP ' is contained as markup in the PERSONAL VS BUSINESS emails
	terminateStartList = ['__________', '<MARKUP ', 'Return-path:', 'Return-Path:',  'Sent by:', 'Subject:', 'To:', 'to:', 'cc:', 'Cc']
	
	# start working through the lines
	for line in sourceFile:
		line = line.strip()
		if line.startswith(finalHeaderLine):
			targetFile.write('********************************************\n')
			header = 0
		elif header == 1:
			for allowedStart in allowedStartList:
				if line.startswith(allowedStart):
					targetFile.write(line + '\n')
		else:
			# let's see if this contains anything that we should use to mark the end of what we want...
			for terminate in terminateContainsList:
				if terminate in line:
					print('Contains terminate string : [' + line + ']')
					return
			# let's see if this starts with a different termination marker
			for terminate in terminateStartList:
				if line.startswith(terminate):
					print('Starts with terminate string : [' + line + ']')
					return
			# otherwise, if the contents are OK, let's write it out...
			targetFile.write(line + '\n')
	
if len(sys.argv) != 3:
	print('Usage : python clean_messages.py [sourceDir] [targetDir]')
	exit(-1)
	
sourceDir = sys.argv[1]
targetDir = sys.argv[2]
if not os.path.exists(targetDir):
    os.makedirs(targetDir)
	
CleanFolder(sourceDir, targetDir)
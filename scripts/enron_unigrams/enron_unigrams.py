# Kelly Peterson
# LING 575
# Simple script to get unigrams from raw Enron email messages

import sys
import os

# for tokenization
import nltk


wordDict = {}

def GetFileCountFromPath(path):
	count = 0
	
	for root, dirs, files in os.walk(path):
		for filename in files:
			count += 1
			
	return count
	
def ScrapeFile(dir, filename):
	# variable to keep track if we are still in the header
	header = 1
	finalHeaderLines = ['X-FileName:', '**************************']
	subjectLine = 'Subject:'
	sourceFile = open(os.path.join(dir, filename), 'r')
	for line in sourceFile:
		line = line.strip()
		if int(header) == 1 and line.startswith(subjectLine):
			subjectContents = line[len(subjectLine):].strip()
			#print('subject : ['  + subjectContents + ']')
			words = nltk.word_tokenize(subjectContents)
			for word in words:
				AddWord(word)
		elif header == 1:
			for finalHeaderLine in finalHeaderLines:
				if line.startswith(finalHeaderLine):
					header = 0
		elif int(header) == 0:
			words = nltk.word_tokenize(line)
			for word in words:
				AddWord(word)
			
def AddWord(word):
	if word.isalpha():
		word = word.lower()
		if word not in wordDict:
			wordDict[word] = 1
	
def ScrapeDir(path):
	print('Working to get scrape Wordnik info from files in folder : ' + sourceDir)
	
	totalFileCount = GetFileCountFromPath(path)
	
	print('About to start work on [' + str(totalFileCount) + '] files')
	
	fileCount = 0 
	for root, dirs, files in os.walk(path):
		for filename in files:
			fileCount += 1
			percent = int((fileCount / float(totalFileCount)) * 100)
			print('Working on File [' + str(fileCount) + '/' + str(totalFileCount) + '] (' + str(percent) + '%)')
			ScrapeFile(root, filename)
			
def WriteUnigramFile(outputFilename):
	outputFile = open(outputFilename, 'w')
	# let's sort these for quick lookups if needed
	sortedWords = wordDict.keys()
	sortedWords.sort()
	for word in sortedWords:
		outputFile.write(word + '\n')
	outputFile.close()
	
if len(sys.argv) != 3:
	print('Usage : python enron_unigrams.py [sourceDir] [outputFile]')
	exit(-1)
		
sourceDir = sys.argv[1]
outputFile = sys.argv[2]
	
ScrapeDir(sourceDir)
WriteUnigramFile(outputFile)
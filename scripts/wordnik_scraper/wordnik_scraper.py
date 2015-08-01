# Kelly Peterson
# LING 575
# Recursive scraper of unigrams definitions from Wordnik

import sys
import os

import wordnik
# for tokenization
import nltk

wordnik_client = wordnik.Wordnik(api_key="ab88a4a190f2ab375a40b0b0c5409582034389dd77022d8d0")
wordnik_sourceDictionary = 'ahd'

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
			
			# here is where we actually talk to wordnik...
			wordDef = wordnik_client.definitions(word, sourceDictionary=wordnik_sourceDictionary)
			#wordDef = 'WORD DEFINITION'
			
			# TODO -- if there is a 'headword' for this word (i.e. 'pisses' -> 'piss')
			# then maybe I should pull the definition for the headword ('piss') instead???
			
			# this could be 0, but let's put it in the dictionary anyway so we don't continue
			# to bother wordnik
			wordDict[word] = wordDef
	
def ScrapeDir(path):
	print('Working to get scrape Wordnik info from files in folder : ' + sourceDir)
	
	totalFileCount = GetFileCountFromPath(path)
	
	print('About to start work on [' + str(totalFileCount) + '] files')
	
	fileCount = 0 
	for root, dirs, files in os.walk(path):
		for filename in files:
			fileCount += 1
			print('Working on File [' + str(fileCount) + '/' + str(totalFileCount) + ']')
			ScrapeFile(root, filename)
			
def WriteFile(outputFilename):
	outputFile = open(outputFilename, 'w')
	# let's sort these for quick lookups if needed
	sortedWords = wordDict.keys()
	sortedWords.sort()
	for word in sortedWords:
		if len(wordDict[word]) > 0:
			outputFile.write(word + '=' + str(wordDict[word]) + '\n')
	outputFile.close()
	
if len(sys.argv) != 4:
	print('Usage : python wordnik_scraper.py [sourceDir] [outputFile] [wordnikSourceDictionary]')
	exit(-1)
		
sourceDir = sys.argv[1]
wordnik_sourceDictionary = sys.argv[2]
outputFile = sys.argv[3]
	
ScrapeDir(sourceDir)
WriteFile(outputFile + '.' + wordnik_sourceDictionary + '.txt')
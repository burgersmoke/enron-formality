# Kelly Peterson
# LING 575
# Script to pull definitions from a gram file (unigrams... maybe bigrams???) that was processing by another file...

import sys
import os

import wordnik
# for tokenization
import nltk

wordnik_client = wordnik.Wordnik(api_key="ab88a4a190f2ab375a40b0b0c5409582034389dd77022d8d0")
wordnik_sourceDictionary = 'ahd'

def GetFileCountFromPath(path):
	count = 0
	
	for root, dirs, files in os.walk(path):
		for filename in files:
			count += 1
			
	return count
	
def ReadGramFile(gramFilename, definitionFile, totalAccessLimit):
	wordDict = ReadDefFile(definitionFile)
	sourceFile = open(gramFilename, 'r')
	lines = sourceFile.readlines()
	currentWordCount = len(wordDict)
	currentAccessCount = 0
	for line in lines:
		word = line.strip()
		word = word.lower()
		# let's see if this is already present
		if word not in wordDict:
			currentWordCount += 1
			percent = int((currentWordCount / float(len(lines))) * 100)
			print('Working on gram [' + str(currentWordCount) + '/' + str(len(lines)) + '] (' + str(percent) + '%)')
			if not word.isalpha():		
				# add an empty def so we don't come back here again...
				wordDict[word] = []
			else:
				# here is where we actually talk to wordnik...
				wordDef = wordnik_client.definitions(word, sourceDictionary=wordnik_sourceDictionary)
				#wordDef = []
				
				currentAccessCount += 1
				
				# this could be length 0, but let's put it in the dictionary anyway so we don't continue
				# to bother wordnik again later
				wordDict[word] = wordDef
				
				if currentAccessCount >= totalAccessLimit:
					print('Done contacting Wordnik for now.  Reached max limit of : ' + str(totalAccessLimit))
					return wordDict
				
	return wordDict
	
def ReadDefFile(defFilename):
	wordDict = {}
	
	print('Attempting to read Definitions file : ' + defFilename)
	if not os.path.exists(defFilename):
		print('File does not exist yet, so starting fresh...')
		return wordDict
	file = open(defFilename, 'r')
	
	for line in file:
		line = line.strip()
		equalsIndex = line.find('=')
		word = line[:equalsIndex]
		wordDefString = line[equalsIndex+1:]
		wordDef = eval(wordDefString)
		wordDict[word] = wordDef
	return wordDict
	
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
			
def WriteFile(wordDict, outputFilename):
	outputFile = open(outputFilename, 'w')
	# let's sort these for quick lookups if needed
	sortedWords = wordDict.keys()
	sortedWords.sort()
	for word in sortedWords:
		# write the word and its definition
		outputFile.write(word + '=' + str(wordDict[word]) + '\n')
	outputFile.close()
	
if len(sys.argv) != 5:
	print('Usage : python wordnik_scraper.py [gramFile] [definitionFile] [wordnikSourceDictionary] [totalAccessLimit]')
	exit(-1)
		
gramFile = sys.argv[1]
wordnik_sourceDictionary = sys.argv[2]
definitionFile = sys.argv[3]
totalAccessLimit = int(sys.argv[4])
	
fullDefFilename = definitionFile + '.' + wordnik_sourceDictionary
wordDict = ReadGramFile(gramFile, fullDefFilename, totalAccessLimit)
WriteFile(wordDict, fullDefFilename)
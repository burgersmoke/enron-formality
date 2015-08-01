# Kelly Peterson
# LING 575
# Pulling certain labels out of enron 

import sys
import os

formalityDict = {}

formalityLabels = ['misspelling', 'colloquial', 'vulgar', 'offensive', 'eye dialect' ]
partsOfSpeech = ['interjection']
# some of these were returning ridiculous results...
#formalityLabels.append('informal')
#formalityLabels.append('slang')

def ReadFile(filename):
	file = open(filename, 'r')
	
	for line in file:
		line = line.strip()
		equalsIndex = line.find('=')
		word = line[:equalsIndex]
		print(word)
		wordDefString = line[equalsIndex+1:]
		wordDef = eval(wordDefString)
		tempLabelDict = {}
		tempPosDict = {}
		for defPart in wordDef:
			labelKey = 'labels'
			if labelKey in defPart:
				labelDict = defPart[labelKey]
				for labelEntry in labelDict:
					textKey = 'text'
					if textKey in labelEntry:
						labelText = labelEntry[textKey].lower()
						#print('LABEL TEXT ENTRY : ' + labelText)
						if labelText in formalityLabels:
							print('Adding label : ' + labelText)
							if labelText not in tempLabelDict:
								tempLabelDict[labelText] = 1
							else:
								tempLabelDict[labelText] += 1
			posKey = 'partOfSpeech'
			if posKey in defPart:
				pos = defPart[posKey]
				if pos in partsOfSpeech:
					if pos not in tempPosDict:
						tempPosDict[pos] = 1
					else:
						tempPosDict[pos] += 1
		# now that we have raw counts, let's see if they are significant enough...
		targetLabelCount = 0
		for label in tempLabelDict:
			targetLabelCount += tempLabelDict[label]
		labelThreshold = 0.5
		# see how many we saw over the total definitions
		actualRatio = targetLabelCount / float(len(wordDef))
		if actualRatio > labelThreshold:
			print('actual ratio : ' + str(actualRatio))
			if word not in formalityDict:
				# set up a new dictionary we can add labels to
				formalityDict[word] = {}
			for label in tempLabelDict:
				formalityDict[word][label] = 1
				
		# now let's see if any of our parts of speech are the same count as total definitions (unanimous voting)
		targetPosCount = 0
		for pos in tempPosDict:
			targetPosCount += tempPosDict[pos]
		
		posThreshold = 0.6
		# see how many we saw over the total definitions
		actualRatio = targetPosCount / float(len(wordDef))
		
		if actualRatio > posThreshold:
			if word not in formalityDict:
				# set up a new dictionary we can add labels to
				formalityDict[word] = {}
			for pos in tempPosDict:
				formalityDict[word][pos] = 1
			
def WriteDict(outputFilename):
	print('Writing to file : ' + outputFilename)
	outputFile = open(outputFilename, 'w')
	# let's sort these for quick lookups if needed
	sortedWords = formalityDict.keys()
	sortedWords.sort()
	for word in sortedWords:
		if len(formalityDict[word]) > 0:
			outputFile.write(word + '=' + str(formalityDict[word]) + '\n')
	outputFile.close()

if len(sys.argv) != 3:
	print('Usage : python wordnik_formality.py [sourceDir] [outputFile]')
	exit(-1)
			
sourceFile = sys.argv[1]
outputFile = sys.argv[2]

ReadFile(sourceFile)
WriteDict(outputFile)
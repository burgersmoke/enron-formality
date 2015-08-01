# Kelly Peterson
# LING 575
# Simple test of reading in a flat file of Wordnik data

import sys
import os

wordnikDict = {}

def ReadFile(filename):
	file = open(filename, 'r')
	
	for line in file:
		line = line.strip()
		tokens = line.split('=')
		if len(tokens) == 2:
			word = tokens[0]
			print(word)
			wordDef = eval(tokens[1])
			wordnikDict[word] = wordDef
			for defPart in wordnikDict[word]:
				labelKey = 'labels'
				if labelKey in defPart:
					labelDict = defPart[labelKey]
					for labelEntry in labelDict:
						textKey = 'text'
						if textKey in labelEntry:
							print('LABEL TEXT ENTRY : ' + labelEntry[textKey])
		else:
			print('WHOA!!  This definition couldnt parse properly with =')

sourceFile = sys.argv[1]

ReadFile(sourceFile)
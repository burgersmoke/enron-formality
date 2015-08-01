# Kelly Peterson
# LING 575
# script to find similarity of "interannotator agreement" by finding which files were placed in the same folders

import sys
import os
import csv

globalFileDict = {}

def CreateFileHashtable(path):
	fileDict = {}
	for root, dirs, files in os.walk(path):
		for filename in files:
			number = GetNumberFromFolderName(root)
			# print('File : ' + filename + ', number : ' + number)
			fileDict[filename] = int(number)
			globalFileDict[filename] = 1
	return fileDict


def GetNumberFromFolderName(folder):
	basename = os.path.basename(folder)
	number = basename.split('_')[0]
	return number

personDicts = []
personNames = []
outputFile = sys.argv[1]
csv = csv.writer(open(outputFile, "wb"), delimiter=',')

personIndex = 2
while personIndex < len(sys.argv):
	inputPath = sys.argv[personIndex]
	print('Working on folder : ' + inputPath)
	personDict = CreateFileHashtable(inputPath)
	personDicts.append(personDict)
	personNames.append(os.path.basename(inputPath))
	personIndex = personIndex + 1
	
header = ['filename']
for name in personNames:
	header.append(name)
header.append('Complete agreement')
header.append('Formality agreement')
csv.writerow(header)

totalRawVoteAgreements = 0
totalFormalityAgreements = 0
totalUnusableFiles = 0
for file in globalFileDict:
	fileRow = [file]
	fileVotes = []
	formalityVotes = {}
	rawVoteDisagreements = 0
	formalityDisagreements = 0
	fileUnusable = 0
	for personDict in personDicts:
		vote = personDict[file]
		fileRow.append(vote)
		
		# now let's look at broad formality
		if vote == 0:
			fileUnusable = 1
		elif vote == 1 or vote == 2:
			#informal
			formalityVotes[0] = 1
		else:
			#formal
			formalityVotes[1] = 1
		
		if len(fileVotes) > 0 and vote not in fileVotes:
			rawVoteDisagreements = rawVoteDisagreements + 1
		fileVotes.append(vote)
	
	# handle raw vote score column
	if rawVoteDisagreements == 0:
		totalRawVoteAgreements += 1
		fileRow.append(1)
	else:
		fileRow.append(0)
	
	# was there a vote for informal (0) and formal (1) in this round?
	if 0 in formalityVotes and 1 in formalityVotes:
		fileRow.append(0)
	else:
		fileRow.append(1)
		totalFormalityAgreements += 1
		
	totalUnusableFiles += fileUnusable
	
	csv.writerow(fileRow)
	
csv.writerow(['Total Unusable Files', totalUnusableFiles])
csv.writerow(['Total Raw Vote Agreements', totalRawVoteAgreements])
csv.writerow(['Total Formality Agreements', totalFormalityAgreements])
comparableFiles = len(globalFileDict) - totalUnusableFiles
print('Total comparable files : ' + str(comparableFiles))
rawVotePercent = totalRawVoteAgreements / float(comparableFiles)
formalityPercent = totalFormalityAgreements / float(comparableFiles)
csv.writerow(['Raw Vote Agreement %', rawVotePercent])
csv.writerow(['Formality Agreement %', formalityPercent])
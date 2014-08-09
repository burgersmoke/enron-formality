# Kelly Peterson
# LING 575
# Analysis of instances that were classified by Mallet

import sys
import os
import string
import time
import datetime

def ReadVectorLog(folder, filebasename):
	logDict = {}
	
	vectorLogDict = os.path.join(folder, 'vectorlogs')
	vectorFileName = os.path.join(vectorLogDict, filebasename + '.log')
	
	lineCountString = 'LineCount'
	featureString = 'Features'
	
	file = open(vectorFileName, 'r')
	for line in file:
		line = line.strip()
		if line.startswith(lineCountString):
			count = line.split('=')[1]
			logDict[lineCountString] = count
		elif line.startswith(featureString):
			features = line.split('=')[1]
			featureTokens = features.split()
			tokenIndex = 0
			totalFeatureCount = 0
			while tokenIndex < len(featureTokens):
				featureName = featureTokens[tokenIndex]
				featureValue = int(featureTokens[tokenIndex + 1])
				logDict[featureName] = featureValue
				totalFeatureCount += featureValue
				tokenIndex += 2
				
			logDict['FeatureCount'] = totalFeatureCount
	
	return logDict

def ReadClassifiedFile(classifiedFile):
	print('Reading Classified file : ' + classifiedFile)
	classifiedDict = {}
	file = open(classifiedFile, 'r')
	currentLineCount = 0
	for line in file:
		line = line.strip()
		
		if currentLineCount % 10000 == 0:
			print('Current Line processing : ' + str(currentLineCount))
			
		currentLineCount += 1
		
		tokens = line.split()
		if len(tokens) == 5 or len(tokens) == 6:
			key = tokens[0]
			bestLabel = tokens[2]
			
			# make sure this is even a classification
			if ':' in bestLabel:
				rawLabel = bestLabel.split(':')[0]
				#print(bestLabel)
				
				if rawLabel == 'FORMAL' or rawLabel == 'INFORMAL':
					# now let's look into the vectorlog file...
					slashTokens = key.split('/')
					filebasename = slashTokens[-1]
					classifyFolder = os.path.dirname(classifiedFile)
					logDict = ReadVectorLog(classifyFolder, filebasename)
					
					effectiveLabel = rawLabel
					if int(logDict['LineCount']) == 0:
						#print('Found an instance without lines.  Changing from [' + rawLabel + '] to EMPTY')
						effectiveLabel = 'EMPTY'
					elif logDict['FeatureCount'] == 0 and rawLabel == 'INFORMAL':
						print('Found an instance marked as informal without features...')
						effectiveLabel = 'FORMAL'
						
					logDict['EffectiveLabel'] = effectiveLabel
				else:
					logDict = {}
					
				# these get saved off regardless
				logDict['RawLabel'] = rawLabel
				classifiedDict[key] = logDict
			
	return classifiedDict
	
def WriteLog(classifiedDict, outputFilename):
	file = open(outputFilename, 'w')
	
	for key in classifiedDict:
		if 'EffectiveLabel' in classifiedDict[key]:
			file.write(key + ' ' + classifiedDict[key]['EffectiveLabel'] + '\n')
		elif 'RawLabel' in classifiedDict[key]:
			file.write(key + ' ' + classifiedDict[key]['RawLabel'] + '\n')
	
	file.close()
	
def WriteBaseFolderReport(classifiedDict, outputFilename):
	print('Writing a report of Base Folder count to : ' + outputFilename)
	file = open(outputFilename, 'w')
	
	baseFolderDict = {}
	file.write('Total instances : ' + str(len(classifiedDict)) + '\n')
	totalLabelDict = {}
	for instance in classifiedDict:
		slashTokens = instance.split('/')
		if len(slashTokens[0]) > 0:
			baseFolder = slashTokens[0]
		else:
			baseFolder = slashTokens[1]
		label = classifiedDict[instance]['EffectiveLabel']
		print('Base Folder : [' + baseFolder + '], label : [' + label + ']')
		if not baseFolder in baseFolderDict:
			baseFolderDict[baseFolder] = {}
		if not label in baseFolderDict[baseFolder]:
			baseFolderDict[baseFolder][label] = 1
		else:
			baseFolderDict[baseFolder][label] += 1
			
		if not label in totalLabelDict:
			totalLabelDict[label] = 1
		
	for baseFolder in baseFolderDict:
		baseFolderCount = 0
		for label in totalLabelDict:
			baseFolderCount += baseFolderDict[baseFolder][label]
			
		baseFolderDict[baseFolder]['TOTAL'] = baseFolderCount
		
	for baseFolder in baseFolderDict:
		baseFolderTotal = baseFolderDict[baseFolder]['TOTAL']
		for label in totalLabelDict:
			labelPercent = baseFolderDict[baseFolder][label] / float(baseFolderTotal)
			baseFolderDict[baseFolder][label + '_PERCENT'] = labelPercent
		
	for baseFolder in baseFolderDict:
		file.write(baseFolder + ' ' + str(baseFolderDict[baseFolder]) + '\n')
	
	file.close()

def WriteSQL(classifiedDict, outputFilename):
	print('Writing a SQL file to : ' + outputFilename)
	file = open(outputFilename, 'w')
	
	# this has problems when the table is not there
	#file.write("DROP TABLE `formality`;\n" )
	
	# let's find all of our possible columns...
	columnDict = {}
	for instanceName in classifiedDict:
		for key in classifiedDict[instanceName]:
			if key not in columnDict:
				print('Adding column : ' + key)
				columnDict[key] = 1
	
	tableString = "CREATE TABLE enron.`formality` (`mid` INT(10) NOT NULL DEFAULT '0'"
	for key in columnDict:
		tableString += ", `" + key + "` INT(10) NOT NULL DEFAULT '0'"
	tableString += ");\n"
	
	file.write(tableString )
	instanceCount = 1
	for instanceName in classifiedDict:
		
		# begin our initial string of column names...
		rowString = "INSERT INTO enron.formality (mid"
		# let's use the same order as the master column dict in writing this out
		for column in columnDict:
			rowString += "," + column
		
		tokens = instanceName.split('/')
		mid = tokens[-1].split('.')[0]
		
		#terminate the column names
		rowString += ") VALUES(" + str(mid)
		
		# now pull each value out of the classified version if it exists....
		for column in columnDict:
			if column in classifiedDict[instanceName]:
				columnValue = classifiedDict[instanceName][column]
				if column == 'EffectiveLabel' or column == 'RawLabel':
					if columnValue == 'FORMAL':
						columnValue = 1
					elif columnValue == 'INFORMAL':
						columnValue = 2
					elif columnValue == 'EMPTY':
						columnValue = 0
						
				rowString += "," + str(columnValue)
			else:
				rowString += ",0"
				
		rowString += ");\n"
		
		file.write(rowString)
		instanceCount += 1
	
	file.close()
	
def WriteSQLForRequests(classifiedDict, outputFilename):
	print('Writing a SQL file (for requests) to : ' + outputFilename)
	file = open(outputFilename, 'w')
	
	# let's find all of our possible columns...
	columnDict = {}
	for instanceName in classifiedDict:
		for key in classifiedDict[instanceName]:
			if key not in columnDict:
				print('Adding column : ' + key)
				columnDict[key] = 1
	
	tableString = "CREATE TABLE enron.`requests` (`mid` INT(10) NOT NULL DEFAULT '0'"
	for key in columnDict:
		tableString += ", `" + key + "` INT(10) NOT NULL DEFAULT '0'"
	tableString += ");\n"
	
	file.write(tableString )
	instanceCount = 1
	for instanceName in classifiedDict:
		# begin our initial string of column names...
		rowString = "INSERT INTO enron.requests (mid"
		# let's use the same order as the master column dict in writing this out
		for column in columnDict:
			rowString += "," + column
		
		tokens = instanceName.split('/')
		mid = tokens[-1].split('.')[0]
		
		#terminate the column names
		rowString += ") VALUES(" + str(mid)
		
		# now pull each value out of the classified version if it exists....
		for column in columnDict:
			if column in classifiedDict[instanceName]:
				columnValue = classifiedDict[instanceName][column]
				if column == 'EffectiveLabel' or column == 'RawLabel':
					if columnValue == 'NREQ':
						columnValue = 0
					elif columnValue == 'REQ':
						columnValue = 1
					else:
						print('Why did this not have an expected column name?')
						columnValue = 0
						
				rowString += "," + str(columnValue)
			else:
				rowString += ",0"
				
		rowString += ");\n"
		
		file.write(rowString)
		instanceCount += 1
	
	file.close()

if len(sys.argv) != 4:
	print('Usage : python classify_analysis.py [malletClassifiedFile] [reportType] [outputFile]')
	sys.exit(-1)
	
startTime = time.time()
	
classifiedFilename = sys.argv[1]
reportType = sys.argv[2]
outputFilename = sys.argv[3]

classifiedDict = ReadClassifiedFile(classifiedFilename)

WriteLog(classifiedDict, outputFilename + '.log')

if reportType == '--basefolder':
	WriteBaseFolderReport(classifiedDict, outputFilename)
elif reportType == '--sql':
	WriteSQL(classifiedDict, outputFilename)
elif reportType == '--sqlRequests':
	WriteSQLForRequests(classifiedDict, outputFilename)

elapsedSeconds = time.time() - startTime
print('Total runtime : ' + str(datetime.timedelta(seconds=elapsedSeconds)))

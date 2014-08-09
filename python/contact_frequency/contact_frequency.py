# Kelly Peterson
# Ling 575
# Getting 1:1 contact frequency and formality

import os 
import sys

def GetOneToOneContact(file):
	one_on_one_dict = {}
	
	outputFile = open(file, 'r')
	
	contactMax = 0
	for line in outputFile:
		line = line.strip()
		tokens = line.split(',')
		
		contactKey = tokens[0] + '_' + tokens[1]
		
		# make sure that they are both from Enron...
		
		#if 'enron.com' in tokens[0] and 'enron.com' in tokens[1]:
		if '.' in tokens[0] and '.' in tokens[1]:
			
			if 'no.address@enron.com' not in contactKey and 'enron.announcements@enron.com'  not in contactKey and 'all.worldwide@enron.com' not in contactKey and '40enron@enron.com' not in contactKey and 'All Enron Worldwide' not in contactKey:
				if contactKey not in one_on_one_dict:
					one_on_one_dict[contactKey] = {}
				
				formalityKey = 'INFORMAL'
				if int(tokens[2]) == 1:
					formalityKey = 'FORMAL'
					
				if formalityKey not in one_on_one_dict[contactKey]:
					one_on_one_dict[contactKey][formalityKey] = 1
				else:
					one_on_one_dict[contactKey][formalityKey] += 1
		
	return one_on_one_dict

csvFile = sys.argv[1]
one_on_one_dict = GetOneToOneContact(csvFile)

print 'Total sender to recipient pairs : %d' % (len(one_on_one_dict))

contactMax = 0
maxContactKey = ''
for contactKey in one_on_one_dict:
	contactCount = 0
	for countKey in one_on_one_dict[contactKey]:
		contactCount += one_on_one_dict[contactKey][countKey]
		
	one_on_one_dict[contactKey]['TOTAL'] = contactCount
		
	if contactCount > contactMax:
		contactMax = contactCount
		maxContactKey = contactKey
	
print 'Max Contacts is %d from the pair %s' % (contactMax, maxContactKey)

groupDict = {}

groupingKeys = [1, 5, 10, 20, 50, 100]
for groupingKey in groupingKeys:
	groupDict[groupingKey] = {'FORMAL':0, 'INFORMAL':0, 'PAIRS':0}

freqDict = {}
for contactKey in one_on_one_dict:
	contactTotal = one_on_one_dict[contactKey]['TOTAL']
	
	# filter out the smallest number of contacts
	groupKey = groupingKeys[0]
	if contactTotal > 0:
		for checkGroupingKey in groupingKeys:
			if contactTotal > checkGroupingKey:
				groupKey = checkGroupingKey
			
		if contactTotal not in freqDict:
			freqDict[contactTotal] = {'FORMAL':0, 'INFORMAL':0}
			
		# count up the pairs in this group...
		groupDict[groupKey]['PAIRS'] += 1
			
		if 'FORMAL' in one_on_one_dict[contactKey]:
			groupDict[groupKey]['FORMAL'] += one_on_one_dict[contactKey]['FORMAL']
			freqDict[contactTotal]['FORMAL'] += one_on_one_dict[contactKey]['FORMAL']
			
		if 'INFORMAL' in one_on_one_dict[contactKey]:
			groupDict[groupKey]['INFORMAL'] += one_on_one_dict[contactKey]['INFORMAL']
			freqDict[contactTotal]['INFORMAL'] += one_on_one_dict[contactKey]['INFORMAL']
		
		groupDict[groupKey]['INFORMAL_RATE'] = groupDict[groupKey]['INFORMAL'] / float(groupDict[groupKey]['INFORMAL'] + groupDict[groupKey]['FORMAL'])
		freqDict[contactTotal]['INFORMAL_RATE'] = freqDict[contactTotal]['INFORMAL'] / float(freqDict[contactTotal]['INFORMAL'] + freqDict[contactTotal]['FORMAL'])

outputCSV = open('count_informality_rates.csv', 'w')
for i in range(contactMax):
	if i in freqDict:
		outputLine = '%d,%f\n' % (i, freqDict[i]['INFORMAL_RATE'])
		outputCSV.write(outputLine)
		
outputCSV.close()
		
for groupingKey in groupingKeys:
	print '%d : %s' % (groupingKey, groupDict[groupingKey])
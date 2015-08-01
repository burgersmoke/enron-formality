# Kelly Peterson
# LING 575
# Software system to write out feature vectors to classify Formality of email communication

import sys
import os
import string

import nltk

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

formalWordDict = {}

# this reads in the dictionary of formal\informal words from wordnik data
def ReadFormalWordDictionary(filename):
	file = open(filename, 'r')
	for line in file:
		line = line.strip()
		tokens = line.split('=')
		if len(tokens) == 2:
			word = tokens[0]
			wordDict = eval(tokens[1])
			formalWordDict[word] = wordDict
			
def GetFileCountFromPath(path):
	count = 0
	
	for root, dirs, files in os.walk(path):
		for filename in files:
			count += 1
			
	return count

class FeatureVector:
	def __init__(self, instanceName, label):
		self.instanceName = instanceName
		self.label = label
		self.featureDict = {}
		logDir = 'vectorlogs/'
		if not os.path.exists(logDir):
			os.makedirs(logDir)
		self.logFile = open(os.path.join(logDir, self.instanceName) + '.log', 'w')
	
	def WriteToFile(self, file):
		file.write(self.instanceName + ' ' + self.label + ' ')
		# now let's write all the features
		for feature in self.featureDict:
			file.write(feature + ' ' + str(self.featureDict[feature]) + ' ')
		file.write('\n')
		
	def AddFeature(self, feature, count):	
		if int(count) > 0:
			if feature not in self.featureDict:
				self.featureDict[feature] = count
			else:
				self.featureDict[feature] += count
				
	def AddLogLine(self, line):
		self.logFile.write(line + '\n')
		
def CaptureWordFeatures(vector, word):
	# there are some acrynoms in all caps that we don't want to mark as informal
	if not word.isupper():
		word = word.lower()
		if word in formalWordDict:
			for label in formalWordDict[word]:
				# NOTE : Changing this to be 'InformalWord' with a count of 1 jumped the MaxEnt accuracy from 74% to 85%
				vector.AddFeature('InformalWord', 1)
				
				# add the count of each label as a feature count
				#vector.AddFeature(label, formalWordDict[word][label])
		
def CapturePunctuationFeatures(vector, line):
	#ellipsis
	ellipsesCount = line.count('...')
	vector.AddFeature('Ellipses', ellipsesCount)
	#some people type it out like this
	altEllipsesCount = line.count('. . .')
	vector.AddFeature('Ellipses', altEllipsesCount)
	#exclamation
	exclamationCount = line.count('!')
	vector.AddFeature('Exclamation', exclamationCount)
	# let's capture multiple question marks
	multipleQuestionCount = line.count('??')
	vector.AddFeature('MultipleQuestion', multipleQuestionCount)
	
def CaptureSentenceFeatures(vector, sentence):

	words = nltk.word_tokenize(sentence)

	if len(words) > 2:
		# let's see if this sentence starts as lowercase
		if sentence[0].islower() :
			vector.AddFeature('LowercaseStartSentence', 1)
		
		if sentence.islower():
			vector.AddFeature('LowercaseEntireSentence', 1)
			
	nonAlphaCharacters = 0
	for char in sentence:
		if not char.isalpha() and not char.isspace() and not char in string.punctuation:
			nonAlphaCharacters += 1
			
	vector.AddLogLine('Sentence : [' + sentence + ']')
			
	# make sure this ends with valid punctuation
	if sentence[-1] == '.' or sentence[-1] == '?' or sentence[-1] == '!':
		# ok, this is not very pretty, but there are lots of "SENTENCES" which are full of URLs, phone numbers, etc
		# so let's only try to do sentence parses when we have very few of these...
		if nonAlphaCharacters < 2 and len(words) > 2:
			vector.AddLogLine('Testing for a parse...')
		
def ProcessLine(vector, line):
	CapturePunctuationFeatures(vector, line)
	# now let's tokenize this for words and work on each word...
	words = nltk.word_tokenize(line)
	for word in words:
		CaptureWordFeatures(vector, word)

def ReadFeatureVectors(path):
	featureVectors = []
	
	totalFileCount = GetFileCountFromPath(path)
	print('About to start writing vectors for [' + str(totalFileCount) + '] files')
	currentFileCount = 0
	
	for root, dirs, files in os.walk(path):
		for filename in files:
			label = os.path.basename(root)
			vector = FeatureVector(filename, label)
			featureVectors.append(vector)
			
			# now let's start reading the file
			filePath = os.path.join(root, filename)
			file = open(filePath, 'r')
			nltkRaw = nltk.data.load( 'file:' + filePath, 'raw' )
			
			terminateStartList = ['___', '>', '<MARKUP ', 'From:', 'Return-path:', 'Return-Path:',  'Sent by:', 'Subject:', 'To:', 'to:', 'cc:', 'Cc']
			terminateContainsList = ['-Original Message','- Forwarded by']
			
			currentFileCount += 1
			print('Working on file [' + str(currentFileCount) + '/' + str(totalFileCount) + '] -> ' + filename)
			
			# variable to keep track if we are still in the header
			header = 1
			finalHeaderLines = ['X-FileName:', '**************************']
			subjectLine = 'Subject:'
			
			# this is a list of lines which are not separated by blank lines
			lineBlocks = []
			currentLineBlock = ''
			
			for line in file:
				line = line.strip()
				
				if int(header) == 1 and line.startswith(subjectLine):
					subjectContents = line[len(subjectLine):].strip()
					ProcessLine(vector, subjectContents)
					
					# let's do any subject-specific features...
					if subjectContents.islower():
						vector.AddFeature('LowerCaseSubject', 1)
				elif header == 1:
					for finalHeaderLine in finalHeaderLines:
						if line.startswith(finalHeaderLine):
							header = 0
				elif int(header) == 0:
					# before we process, let's see if this message contains noise from a previous message...
					keepProcessing = 1
					for terminate in terminateContainsList:
						if terminate in line:
							print('Contains terminate string : [' + line + ']')
							keepProcessing = 0
					# let's see if this starts with a different termination marker
					for terminate in terminateStartList:
						if line.startswith(terminate):
							print('Starts with terminate string : [' + line + ']')
							keepProcessing = 0
							
					if keepProcessing == 0:
						break
					
					ProcessLine(vector, line)
					
					# terminate the current block if it's empty or if it ends with punctuation
					if len(line) == 0 or line[-1] == ',' or line[-1] == '-' or line[-1] == '!' or line[-1] == '?':
						currentLineBlock += line + ' '
						# add this block to the list of blocks as long as it has something in it
						if len(currentLineBlock) > 0:
							lineBlocks.append(currentLineBlock)
						currentLineBlock = ''
					else:
						# add to the current block
						currentLineBlock += line + ' '
					
					# NOTE : Accuracy went down pretty far when adding these...
					# let's count empty and non-empty lines
					#if len(line) == 0:
					#	vector.AddFeature('EmptyLines', 1)
					#else:
					#	vector.AddFeature('NonEmptyLines', 1)
				
			# only try to get sentence breaks from line blocks
			sentenceCount = 0
			for lineBlock in lineBlocks:
				lineBlock = lineBlock.strip()
				sentences = nltk.sent_tokenize(lineBlock)
				for sentence in sentences:
					if len(sentence) > 0:
						sentenceCount += 1
						CaptureSentenceFeatures(vector, sentence)
						
			if sentenceCount == 1:
				vector.AddFeature('OneSentence', 1)
					
			print('Line Block Count : [' + str(len(lineBlocks)) + '], SentenceCount : [' + str(sentenceCount) + ']')
				
	return featureVectors

if len(sys.argv) != 4:
	print('Usage : python furcoat.py [sourceDir] [formalWordsFile] [customWordsFile]')
	sys.exit(-1)
	
sourcePath = sys.argv[1]
formalWordsFile = sys.argv[2]
customWordsFile = sys.argv[3]
#trainingPercent = float(sys.argv[3])

ReadFormalWordDictionary(formalWordsFile)
ReadFormalWordDictionary(customWordsFile)

vectors = ReadFeatureVectors(sourcePath)

# sort these by instance name so that hopefully we get a good mix of each label in training\test
vectors = sorted(vectors, key=lambda FeatureVector: FeatureVector.instanceName)

if len(sys.argv) == 5:
	trainFile = open('training.vectors.txt', 'w')
	testFile = open('test.vectors.txt', 'w')
else:
	trainingPercent = 1.0
	trainFile = open('all.vectors.txt', 'w')

count = 0
testLimit = len(vectors) * trainingPercent
while count < len(vectors):
	if count < testLimit:
		vectors[count].WriteToFile(trainFile)
	else:
		vectors[count].WriteToFile(testFile)
	count += 1
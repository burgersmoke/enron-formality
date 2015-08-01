# Kelly Peterson
# LING 575
# Simple test of the Wordnik client in Python

import sys
import os
import pprint

import wordnik

pp = pprint.PrettyPrinter(indent=4)

wordnik_client = wordnik.Wordnik(api_key="ab88a4a190f2ab375a40b0b0c5409582034389dd77022d8d0")
#wotd = wordnik_client.word_of_the_day()
#print('*******************')
#print('WORD OF THE DAY')
#print(wotd)
#print('*******************')
input = raw_input('What word would you like to look up? ')
print('Looking up : ' + input + '...')
myword = wordnik_client.word(input)
print(myword)
mydef = wordnik_client.definitions(input, sourceDictionary='wiktionary')
#mydef = wordnik_client.definitions(input, sourceDictionary='ahd')
pp.pprint(mydef)
#encoding=utf-8

import sys
import urllib
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
import pickle
import itertools
import time


def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            #filename = file
            #print filename
            document = open(os.path.join(root, file)).read() # read the entire document, as one big string
            yield document # or whatever tokenization suits you

def set_FakeListToStore(ehowdir,cheat = True):
#""" chating and suck coding  ... Ouput: {'airplane' or 'comic' or 'drama':{A or B: words}} """
	eHowNetRef = [line.split() for line in iter_documents(ehowdir)]
	eHowNetRef1 = [line.replace('\ufeff',"").split() for line in iter_documents(ehowdir)]
	print " this is eHowNetRef .... "
	print eHowNetRef
	print eHowNetRef1
	try:
		with open('data/NEWehownet.pickle', 'wb') as ehw:
			pickle.dump(eHowNetRef, ehw)
	except IOError as ioerr:	
		print('File error (put_and_store): ' + str(ioerr))

def get_FakeListToStore(cheat = True, index = 'airplane'):
	try:
		with open('data/NEWehownet.pickle', 'rb') as ehw:
			eHowNetRef = pickle.load(ehw)
	except IOError as ioerr:
		print('File error (get_from_store): ' + str(ioerr))

	return (eHowNetRef)

def recursiveFindAllCombinations(listA,listB):
	result = list(itertools.product(listA,listB))
	return result 
	
def joinAllWordAsQuery(recursiveResults):
	l1 = []
	for i in recursiveResults:
		q = ''.join(str(e) for e in i)
		l1.append(q)
	return l1

def get_allExpannedQueryFromStore(SQ):
	eHowNetRefList = get_FakeListToStore()
	#print eHowNetRefList
	SQ  = [line.strip() for line in SQ if line != '\n' ]
	print "SQ"
	print SQ
	tempPos0 = []
	tempPos1 = []
	for lis in eHowNetRefList:
		#print eHowNetRefList
		if any(SQ[0] in s.decode("utf-8") for s in lis):
			tempPos0 = lis
		elif any(SQ[1] in s.decode("utf-8") for s in lis):
			tempPos1 = lis
	result = recursiveFindAllCombinations(tempPos0,tempPos1)
	if result: # found it 
		print "Found it in ehownet!"
		flag = True
		combinedQueryList = joinAllWordAsQuery(result)
		print " this is conbined list .... "
		print combinedQueryList
		return combinedQueryList
	else:
		print "term is not found in ehownet!!!!"
		return None
	#print tempPos1
	
	
	
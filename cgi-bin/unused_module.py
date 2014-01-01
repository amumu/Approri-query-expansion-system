##################################################################################
#                                                                                #
#  Copyright (c) 2013 Yao Nien, Yang, paulyang0125@gmail.com                     #  
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not   #
#  use this file except in compliance with the License. You may obtain a copy    #
#  of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless required #
#  by applicable law or agreed to in writing, software distributed under the     #
#  License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS  #
#  OF ANY KIND, either express or implied. See the License for the specific      #
#  language governing permissions and limitations under the License.             # 
#                                                                                #
##################################################################################


import os, sys, inspect

####### unused modules from controller2 ######

def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            #filename = file
            #print filename
            document = open(os.path.join(root, file)).read() # read the entire document, as one big string
            yield document # or whatever tokenization suits you

def set_FakeListToStore(cheat = True):
#""" chating and suck coding  ... Ouput: {'airplane' or 'comic' or 'drama':{A or B: words}} """
	eHowNetRef = [line.split() for line in iter_documents(ehowdir)]
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
	print eHowNetRefList
	SQ  = [line.strip() for line in SQ ]
	print "SQ"
	print SQ
	tempPos0 = []
	tempPos1 = []
	for lis in eHowNetRefList:
		if any(SQ[0] in s for s in lis):
			tempPos0 = lis
		elif any(SQ[1] in s for s in lis):
			tempPos1 = lis
	rResult = recursiveFindAllCombinations(tempPos0,tempPos1)
	print "RrESULT"
	print rResult
	combinedQueryList = joinAllWordAsQuery(rResult)
	return combinedQueryList
	
def getDisplayResult(which_page,dicOfAllPagesOfAQuery):
	titles = myquerypaser.dicOfAllPagesOfAQuery[which_page]['titles']
	contents = dicOfAllPagesOfAQuery[which_page]['contents']
	url = dicOfAllPagesOfAQuery[which_page]['url']
	return titles, contents, url
	
def prepareSegDataForAprori(webQuerryResultPerQuery):
	ctListPerQuery = myquerypaser.jsonPaserForOneQuery(webQuerryResultPerQuery, mergeCTResult = True)
	segCTStingListPerQuery = segQuery.segmentCTListPerQuerys(ctListPerQuery)
	return segCTStingListPerQuery


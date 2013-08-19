#! /usr/local/bin/python3
import cgitb
cgitb.enable()
import sys
import cgi 
import urllib
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
import yate
import markup
import pickle
import itertools
import time
import myquerypaser
#import chineseseg
import sql_webModel
import ehownet




#######

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


	
##### global paratermters #######

myDB = 'final.sqlite'
the_url = 'controller3.py'
# CGI parameter passing 
form_data = cgi.FieldStorage()
term = form_data['terms'].value
print(yate.start_response())
print(yate.include_header("Aprori Page for " + str(term)))

####### controller process #############


#segQuery = chineseseg.segmentToListPerQuery(term)
#s = [s.encode("utf-8") for s in segQuery] 
### render segmented results #### 
#segmentedQuery = segQuery.segmentToListPerQuery(term)
#print(yate.para("These are segmented query: "))
#print ("<h1>" +  str(segQuery) + "<h1>")
#s = ' '.join(segQuery.encode("utf-8")
#print(yate.u_list(s))

#### get expanded word from SQL, render them and pass through input method to controller 3  



if sql_webModel.checkIfdataIsStore(term.decode("utf-8"),myDB): ## found it in DB
	# this should get from SQL, NOT ehownet.... 
	#expandedQueriesPerDemoList = ehownet.get_allExpannedQueryFromStore(term.decode('utf-8'))
	expandedQueriesPerDemoList =  sql_webModel.get_expannedQueryFromStore(term.decode('utf-8'),myDB)
	
	#print ("<h1>" +  str(expandedQueriesPerDemoList) + "<h1>")
	d = [s.encode("utf-8") for s in expandedQueriesPerDemoList] 
	### render eexpanded word results #### 
	print('<h2>' + "these are the expanded queries from eHownet" +'</h2>')
	print ('</br>')
	print(yate.u_list(d))
	print(yate.start_form(the_url, form_type="POST"))
	for each_word in expandedQueriesPerDemoList:
		print(yate.hidden_input('expanded_terms_array', each_word.encode("utf-8")))
	print(yate.end_form())
	print ('</br>')
	print(yate.include_footer({"Cancel, go back to Google": "/index.html"}))
	#print(yate.include_menu1({"cancel, go back to Google": "/index.html"}, str(term) ))
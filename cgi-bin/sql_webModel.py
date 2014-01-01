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

﻿#encoding=utf-8
import sqlite3
#import segQuery
import ModifiedGoogleSearch
import itertools
import glob
import re, string
import pickle 
from itertools import izip
import string 
import logging


####### GOLABL PARAMETERS ####################3
#db_name = 'myquery1.sqlite'
eHownetMapping = '../data/mapping.conf'
cheatFakeAll = '../data/ehownet/'
airplaneRef = '../data/ehownet/airplane/'
comicRef = '../data/ehownet/comic/'
dramaRef = '../data/ehownet/drama/'

########### logging init ############
logger = logging.getLogger('myapp')
logger.info('sql_webModel.py started')



######### init ##############


############  NORMAL GOOGLE QUERY #################### 

## controller passes the cgi "which_query" to model file: ModififedGoogleSearch.py 
## 

### First table(query): id, query_name
###	Second table(expand_words): id, qid, expand_word,
### third table(query_results): eq_id , titles, contents, url, ct_contents,ruleset, rule_num, contain_flag


######for client #############
def get_googleResult_forClient(userQuery, multipleQuery = False):
	if multipleQuery == False:
#""" Input: query String (which_query) from google-search bar """
# output: a list of JSONs containing each page result FOR ONE QUERY [[ONE PAGE - JSON],[ONE PAGE - JSON]]
		firstQuery = ModifiedGoogleSearch.pygoogle(userQuery)
		failedQuery = userQuery
		firstQuery.pages = 3
		firstQuery.display_results()
		#print '*Found %s results*'%(firstQuery.get_result_count())
		#set_original_googleResultToSql(firstQuery)
		#return firstQuery.containerForAllData, firstQuery.containerForFailedData # return if not 200, and reply the list of the failed queries.
		if firstQuery.found:
			failedQuery = None
		return firstQuery.containerForAllData, firstQuery.found, failedQuery # temp ver for one page 
		
######for server #############
def get_googleResult_forServer(userQuery, multipleQuery = False):
	if multipleQuery == False:
#""" Input: query String (which_query) from google-search bar """
# output: a list of JSONs containing each page result FOR ONE QUERY [[ONE PAGE - JSON],[ONE PAGE - JSON]]
		firstQuery = ModifiedGoogleSearch.pygoogle(userQuery)
		failedQuery = userQuery
		firstQuery.pages = 3
		firstQuery.display_results()
		if firstQuery.found:
			failedQuery = None
		return firstQuery.containerForAllData, firstQuery.found, failedQuery # temp ver for one page 

def checkIfdataIsStore(query,db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	flag = False
	#try:
	#results = cursor.execute("SELECT qid FROM expand_words WHERE expand_word LIKE ?", (query,))
	#print "for debug" 
	#print type(query)
	#query
	logger.debug("query : ")
	logger.debug(query)
	results = cursor.execute("SELECT qid FROM expand_words WHERE expand_word = ?", (query,))
	#results1 = cursor.execute("SELECT expand_word FROM expand_words")
	response = results.fetchall()
	#print "response : "
	#print response 
	logger.debug("response : ")
	logger.debug(response)
	#print "all"
	if len(response) == 0:
		#print ( "\n")
		#print ( query + " is not found in DB, prepare to query!")
		return flag # return false if not found...  
	else: # return True if it is found 
		flag = True
		return flag 
	
	#except sqlite3.Error:
	#	print ("Error: unable to fecth data due to " + str(sqlite3.Error))
	
def getExistedQIDFromStore(query,db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	#try:
	#get qid to index the value in table 2, 3 ,4
	results = cursor.execute("SELECT qid FROM expand_words WHERE expand_word = ? ", (query,))
	print "existed QID : "
	print results
	qid = results.fetchone()[0]
	#return qid[0]
	return qid
	#except sqlite3.Error:
	#	print ("Error: unable to fecth data due to " + str(sqlite3.Error))

	
def getExistedIDFromStore(query,db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	#try:
	#get qid to index the value in table 2, 3 ,4
	results = cursor.execute("SELECT id FROM expand_words WHERE expand_word = ? ", (query,))
	#print "existed QID : "
	#print results
	id = results.fetchone()[0]
	#return qid[0]
	return id
	#except sqlite3.Error:
	#	print ("Error: unable to fecth data due to " + str(sqlite3.Error))
	
	
def get_theFlagFromAproriByEqid(eqid,db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT contain_flag FROM aprori_data WHERE eq_id = ? ", (eqid,))
	flag = results.fetchone()[0]
	return flag

	
def get_verboseInfoForCandidateByEqid(eqid,db_name): # create {"C1":{'BOW':?,'Dic':?,'Rules':?,'tag':?,'segCT':?},C2:{}} 
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT BOW,dictionary,rule_num, id FROM aprori_data WHERE eq_id = ? ", (eqid,))
	response = results.fetchone()
	BOW = response[0]
	dictionary = response[1]
	rule_num = response[2]
	id = response[3]
	results = cursor.execute("SELECT min_support,min_confidence FROM aprori_ruleResults WHERE a_id = ? ", (id,))
	min_support = results.fetchone()[0]
	min_confidence = results.fetchone()[1]
	results1 = cursor.execute("SELECT leftHand, rightHand, conf FROM aprori_ruleResults WHERE a_id = ? ", (id,))
	leftHand = [row[0] for row in results1.fetchall()]
	results1 = cursor.execute("SELECT leftHand, rightHand, conf FROM aprori_ruleResults WHERE a_id = ? ", (id,))
	rightHand = [row[1] for row in results1.fetchall()]
	results1 = cursor.execute("SELECT leftHand, rightHand, conf FROM aprori_ruleResults WHERE a_id = ? ", (id,))
	conf = [row[2] for row in results1.fetchall()]
	mixData = {'min_support':   min_support,
                'min_confidence':    min_confidence,
                'leftHand':   leftHand,
                'rightHand':   rightHand,
				'BOW':   BOW,
				'dictionary':   dictionary,
				'rule_num':   rule_num, 
				'conf':   conf}
	return(mixData)
				
	
	
	
def initFirstTable(query, expandedQueriesPerDemoList, db_name): 
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	#try:
	cursor.execute("INSERT INTO query (query_name) VALUES (?)", (query,))
	connection.commit()
	results = cursor.execute("SELECT id from query WHERE query_name = ?", (query,))
	print results
	the_current_id = results.fetchone()[0]
	print "the_current_id"
	print the_current_id
	print "expandedQueriesPerDemoList"
	print expandedQueriesPerDemoList
	for each_q in expandedQueriesPerDemoList:
		a = each_q.translate(None, string.punctuation)
		a = a.rstrip('\r\n')
		#cursor.execute("INSERT INTO expand_words(qid, expand_word) VALUES (?,?)", (the_current_id, each_q.decode("utf-8")))
		cursor.execute("INSERT INTO expand_words(qid, expand_word) VALUES (?,?)", (the_current_id, a.decode('utf-8-sig')))
		print "each_q's type:"
		print type(each_q)
		print each_q
		print each_q.decode("utf-8")
	connection.commit()
	#except sqlite3.Error:
	#	print ("Error: unable to fecth data due to " + str(sqlite3.Error))
	#finally:
	connection.close()

def get_expandedQueriesAndID_by_name(queryname, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	# get id from table 
	results = cursor.execute("SELECT id from query WHERE query_name = ?", (queryname,))
	the_current_id = results.fetchone()[0]
	results1 = cursor.execute("SELECT id, expand_word from expand_words WHERE qid = ?", (the_current_id,))
	response = results1.fetchall()
	#id_table2 = [row[0] for row in results.fetchall()]
	#expandWords = [row[1] for row in results.fetchall()]
	#response = {'qid':   the_current_id,
     #           'expandWords':  data}
	return response # response = [[id,expand_word],[id,expand_word],[id,expand_word]...n]

def get_expannedQueryByQID(eqid, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT expand_word from expand_words WHERE id = ?", (eqid,))
	expandedWord = results.fetchone()[0]
	return expandedWord
	
def get_expannedQueryFromStore(queryname, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT qid from expand_words WHERE expand_word = ?", (queryname,))
	the_current_qid = results.fetchone()[0]
	results = cursor.execute("SELECT expand_word from expand_words WHERE qid = ?", (the_current_qid,))
	expanded_wordsList = [row[0] for row in results.fetchall()]
	return expanded_wordsList
	
	
#third table(query_results): eq_id , titles, contents, url, 
#fourth table(ctContents): eq_id, ct_contents,ruleset, rule_num, contain_flag
# resultsPerExpandWord =  {page(0 - n):{'titles':[t1, t2, t3....etc], 'contents':[c1, c2, c3....etc], 'urls': [u1, u2, u3]}}
def initSecondTable(table2ID, expandWord, resultsPerExpandWord, segCTList, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	for page in resultsPerExpandWord.keys():
		for t, c, u in zip(resultsPerExpandWord[page]['titles'],resultsPerExpandWord[page]['contents'],resultsPerExpandWord[page]['urls']):
			cursor.execute("INSERT INTO query_results(eq_id, titles, contents, urls) VALUES (?,?,?,?)", (table2ID,t.decode("utf-8"),c.decode("utf-8"),u.decode("utf-8"),))
	for each in segCTList:
		cursor.execute("INSERT INTO ctContents(eq_id,ct_content) VALUES (?,?)", (table2ID,each,))
	connection.commit()
	connection.close()
	# insert eq_id 
	

def get_segCTContentFromStore(notExistedeEqid, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT ct_content from ctContents WHERE eq_id = ?", (notExistedeEqid,))
	CTContentList = [row[0] for row in results.fetchall()]
	return CTContentList

def checkIfAproriDataIsStore(availableEqid, db_name):
	Foundflag = False
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT rule_num FROM aprori_data WHERE eq_id = ?", (availableEqid,))
	response = results.fetchall()
	#print "response : "
	#print response 
	if len(response) == 0:
		#print ( "\n")
		#print ( str(availableEqid) + " is not in Aprori table, prepare to set up!")
		return Foundflag # return false if not found...  
	else: # return True if it is found 
		Foundflag = True
		return Foundflag
		
def checkIfCtcontentIFromStore(availableEqid, db_name):
	Foundflag = False
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT ct_content FROM ctContents WHERE eq_id = ?", (availableEqid,))
	response = results.fetchall()
	#print "response : "
	#print response 
	if len(response) == 0:
		#print ( "\n")
		#print ( str(availableEqid) + " is not in Aprori table, prepare to set up!")
		return Foundflag # return false if not found...  
	else: # return True if it is found 
		Foundflag = True
		return Foundflag
		
def get_avaiableExpandWordsIDfromStore(db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT id FROM expand_words ")
	IDList = [row[0] for row in results.fetchall()]
	return IDList
	
def get_aExpandWordsByQid(availableEqid, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	results = cursor.execute("SELECT expand_word from expand_words WHERE id = ?", (availableEqid,))
	expandWord = results.fetchone()[0]
	return expandWord
	


##init 
##known stuffs: aprori_data: eq_id, ruleNumber, dictionary, BOW, containFlag 
##aprori_ruleResults: a_id, min_support, min_confidence , rule_id, leftHand, rightHand, conf, 

def initAproriTable(qid, query, minsupport, min_confidence, covertedListForAllRules, containFlag, ruleNumber, dataset, wdic, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute("INSERT INTO aprori_data(eq_id, rule_num, contain_flag, dictionary, BOW) VALUES (?,?,?,?,?)", (qid, ruleNumber, containFlag, str(wdic).decode("utf-8"), str(dataset).decode("utf-8"),))
	connection.commit()
	results = cursor.execute("SELECT id from aprori_data WHERE eq_id = ?", (qid,))
	current_aid = results.fetchone()[0]
	for rule in covertedListForAllRules:
		#print "debug rule....."
		#print rule[0],
		#print " -> "
		#print rule[1],
		#print "\n"
		left = joinAllWord(rule[0])
		right = joinAllWord(rule[1])
		cursor.execute("INSERT INTO aprori_ruleResults(a_id,  min_support, min_confidence, leftHand, rightHand, conf) VALUES (?,?,?,?,?,?)", (current_aid, minsupport, min_confidence, left, right, rule[2], ))
		#for left,right in zip(rule[0],rule[1]): #lefthand and righthand data
			#print left + " --> " + right + ",conf:" + str(rule[2]).decode("utf-8") + '\n'
			#print "writing into SQL....."
		#	cursor.execute("INSERT INTO aprori_ruleResults(a_id,  min_support, min_confidence, leftHand, rightHand, conf) VALUES (?,?,?,?,?,?)", (current_aid, minsupport, min_confidence, left, right, rule[2], ))
	connection.commit()
	connection.close()
	
	

def joinAllWord(recursiveResults):
	q = ' '.join(e for e in recursiveResults)
	return q



def get_onePageResultsfromStore(query, itemsNumToPick, db_name):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	## get eqid 
	results = cursor.execute("SELECT id FROM expand_words WHERE expand_word = ?", (query,))
	#results = cursor.execute("SELECT id, expand_word FROM expand_words")
	#response = results.fetchall()
	#id = [row[0] for row in response]
	#expand_word = [row[1] for row in response]
	#print (<p>id</p>)
	#print ('<p>' + expand_word + '</p>')
	current_eqid = results.fetchone()[0]
	results = cursor.execute("SELECT titles, contents, urls FROM query_results WHERE eq_id = ? LIMIT ?", (current_eqid,itemsNumToPick))
	response = results.fetchall()
	# response = [[id,expand_word],[id,expand_word],[id,expand_word]...n]
	titles = [row[0] for row in response]
	contents = [row[1] for row in response]
	urls = [row[2] for row in response]
	"""
    response = {'Name':   name,
                'DOB':    dob,
                'data':   data,
                'top3':   data[0:3]}
	"""
	connection.close()
	return titles, contents, urls
	
	
	
	
############  MY CUSTOM QUERY #################### 

## controller passes the cgi "which_query" to model file: ModififedGoogleSearch.py 

###old noy used######
def get_list_FromAcombinations(e_file):
	eachFileList = [] 
	for line in open(e_file):
		out1 = re.sub('[%s]' % re.escape(string.punctuation), '', line)
		eachFileList.append(out1)
	return eachFileList


def get_allList_from_ehownet(files_list):
	all_list = []
	for each_file in files_list:
		g = get_list_FromAcombinations(each_file)
		all_list.append(g)
	expanedquerys = recursiveFindAllCombinations(all_list)
	#joinExpanedquerys = joinAllWordAsQuery(results)
	return(expanedquerys)

###new######


#def recursiveFindAllCombinations(listOfwords):
def recursiveFindAllCombinations(listA,listB):
	result = list(itertools.product(listA,listB))
	return result 
	
def joinAllWordAsQuery(recursiveResults):
	l1 = []
	for i in recursiveResults:
		q = ''.join(str(e) for e in i)
		l1.append(q)
	return l1


#def resolveFilenameOfeHownet(segWordList = None, unsegWord, fake = TRUE):
#""" should use seged work to locate the FILEs for expanding but for this ver, just """


def get_allExpannedQueryFromStore(userQuery):
	allDics = get_FakeListToStore()
	print allDics
	SQ = segment_Query(userQuery)
	SQ  = [line.strip() for line in SQ ]
	print "SQ"
	print SQ
	tempA = []
	tempB = []
	for index, dic in allDics.items():
	#	for ll in dic['A']:
	#		print "dic A"
	#		print dic['A']
	#		if SQ[0] == ll:
	#			tempA = dic['A']
	#	print tempA
		if SQ[0] in dic['A']:
			tempA = dic['A']
			print "tempA"
			print tempA
		if SQ[1] in dic['B']:
			tempB = dic['B']
			print "tempB"
			print tempB
	rResult = recursiveFindAllCombinations(tempA,tempB)
	print "RrESULT"
	print rResult
	
	#set_recursiveResultToSql(rResult)
	combinedQueryList = joinAllWordAsQuery(rResult)
	return combinedQueryList

def get_googleResult_from_allExpandedQuery(combinedQueryList):
#""" Input: query String (which_query) from google-search bar output: get the list of JSONs """
	allJSON = {}
	for q in combinedQueryList:
		queryResult = ModifiedGoogleSearch.pygoogle(q)
		allJSON[q] = queryResult.containerForAllData
		#print '*Found %s results*'%(firstQuery.get_result_count())
	#set_original_googleResultToSql(firstQuery)
	
	return allJSON

def get_athlete_from_id(athlete_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    results = cursor.execute("""SELECT name, dob FROM athletes WHERE id=?""",
                                     (athlete_id,))
    (name, dob) = results.fetchone()
    results = cursor.execute("""SELECT value FROM timing_data WHERE athlete_id=?""",
                                     (athlete_id,))
    data = [row[0] for row in results.fetchall()]
    response = {'Name':   name,
                'DOB':    dob,
                'data':   data,
                'top3':   data[0:3]}
    connection.close()
    return(response)

def get_namesID_from_store():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    results = cursor.execute("""SELECT name, id FROM athletes""")
    response = results.fetchall()
    connection.close()
    return(response)
	
	
############################


def get_names_from_store():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    results = cursor.execute("""SELECT name FROM athletes""")
    response = [row[0] for row in results.fetchall()]
    connection.close()
    return(response)

def get_athlete_from_id(athlete_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    results = cursor.execute("""SELECT name, dob FROM athletes WHERE id=?""",
                                     (athlete_id,))
    (name, dob) = results.fetchone()
    results = cursor.execute("""SELECT value FROM timing_data WHERE athlete_id=?""",
                                     (athlete_id,))
    data = [row[0] for row in results.fetchall()]
    response = {'Name':   name,
                'DOB':    dob,
                'data':   data,
                'top3':   data[0:3]}
    connection.close()
    return(response)

def get_namesID_from_store():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    results = cursor.execute("""SELECT name, id FROM athletes""")
    response = results.fetchall()
    connection.close()
    return(response)







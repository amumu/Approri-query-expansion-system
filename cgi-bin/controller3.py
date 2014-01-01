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

#! /usr/local/bin/python3
import cgitb
cgitb.enable()
import cgi 
import urllib
import yate
import markup
import pickle
import itertools
import time
import myquerypaser
import sql_webModel
import ehownet
import config_sectionmap
import logging 


	
def getDisplayResult(which_page,dicOfAllPagesOfAQuery):
	titles = myquerypaser.dicOfAllPagesOfAQuery[which_page]['titles']
	contents = dicOfAllPagesOfAQuery[which_page]['contents']
	url = dicOfAllPagesOfAQuery[which_page]['url']
	return titles, contents, url
	
def prepareSegDataForAprori(webQuerryResultPerQuery):
	ctListPerQuery = myquerypaser.jsonPaserForOneQuery(webQuerryResultPerQuery, mergeCTResult = True)
	segCTStingListPerQuery = segQuery.segmentCTListPerQuerys(ctListPerQuery)
	return segCTStingListPerQuery


	
########### global ############
FILE_SQLITE = config_sectionmap.ConfigSectionMap("client_one")['file_sqlite']
NEXT_URL = 'controller4.py'
#NEXT_URL1 = 'controller5.py'

########### logging init ############
logger = logging.getLogger('myapp')
logger.info('controller2.py started')

####### controller process #############
# CGI parameter passing 
form_data = cgi.FieldStorage()
expanedWordsList = form_data.getlist("expanded_terms_array")

print(yate.start_response())
print(yate.include_header("Aprori Results: "))
#print('<h2>' + "these are the expanded queries" +'</h2>')
#print(yate.u_list(expanedWordsList))
#print ('</br>')
	

#### get eqid for the expaned words 

eqidList = [] 
for each_word in expanedWordsList:
	eqidList.append(sql_webModel.getExistedIDFromStore(each_word.decode("utf-8"),FILE_SQLITE))

#print(yate.para(str(eqidList)))
#### get the candicate 
candidateDic = {}
for id in eqidList:
	candidateDic[id] = sql_webModel.get_theFlagFromAproriByEqid(id,FILE_SQLITE)

#print(yate.para(str(candidateDic))) 

candidateList = []
print(yate.start_form(NEXT_URL, form_type="POST"))

for id in candidateDic.keys():
	if candidateDic[id] == 1:
		candidateList.append(sql_webModel.get_expannedQueryByQID(id,FILE_SQLITE))
		print(yate.hidden_input('candidateID', str(id)))
		#print(yate.para(str(candidateList)))  

#print(yate.end_form())

candidateList = [s.encode("utf-8") for s in candidateList]

print('<h2>' + "After calculation, these are the most possible query candidates! " +'</h2>')
print(yate.u_list(candidateList))
print ('</br>')
#print(yate.createLink({"Verbose mode": "/cgi-bin/controller4.py"}))
print ('</br>')

#print(yate.start_form(NEXT_URL, form_type="POST"))

#### CGI passing for DEBUG page  
for c in candidateList:
	print(yate.hidden_input('candidate', c))
print('<h3>' + "Check verbose info: " +'</h3>')
print(yate.end_form("enter to verbose mode"))

#### CGI passing for final results page 

#print(yate.start_form(NEXT_URL1, form_type="POST"))
#for c in candidateList:
#	print(yate.hidden_input('results', c))
#print('<h3>' + "View the final results: " +'</h3>')
#print(yate.end_form("Go to result page", submitname = "submit1"))


print(yate.include_footer({"Done, go back to Google": "/index.html"}))

### render segmented results #### 
#segmentedQuery = segQuery.segmentToListPerQuery(term)
#print(yate.para("These are segmented query: "))
#print ("<h1>" +  str(segQuery) + "<h1>")
#print(yate.u_list(segQuery))

#### get expanded word from SQL 
#if sql_webModel.checkIfdataIsStore(term.decode("utf-8"),FILE_SQLITE): ## found it in DB
#	expandedQueriesPerDemoList = ehownet.get_allExpannedQueryFromStore(term.decode("utf-8"))
	### render eexpanded word results #### 
#	print(yate.para("These are expanded queries: "))
#	print(yate.u_list(expandedQueriesPerDemoList))
#	print(yate.include_menu1({"cancel, go back to Google": "/index.html"}, str(term) ))

	
	
	
	
	
	
	



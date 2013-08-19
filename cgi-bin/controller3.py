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
import sql_webModel
import ehownet


	
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
the_url = 'controller4.py'
#the_url1 = 'controller5.py'
# CGI parameter passing 
form_data = cgi.FieldStorage()
expanedWordsList = form_data.getlist("expanded_terms_array")

####### controller process #############
print(yate.start_response())
print(yate.include_header("Aprori Results: "))
#print('<h2>' + "these are the expanded queries" +'</h2>')
#print(yate.u_list(expanedWordsList))
#print ('</br>')
	

#### get eqid for the expaned words 

eqidList = [] 
for each_word in expanedWordsList:
	eqidList.append(sql_webModel.getExistedIDFromStore(each_word.decode("utf-8"),myDB))

#print(yate.para(str(eqidList)))
#### get the candicate 
candidateDic = {}
for id in eqidList:
	candidateDic[id] = sql_webModel.get_theFlagFromAproriByEqid(id,myDB)

#print(yate.para(str(candidateDic))) 

candidateList = []
print(yate.start_form(the_url, form_type="POST"))

for id in candidateDic.keys():
	if candidateDic[id] == 1:
		candidateList.append(sql_webModel.get_expannedQueryByQID(id,myDB))
		print(yate.hidden_input('candidateID', str(id)))
		#print(yate.para(str(candidateList)))  

#print(yate.end_form())

candidateList = [s.encode("utf-8") for s in candidateList]

print('<h2>' + "After calculation, these are the most possible query candidates! " +'</h2>')
print(yate.u_list(candidateList))
print ('</br>')
#print(yate.createLink({"Verbose mode": "/cgi-bin/controller4.py"}))
print ('</br>')

#print(yate.start_form(the_url, form_type="POST"))

#### CGI passing for DEBUG page  
for c in candidateList:
	print(yate.hidden_input('candidate', c))
print('<h3>' + "Check verbose info: " +'</h3>')
print(yate.end_form("enter to verbose mode"))

#### CGI passing for final results page 

#print(yate.start_form(the_url1, form_type="POST"))
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
#if sql_webModel.checkIfdataIsStore(term.decode("utf-8"),myDB): ## found it in DB
#	expandedQueriesPerDemoList = ehownet.get_allExpannedQueryFromStore(term.decode("utf-8"))
	### render eexpanded word results #### 
#	print(yate.para("These are expanded queries: "))
#	print(yate.u_list(expandedQueriesPerDemoList))
#	print(yate.include_menu1({"cancel, go back to Google": "/index.html"}, str(term) ))

	
	
	
	
	
	
	



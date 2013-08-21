# Aprori-based query expansion: controller2.py
#
# 
# Author: Paul Yang <paulyang0125@gmail.com>
# URL: 
# For license information, see LICENSE.TXT
#encoding=utf-8
import cgitb
cgitb.enable()
import submodule_load
import cgi 
import urllib
import yate
import myquerypaser
import chineseseg
import sql_webModel
import ehownet
import logging

##### global parameters #######

FILE_SQLITE = 'final.sqlite'
NEXT_URL = 'controller3.py'

########### logging init ############
logger = logging.getLogger('myapp')
logger.info('controller2.py started')

## CGI parameter passing 
form_data = cgi.FieldStorage()
term_ascii = form_data['terms'].value
print(yate.start_response())
print(yate.include_header("Aprori Page for " + str(term_ascii)))


####### controller process #############


#### get expanded word from SQL, render them and pass through input method to controller 3  #####

if sql_webModel.checkIfdataIsStore(term_ascii.decode("utf-8"),FILE_SQLITE): 
	## this should get from SQL, NOT ehownet....
	logger.info('get the expanded query from SQLite')
	#expandedQueriesPerDemoList = ehownet.get_allExpannedQueryFromStore(term_ascii_ascii.decode('utf-8'))
	expandedQueriesPerDemoList =  sql_webModel.get_expannedQueryFromStore(term_ascii.decode('utf-8'),FILE_SQLITE)
	
	#print ("<h1>" +  str(expandedQueriesPerDemoList) + "<h1>")
	d = [s.encode("utf-8") for s in expandedQueriesPerDemoList] 
	### render eexpanded word results #### 
	print('<h2>' + "these are the expanded queries from eHownet" +'</h2>')
	print ('</br>')
	print(yate.u_list(d))
	print(yate.start_form(NEXT_URL, form_type="POST"))
	for each_word in expandedQueriesPerDemoList:
		print(yate.hidden_input('expanded_terms_array', each_word.encode("utf-8")))
	print(yate.end_form())
	print ('</br>')
	print(yate.include_footer({"Cancel, go back to Google": "/index.html"}))
	#print(yate.include_menu1({"cancel, go back to Google": "/index.html"}, str(term_ascii) ))

else: ## not processed before, do expannedQuery on the air 
	logger.info('get the expanded query from eHownet DB')
	##TODO: do expannedQuery on the air
	#segQuery = chineseseg.segmentToListPerQuery(term_ascii)
	#s = [s.encode("utf-8") for s in segQuery] 
	### render segmented results #### 
	#segmentedQuery = segQuery.segmentToListPerQuery(term_ascii)
	#print(yate.para("These are segmented query: "))
	#print ("<h1>" +  str(segQuery) + "<h1>")
	#s = ' '.join(segQuery.encode("utf-8")
	#print(yate.u_list(s))
	pass 
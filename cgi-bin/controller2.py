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

#encoding=utf-8
import cgitb
cgitb.enable()
import cgi 
import urllib
import yate
import myquerypaser
import chineseseg
import sql_webModel
import ehownet
import logging
import config_sectionmap

##### global parameters #######

FILE_SQLITE = config_sectionmap.ConfigSectionMap("client_one")['file_sqlite']
NEXT_URL = 'controller3.py'

########### logging init ############
logger = logging.getLogger('myapp')
logger.info('controller2.py started')

####### controller process #############

## CGI parameter passing 
form_data = cgi.FieldStorage()
term_ascii = form_data['terms'].value
print(yate.start_response())
print(yate.include_header("Aprori Page for " + str(term_ascii)))


#### get expanded word from SQL or on the air if data in not in sql, render them and pass through input method to controller 3  

if sql_webModel.checkIfdataIsStore(term_ascii.decode("utf-8"),FILE_SQLITE): 
	logger.info('get the expanded query from SQLite')
	lexpandedQueries_SQL =  sql_webModel.get_expannedQueryFromStore(term_ascii.decode('utf-8'),FILE_SQLITE)
	
	#print ("<h1>" +  str(lexpandedQueries_SQL) + "<h1>")
	lexpandedQueries_SQL_ascii = [s.encode("utf-8") for s in lexpandedQueries_SQL] 
	### render expanded word results #### 
	print('<h2>' + "these are the expanded queries from eHownet" +'</h2>')
	print ('</br>')
	print(yate.u_list(lexpandedQueries_SQL_ascii))
	print(yate.start_form(NEXT_URL, form_type="POST"))
	for each_query in lexpandedQueries_SQL:
		print(yate.hidden_input('expanded_terms_array', each_query.encode("utf-8")))
	print(yate.end_form())
	print ('</br>')
	print(yate.include_footer({"Cancel, go back to Google": "/index.html"}))
	#print(yate.include_menu1({"cancel, go back to Google": "/index.html"}, str(term_ascii) ))

else: ## not processed before, do expannedQuery on the air 
	logger.info('get the expanded query from eHownet DB')
	print('<h1>' + 'get the expanded query from eHownet DB' +'</h1>')
	print('<h2>' + 'sorry, your term is not supported in ehowent cache!' +'</h2>')
	logger.info('get the expanded query from eHownet DB')
	'''
	#lexpandedQueries_ehownet = ehownet.get_allExpannedQueryFromStore(term_ascii_ascii.decode('utf-8'))
	##TODO: do expannedQuery on the air
	#segQuery = chineseseg.segmentToListPerQuery(term_ascii)
	#s = [s.encode("utf-8") for s in segQuery] 
	### render segmented results #### 
	#segmentedQuery = segQuery.segmentToListPerQuery(term_ascii)
	#print(yate.para("These are segmented query: "))
	#print ("<h1>" +  str(segQuery) + "<h1>")
	#s = ' '.join(segQuery.encode("utf-8")
	#print(yate.u_list(s))
	'''
	pass 

# Aprori-based query expansion: controller1.py
#
# 
# Author: Paul Yang <paulyang0125@gmail.com>
# URL: 
# For license information, see LICENSE.TXT
#encoding=utf-8

import cgitb
cgitb.enable()
import cgi 
import urllib
import sql_webModel
import yate
import myquerypaser
import logging
import config_sectionmap

########### global ############  ##TODO: use ConfigParser to move them to *.ini

LOG_PATH = config_sectionmap.ConfigSectionMap("client_one")['log_path']
FILE_SQLITE = config_sectionmap.ConfigSectionMap("client_one")['file_sqlite']
DATAINSTORE = bool(config_sectionmap.ConfigSectionMap("client_one")['datainstore'])




########### logging init ############
print "initializing the logging" 

LOG_LEVEL = logging.DEBUG
LOG_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(LOG_PATH)
hdlr.setFormatter(LOG_FORMATTER)
logger.addHandler(hdlr) 
logger.setLevel(LOG_LEVEL)
logger.info('controller1.py started')



####### CGI controller process #############

## get CGI result
form_data = cgi.FieldStorage()
term_ascii = form_data['terms'].value
query = term_ascii.decode("utf-8")
logger.info('Got the user query %s from fields from index.html' % query)

## Determine if Google pages by the query has been cached in SQLite 
if sql_webModel.checkIfdataIsStore(query,FILE_SQLITE):
	logger.info("Found it, use it from the cache to save crawler's time")
	lTitles_SQL, lContents_SQL, lUrls_SQL = sql_webModel.get_onePageResultsfromStore(query, 8, FILE_SQLITE) ## 8 eight Google web-snippet 
else:
	logger.info("Not found, query through Google Search API directly!")
	## "results" are the JSONs list containing each page result FOR ONE QUERY [[ONE PAGE - title,content,url],[ONE PAGE - JSON]]
	lQueried_results_json = sql_webModel.get_googleResult_forClient(term_ascii)

	#for each in results:
	#	fordiaply = each_jsonPaser(each)

	for each_json in lQueried_results_json:
		lTitles,lContents,lUrls  = myquerypaser.onePageJsonPaser(each_json)
	DATAINSTORE = False


###### start to render in html-based ###############

print(yate.start_response())
print(yate.include_header("Google search result for " + str(term_ascii)))
print(yate.include_menu({"Are you satisfied? , go back to Google": "/index.html"}, str(term_ascii) ))
#print(yate.start_form("controller2.py"))
#print(yate.input_text('terms',str(term)))
#print(yate.end_form("enter to my app"))
#print(yate.para("Query for:" + str(term)))
#print("<br /><br />")

if DATAINSTORE:
	for title, content, url in zip(lTitles_SQL,lContents_SQL,lUrls_SQL):
		print(yate.render_search_result(title.encode('utf-8-sig'),content.encode('utf-8-sig'),url.encode('utf-8-sig')))
else:
	for title, content, url in zip(lTitles,lContents,lUrls):
		print(yate.render_search_result(title,content,url))






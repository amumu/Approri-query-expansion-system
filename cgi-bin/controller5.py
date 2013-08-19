


####### controller process #############

## get CGI result
print "get CGI result ..... "
form_data = cgi.FieldStorage()
term = form_data['terms'].value
query = term.decode("utf-8")
print "determine if CTU is stored"
if sql_webModel.checkIfdataIsStore(query,myDB): ## found it in DB
	onePageTitlesFromSQL,onePageContentsFromSQL,onePageUrlsFromSQL = sql_webModel.get_onePageResultsfromStore(query, 8,myDB)
else:
	print "not found from store, query Google directly"
	# "results" are the JSONs list containing each page result FOR ONE QUERY [[ONE PAGE - title,content,url],[ONE PAGE - JSON]]
	results = sql_webModel.get_googleResult_forClient(term)

	#for each in results:
	#	fordiaply = each_jsonPaser(each)

	for each in results:
		onePageTitles,onePageContents,onePageUrls  = jsonPaserForOnePage(each)
	dataInStore = False


###### strat to render in html-based ###############

print(yate.start_response())
print(yate.include_header("Google search result for " + str(term)))
print(yate.include_menu({"Are you satisfied? , go back Google": "/index.html"}, str(term) ))
#print(yate.start_form("controller2.py"))
#print(yate.input_text('terms',str(term)))
#print(yate.end_form("enter to my app"))
#print(yate.para("Query for:" + str(term)))

#print("<br /><br />")

if dataInStore:
	for title, content, url in zip(onePageTitlesFromSQL,onePageContentsFromSQL,onePageUrlsFromSQL):
		print(yate.render_search_result(title.encode('utf-8-sig'),content.encode('utf-8-sig'),url.encode('utf-8-sig')))
else:
	for title, content, url in zip(onePageTitles,onePageContents,onePageUrls):
		print(yate.render_search_result(title,content,url))




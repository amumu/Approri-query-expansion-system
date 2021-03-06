﻿##################################################################################
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



﻿#! /usr/local/bin/python3
import cgitb
cgitb.enable()
import sys
import cgi 
import urllib
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
import markup
import itertools
import time



###### 2 Pasers ########
# input: webquerry result 
# ultimate: {query1:{page(0 - n):{'titles':[t1, t2, t3....etc], 'contents':[c1, c2, c3....etc], 'urls': [u1, u2, u3]}},
#                                query1:{page(0 - n):{'titles':[t1, t2, t3....etc], 'contents':[c1, c2, c3....etc], 'urls': [u1, u2, u3]}} }
# output 1: query -  {page(0 - n):{'titles':[t1, t2, t3....etc], 'contents':[c1, c2, c3....etc], 'urls': [u1, u2, u3]}}
# output 2: merge a query of pages of title and content into one list [c1,t1,c2,t2,.....etc] for seg and Aproori
# optional: {query:[c1,c2,c3,t1,t2,t3.......etc]} -> {query"[sC1, sC2.......]}
# 
def jsonPaserForOneQuery(webQuerryResultPerQuery, mergeCTResult = False):
	dicOfAllPagesOfAQuery ={} #{page(0 - n):{'titles':[t1, t2, t3....etc], 'contents':[c1, c2, c3....etc], 'urls': [u1, u2, u3]}}
	mergedCTlistPerQuery = []
	pageCount = 0 
	for each_page in webQuerryResultPerQuery:
		titlesPerPage = []
		contentsPerPage = []
		urlsPerPage = []
		if each_page['responseStatus'] == 200:
			for result in each_page['responseData']['results']:
				temp_title = urllib.unquote(result['titleNoFormatting']).encode('utf-8')
				titlesPerPage.append(temp_title)
				temp_content = result['content'].encode('utf-8').strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
				contentsPerPage.append(temp_content)
				temp_url = urllib.unquote(result['unescapedUrl']).encode('utf-8')
				urlsPerPage.append(temp_url)
		dicOfAllPagesOfAQuery[pageCount] = {'titles':titlesPerPage,'contents':contentsPerPage,'urls':urlsPerPage}
		pageCount += 1
	if mergeCTResult == True:
		#merge c and t
		for v in dicOfAllPagesOfAQuery.values():
			mergedCTlistPerPage = list(set(v['titles'] + v['contents']))
			mergedCTlistPerQuery.extend(mergedCTlistPerPage)
		return mergedCTlistPerQuery
	else:
		return dicOfAllPagesOfAQuery
		

def jsonPaserForOnePage(each_json):
	titles = []
	contents = []
	urls = []
	####### each JSON means each page result in a JSON 
	if each_json['responseStatus'] == 200:
		for result in each_json['responseData']['results']:
			temp_title = urllib.unquote(result['titleNoFormatting']).encode('utf-8')
			titles.append(temp_title)
			temp_content = result['content'].encode('utf-8').strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
			contents.append(temp_content)
			temp_url = urllib.unquote(result['unescapedUrl']).encode('utf-8')
			urls.append(temp_url)
		return titles, contents, urls

		
####################SINGLE QUERY ##########################################
def onePageJsonPaser(each_json):
	titles = []
	contents = []
	urls = []
	####### each JSON means each page result in a JSON 
	for result in each_json['responseData']['results']:
		temp_title = urllib.unquote(result['titleNoFormatting']).encode('utf-8')
		titles.append(temp_title)
		temp_content = result['content'].encode('utf-8').strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
		contents.append(temp_content)
		temp_url = urllib.unquote(result['unescapedUrl']).encode('utf-8')
		urls.append(temp_url)
	return titles, contents, urls
	
def each_jsonPaser(each_json):
	all_result = []
	for result in each_json['responseData']['results']:
		each_result = []
		temp_title = urllib.unquote(result['titleNoFormatting']).encode('utf-8')
		each_result.append(temp_title)
		temp_content = result['content'].encode('utf-8').strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
		each_result.append(temp_content)
		temp_url = urllib.unquote(result['unescapedUrl']).encode('utf-8')
		each_result.append(temp_url)
		all_result.append(each_result)
	return all_result
	
def each_jsonPaserUsingDic(each_json):
	all_result = {}
	for result in each_json['responseData']['results']:
		temp_title = urllib.unquote(result['titleNoFormatting']).encode('utf-8')
		all_result['title'] = temp_title
		each_result.append(temp_title)
		temp_content = result['content'].encode('utf-8').strip("<b>...</b>").replace("<b>",'').replace("</b>",'').replace("&#39;","'").strip()
		each_result.append(temp_content)
		temp_url = urllib.unquote(result['unescapedUrl']).encode('utf-8')
		each_result.append(temp_url)
		all_result.append(each_result)
	return all_result
	


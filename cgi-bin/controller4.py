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
#import segQuery
import pickle
import itertools
import time
import myquerypaser
#import chineseseg
import sql_webModel
import ehownet

##### global paratermters #######

myDB = 'final.sqlite'

# CGI parameter passing 
form_data = cgi.FieldStorage()
candidateIDList = form_data.getlist("candidateID")
candidateList = form_data.getlist("candidate")

####### controller process #############
print(yate.start_response())
print(yate.include_header("Verbose info of cal "))
# create {"C1":{'BOW':?,'Dic':?,'Rules':?,'tag':?,'segCT':?},C2:{}} 

mixInfoDic = {}
#### get eqid from candidateList 
for eqid, name in zip(candidateIDList, candidateList): 
	infoDic = sql_webModel.get_verboseInfoForCandidateByEqid(eqid,myDB)
	mixInfoDic[name] = infoDic

#print ('<h3>' + "debug ........." +'</h3>')
#print ('<p>' + str(mixInfoDic) +'</p>')

print('<h2>' + "these are BOW" +'</h2>')
for name in candidateList:
	print('<h3>' + name +'</h3>')
	print ('<p>' + str(mixInfoDic[name]['BOW']) +'</p>')
print ('</br>')

print('<h2>' + "these are Dic" +'</h2>')
for name in candidateList:
	print('<h3>' + name +'</h3>')
	print ('<p>' + str(mixInfoDic[name]['dictionary']) +'</p>')
print ('</br>')

print('<h2>' + "these are Rules produced by Aprori" +'</h2>')
for name in candidateList:
	print('<h3>' + name +'</h3>')
	print ('<p>' + "Rule number: " +str(mixInfoDic[name]['rule_num']) +'</p>')
	print ('</br>')
	print ('<p>' + "min_support: " + str(mixInfoDic[name]['min_support']) + " min_confidence: " + str(mixInfoDic[name]['min_confidence']) +'</p>')
	print ('</br>')
	for left, right, c in zip(mixInfoDic[name]['leftHand'],mixInfoDic[name]['rightHand'],mixInfoDic[name]['conf'] ):
		print ('<p>' + left.encode("utf-8") + ' --> '+ right.encode("utf-8") + ' ' + str(c)  +   '</p>')

print ('</br>')


print(yate.include_footer({"Done, go back to Google": "/index.html"}))


"""
mixData = {'min_support':   min_support,
                'min_confidence':    min_confidence,
                'leftHand':   leftHand,
                'rightHand':   rightHand,
				'BOW':   BOW,
				'dictionary':   dictionary,
				'rule_num':   rule_num}
"""
	
	
	
	
	
	
	



# Aprori-based query expansion: config_sectionmap.py
#
# 
# Author: Paul Yang <paulyang0125@gmail.com>
# URL: 
# For license information, see LICENSE.TXT
#encoding=utf-8

import ConfigParser

## global 
SETTINGS = "config\server.ini"

## section is like 'SectionOne', 'SectionTwo', 'SectionThree', 'Others'
def ConfigSectionMap(section):
	dict1 = {}
	Config = ConfigParser.ConfigParser()
	Config.read(SETTINGS)
	
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1
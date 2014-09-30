# -*- coding: utf-8 -*-
"""
data
	siteabb
		html (downloaded)
			archives
			updates
			models
		htmlc (parsed)
			archives
			models
			updates
		db (DB)
			pickle (archives / updates / models)
			sqlite
			mysql
		export (computed)
			csv (archives / updates / models)
			json 
libraries
	covers (downloaded)
		siteabb
			updates
				alt
				wide
			models
	img (web downloaded)(link)
		siteabb
			updates
	vid (web downloaded)(link)
		siteabb
			updates
"""

OFFLINEPATH = 'd:/.lkjhdata/data'
DATAPATH = 'd:/.lkjhdata/data'
DBPATH = 'd:/.lkjhdata/data'
LIBRARIESPATH = 'd:/.lkjhdata/lib'

import os
import time

def setfiledate(file, day):
	if day:
		t = time.mktime(time.strptime(day, '%Y-%m-%d'))
		os.utime(file, (t,t))

def getfiledate(file):
	statf = os.stat(file)
	return time.ctime(statf.st_mtime)

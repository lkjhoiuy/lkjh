# -*- coding: utf-8 -*-
"""
Test.
"""
import lkjh.logger
import lkjh.sites.ma as ma_
import lkjh.sites.fj as fj_
from lkjh.cover import *
from lkjh.model import *
import internet

from pprint import pprint

class Test:
	def __init__(self, site):
		self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
		self.site = site
		
	def get_07(self):
		for year in [2014]:
			self.site.delcsv(year)
			
			for month in [7]:
				self.site.update(year, month)
				#~ self.site.writecsv()
		
		self.site.save('json')
		self.site.save('pickle')
		#~ self.site.concatcsv(2014, 2004)

	def get_all(self, endyear, beginyear=None):
		beginyear = beginyear or endyear
		
		for year in range(endyear, beginyear-1, -1):
			self.site.delcsv(year)
			
			for month in range(12, 0, -1):
				self.site.update(year, month)
		
		self.site.save()
		self.site.concatcsv(2014, 2004)
		
	def json_write(self):
		self.site.json_export()
		
	def json_write_model(self, modelid):
		JsonFile(modelid).write(self.site.export_modelupdates(modelid), 2)

	def json_read(self):
		self.site.json_import()

	def db_stats(self):
		print(self.site.models.count, 'models')
		print(self.site.updates.count, 'updates')
		print(self.site.covers.count, 'covers')
	
	def printCoverUrl(self):
		for cover in self.site.covers.values():
			#~ print(cover)
			print(cover[0].url)

def maTest():
	xs = Test(ma_.xSite('json'))
	xs.db_stats()
	#~ xs.get_07()
	xs.get_all(2014)
	#~ xs.get_all(2014, 2005)
	
	#~ xs.json_read()
	xs.site.save()
	#~ xs.json_write()
	
	#~ xs.json_write_model('sofi-a')
	
def fjTest():
	xs = Test(fj_.xSite('json'))
	xs.db_stats()
	#~ xs.get_07()
	xs.get_all(2014)
	xs.site.save()
	#~ xs.json_write()
	#~ xs.printCoverUrl()

	
if __name__ == "__main__":
	
	print("IP", internet.myip())
	lkjh.logger.init("test.log")  #, logging.DEBUG)
	#~ Cover.offline = True
	#~ Model.offline = True

	maTest()
	fjTest()
	
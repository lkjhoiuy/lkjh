# -*- coding: utf-8 -*-
"""
Data element.
Class for all data elements cats: archive, update, model, author.
"""
import logging
from bs4 import BeautifulSoup
from collections import OrderedDict
from lkjh.remotepage import *

class Data:
	"""
	"""
	fields = ['id']  # for import/export purpose
	
	def __init__(self, cat, id=''):
		self.logger = logging.getLogger('lkjh.' + self.__class__.__name__ + '['+cat+']')
		self.cat = cat
		self.id = id

	def read(self):
		if self.offline: return None
		self.remotepage = RemotePage(self.cat, self.localpath, self.url)
		return self.remotepage.read()
		
	def get_html_date(self):
		return self.remotepage.get_html_date(self.date)

	def set_html_date(self):
		self.remotepage.set_html_date(self.date)

	def parse(self, html):
		return BeautifulSoup(html)

	def write_htmlc(self, htmlc):
		self.remotepage.write_htmlc(htmlc)

	def update(self):
		self.parse(self.read())
		
	def save(self):
		self.site.colls[self.cat].set(self)
		
	# self.__dict__ -> no property
	# getattr(self) -> with property
	def export(self):
		# return OrderedDict( [(k.lstrip('_'), self.__dict__[k]) for k in self.fields] )
		return OrderedDict( [(k, getattr(self,k)) for k in self.fields] )

	def dbexport(self):
		return OrderedDict( [(k, getattr(self,k)) for k in self.dbfields] )

	def importFrom(self, data):
		#~ for k in  self.__dict__:  # TODO open
		for k in  self.dbfields:
			try:
				setattr(self, k, data[k])
			except KeyError:
				if k == 'open':
					setattr(self, k, False)  # no open field => closed
			except AttributeError:
				pass  # Model urlpath
		return self

"""
def to_json(self, indent=2):
	# json.dumps({k.lstrip('_'): v for k, v in self.__dict__.items()})
	return json.dumps(OrderedDict([ (k.lstrip('_'), self.__dict__[k]) for k in self.fields]),
		default=lambda o: {k:v for k,v in o.__dict__.items()},
		sort_keys=False, indent=indent)
"""
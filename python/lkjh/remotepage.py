# -*- coding: utf-8 -*-
"""
Remote page.
"""
import logging
import os
from lkjh.cst import *
from lkjh.remotefile import *

class RemotePage(RemoteFile):
	"""
	"""
	site = None
	path = DATAPATH
	
	def __init__(self, type, localpath, url=None):
		self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
		self.type = type  # 'archive', 'update', 'model'
		self.localpath = localpath
		super().__init__(self.htmlfile, url)
		
	@property
	def htmlfile(self):
		return '{0}/{1}/html/{2}s/{3}.html'.format(self.path, self.site.abb, self.type, self.localpath.strip('/').replace('/', '_'))
		
	@property
	def htmlcfile(self):
		return '{0}/{1}/htmlc/{2}s/{3}.html'.format(self.path, self.site.abb, self.type, self.localpath.strip('/').replace('/', '_'))
		
	def read(self):
		return super().read()

	def write_htmlc(self, htmlc):
		if os.path.exists(self.htmlcfile):
			return
		if htmlc:
			with open(self.htmlcfile, 'w') as f:
				f.writelines(htmlc)

	def get_html_date(self):
		return getfiledate(self.htmlfile)
	
	def set_html_date(self, date):
		setfiledate(self.htmlfile, date)
	

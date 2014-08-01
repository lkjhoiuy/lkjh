# -*- coding: utf-8 -*-
"""
Cover.
"""
import os
from lkjh.cst import *
from lkjh.data import *
from lkjh.remotefile import *

LOCALPATH = 'd:/.lkjhdata/libraries'

class Cover(Data):
	"""
	"""
	site = None
	path = LOCALPATH
	rad = ''
	offline = False
	dbfields = [
		'id',  # md5
		'ctype',
		'refid',  # update or model
		'size',
		'open'
	]
	fields = dbfields
	
	def __init__(self, refid='', ctype='cover'):
		super().__init__('cover')
		# self.id = id  # md5
		self.refid = refid  # ref = update, model
		self.ctype = ctype  # cover, alt, wide, headshot, ...
		self.size = 0
		# TODO setter for str -> int
		self.crc32 = 0
		self.urls = {}  # by ctype
		self._urls = {}  # by ctype
		self.open = True
	
	@property
	def localfile(self):
		return '{0}/covers/{1}/{2}/{3}.jpg'.format(self.path, self.site.abb, self.ctype, self.refid)
	
	def localfile_exists(self):
		return os.path.exists(self.localfile)
		
	def read(self):
		self.logger.debug(self.urls[self.ctype])
		self.logger.debug(self.localfile)
		r = RemoteFile(self.localfile, self.urls[self.ctype]).read()
		if len(r) < 100:  # fj HTTP Error 404: Not Found = 88
			if self._urls:
				os.remove(self.localfile)
				try:
					return RemoteFile(self.localfile, self._urls[self.ctype](self)).read()
				except:
					return None
		else:
			return r

	def update(self, date=None):
		if self.open and not self.offline:
		#~ if not self.offline:
			self.logger.debug(self.refid)
			if self.read():
				if date:
					self.set_all(date)
				self.open = False
		
	def set_date(self, date=None):
		if not self.localfile_exists():
			return
		if date == None:  # date of update (same id)
			if self.site.updates.has_key(self.refid):
				date = self.site.updates[self.refid].date
			else:
				return
		setfiledate(self.localfile, date)
	
	def set_size(self):
		self.size = RemoteFile(self.localfile).size
	
	def set_crc(self):
		self.crc32 = RemoteFile(self.localfile).xcrc32
	
	def set_md5(self):
		self.id = RemoteFile(self.localfile).md5

	def set_all(self, date=None):
		#~ self.logger.info(date)
		self.set_date(date)
		self.set_size()
		# self.set_crc()
		self.set_md5()
		self.logger.debug(self.id)

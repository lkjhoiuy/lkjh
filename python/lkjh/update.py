# -*- coding: utf-8 -*-
"""
Update.
"""
from lkjh.cst import *
from lkjh.data import *

PRESENTING_PREFIX = '!'

class Update(Data):
	"""
	"""
	site = None
	rad = ''
	offline = False
	dbfields = [
		'id',
		'name',
		'urlpath',
		'date',
		'type',
		'models',
		'author',
		'count',
		'size',
		'dur',
		'covers',
		'open'
	]
	fields = dbfields + [
		'strmodels',
		'fingerprint'
	]

	def __init__(self, id=''):
		super().__init__('update', id)
		# self.id = id
		self.name = ''
		self.urlpath = ''
		self.date = ''  # yyyy-mm-dd
		self.type = 'img'  # 'img' / 'vid'
		self.count = ''  # img
		self.size = ''  # img / vid
		self.dur = ''  # vid
		self.models = []  # id
		self.author = ''  # id
		self.covers = {}  # ctype, id
		self.open = True
		
	@property
	def url(self):
		return '{0}/{1}'.format(self.rad, self.urlpath.lstrip('/'))
		
	@property
	def localpath(self):
		return self.urlpath
		
	@property
	def name(self):
		return self._name
		
	@name.setter
	def name(self, value):
		if value.startswith('Presenting'):
			value = PRESENTING_PREFIX + 'Presenting'
		value = value.replace('"', "'")
		self._name = value
	
	@name.deleter
	def name(self):
		del self._name
		
	@property
	def modelnames(self):
		return sorted([self.site.models.get(id).name for id in self.models])
		
	@property
	def modelids(self):
		return self.models
		
	@property
	def strmodels(self):
		return ', '.join(self.modelnames)
		
	@property
	def title(self):
		return "{0} - {1}".format(self.strmodels, self.name)
		
	@property
	def filename(self):
		return self.title.replace('?', '').replace(':', '!')
		
	def addmodel(self, id):
		if not id in self.models:
			self.models.append(id)
		
	def addcover(self, cover):
		self.covers[cover.ctype] = cover.id
		
	def getcover(self, ctype):
		try:
			return self.site.covers.get(self.covers[ctype])
		except KeyError:
			return None
		
	def update(self):
		super().parse()
		self.set_html_date()

	@property
	def fingerprint(self):
		l = list(self.title.lower())
		l.sort()
		return ''.join(l).lstrip(' _-,.:?!&%"()/\'')

	def get_fingerprint(self, s):
		l = list(s.lower())
		l.sort()
		return ''.join(l).lstrip(' _-,.:?!&%"()/\'')

	def __str__(self):
		return 'name={0}, type={1}, date={2}, id={3}, {4}'.format(self.name, self.type, self.date, self.id, self.title)
	
	def __repr__(self):
		return 'name={0}, type={1}, date={2}, id={3}, {4}'.format(self.name, self.type, self.date, self.id, self.title)

	def fmt4csv(self):
		s = '\t'.join([self.date, self.type, str(self.count), self.name, self.id, self.fingerprint, self.urlpath, self.title] + self.modelids)
		return s

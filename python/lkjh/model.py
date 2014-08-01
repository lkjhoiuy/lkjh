# -*- coding: utf-8 -*-
"""
Model.
"""
from lkjh.cst import *
from lkjh.data import *

from pprint import pprint

class Model(Data):
	"""
	"""
	site = None
	rad = ''
	offline = False
	dbfields = [
		'id',
		'name',
		'urlpath',
		'country',
		'ethnicity',
		'haircolor',
		'eyecolor',
		'breasts',
		'shaved',
		'height',
		'weight',
		'measurements',
		'icgid',
		'covers',
		'open'
	]
	fields = dbfields
	
	def __init__(self, id=''):
		super().__init__('model', id)
		# self.id = id
		self.name = ''
		self.urlpath = ''
		self.eyecolor = ''
		self.haircolor = ''
		self.height = ''
		self.weight = ''
		self.breasts = ''
		self.shaved = ''
		self.measurements = ''
		self.country = ''
		self.ethnicity = ''
		self.icgid = ''  # ICGID: AG-91O8 => http://www.thenude.eu/index.php?page=search&action=searchModels&m_name=AG-91O8#ModelsSearch => http://www.thenude.eu/Alisa%20G_16168.htm
		self.covers = {}
		self.open = True
	
	@property
	def url(self):
		return '{0}/{1}'.format(self.rad, self.urlpath.lstrip('/'))
		
	@property
	def localpath(self):
		return self.urlpath
		
	@property
	def title(self):
		# 'titi toto' -> 'Titi Toto'
		r = ' '.join(w.capitalize() for w in self.name.split(' '))
		return r

	def id2name(self):
		# 'titi-toto -> Titi Toto'
		r = ' '.join(w.capitalize() for w in self.id.split('-'))
		return r

	def addcover(self, cover):
		self.covers[cover.ctype] = cover.id
		
	def getcover(self, ctype):
		try:
			return self.site.covers.get(self.covers[ctype])
		except KeyError:
			return None

	def save(self):
		super().save()
		#~ self.logger.info(self.id)

	def __str__(self):
		return 'name={0}, id={1}, url={2}'.format(self.name, self.id, self.urlpath)
		
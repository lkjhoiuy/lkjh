# -*- coding: utf-8 -*-
"""
Author.
"""
from lkjh.cst import *
from lkjh.data import *

class Author(Data):
	"""
	"""
	site = None
	rad = ''
	dbfields = [
		'id',
		'name',
		'urlpath',
		'open'
	]
	fields = dbfields
	
	def __init__(self, id=''):
		super().__init__('author', id)
		# self.id = id
		self.name = ''
		self.urlpath = ''
		self.open = True
	
	@property
	def url(self):
		return '{0}/{1}'.format(self.rad, self.urlpath.lstrip('/'))

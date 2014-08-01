# -*- coding: utf-8 -*-
"""
JSON.
"""
import json
from lkjh.cst import *

from pprint import pprint

class JsonFile:
	"""
	"""
	site = None
	path = DATAPATH
	
	def __init__(self, filename):
		self.filename = filename  # 'updates', 'models', ...
		
	@property
	def jsonfile(self):
		return '{0}/{1}/export/json/{2}.json'.format(self.path, self.site.abb, self.filename)
		
	def write(self, o, indent):
		with open(self.jsonfile, 'w') as fp:
			json.dump(o, fp, indent=indent)

	def read(self):
		with open(self.jsonfile, 'r') as fp:
			o = json.load(fp)
		#~ pprint(o)
		return o
		
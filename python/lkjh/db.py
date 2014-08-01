# -*- coding: utf-8 -*-
"""
DB.
"""
import logging
from lkjh.cst import *

# http://python-3-patterns-idioms-test.readthedocs.org/en/latest/Singleton.html
# http://all4dev.libre-entreprise.org/index.php/Le_singleton_en_python
# http://fr.openclassrooms.com/forum/sujet/le-design-pattern-singleton-en-python
# http://blog.amir.rachum.com/blog/2012/04/26/implementing-the-singleton-pattern-in-python/

# def singleton(cls):
	# instance = None
	# def ctor(*args, **kwargs):
		# nonlocal instance
		# if not instance:
			# instance = cls(*args, **kwargs)
		# return instance
	# return ctor

# @singleton
class DB:
	"""
	"""
	path = DBPATH
	
	def __init__(self, siteabb):
		self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
		self.siteabb = siteabb
	
	def load(self, cat):
		return {}
		
	def save(self, cat, obj):
		raise NotImplementedError


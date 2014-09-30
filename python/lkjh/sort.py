# -*- coding: utf-8 -*-
"""
Sort.
"""
import logging
import glob
import os
import re
import shutil

#~ from lkjh.cst import *

from pprint import pprint

def repinside(str, c):
	#~ print(str)
	reb = re.compile('^' + '\\' + c + '*')
	ree = re.compile('\\' + c + '*' + '$')
	sb = reb.findall(str)[0]
	se = ree.findall(str)[0]
	if se == '':
		s = str[len(sb):]
	else:
		s = str[len(sb):-len(se)]
	s = s.replace(c, ' ')  # replace inside
	s = ' '.join(s.split())  # remove multiple whitespaces
	s = sb + s + se
	return s

class Path:
	"""
	"""
	def __init__(self, root, path=''):
		self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
		self.root = os.path.normpath(root)
		#~ print('root = ' + self.root)
		if not path == '':
			path = os.path.normpath(path)
		#~ print('path = ' + path)
		if path.startswith(self.root):
			self.path = path[len(self.root)+1:]
		else:
			self.path = path
		#~ print('path = ' + self.path)

	@property
	def abspath(self):
		return os.path.join(self.root, self.path)		
	
	@property
	def basename(self):
		return os.path.basename(self.path)

	@property
	def dirname(self):
		return os.path.dirname(self.path)

	@property
	def absdirname(self):
		return os.path.dirname(self.abspath)

	@property
	def ext(self):
		try:
			return os.path.splitext(self.basename)[1].lower()
		except:
			return ''
	
	@property
	def bbasename(self):
		return os.path.splitext(self.basename)[0]
	
	@property
	def size(self):
		if self.isfile():
			return os.path.getsize(self.abspath)
		else:
			# TODO sum all files + subdir
			return -1
		
	@property
	def depth(self):
		return len(self.path.split(os.sep))-1
		
	def exists(self):
		return os.path.exists(self.abspath)
		
	def isfile(self):
		return os.path.isfile(self.abspath)
		
	def isdir(self):
		return os.path.isdir(self.abspath)
	
	def isempty(self):
		if self.isfile():
			return False
		else:
			return self.list() == []
		
	def delfrompath(self, c):
		reb = re.compile('^' + '\\' + c + '*')
		ree = re.compile('\\' + c + '*' + '$')
		sb = reb.findall(self.basename)[0]
		se = ree.findall(self.basename)[0]
		if se == '':
			s = self.basename[len(sb):]
		else:
			s = self.basename[len(sb):-len(se)]
		s = s.replace(c, ' ')  # replace inside
		s = ' '.join(s.split())  # remove multiple whitespaces
		return Path(self.root, os.path.join(self.dirname, sb + s + se))
		
	def normalize(self):
		newpath = self.delfrompath('_')
		newpath = newpath.delfrompath('.')
		return newpath
	
	def addsuffix(self, suffix='_'):
		if self.isfile():
			return Path(self.root, os.path.join(self.dirname, self.bbasename + suffix + self.ext))
		else:
			return Path(self.root, os.path.join(self.dirname, self.basename + suffix))
			
	def free(self, newpath):
		if self == newpath: return self
		if not newpath.exists(): return newpath
		
		while True:
			newpath = newpath.addsuffix()
			if not newpath.exists(): break
		return newpath

	def parent(self):
		return Path(self.root, os.path.dirname(self.abspath))
		
	def add(self, path):
		return Path(self.root, os.path.join(self.path, path))
		
	def move(self, newpath):
		# no move, same path
		if self == newpath: return
		
		# if file exists and same size -> same file, delete it
		if self.isfile() and newpath.exists() and self.size == newpath.size:
			self.logger.info("{0} -> {1}: newpath already exists.".format(self, newpath))
			#~ self.delete()
		elif self.isdir() and newpath.exists():
			self.logger.info("{0} -> {1}: newpath already exists.".format(self, newpath))
			# TODO ?
			dest = self.free(newpath)
			self.logger.info("{0} -> {1}".format(self, dest))
			shutil.move(self.abspath, dest.abspath)
			self.path = dest.path
		else:
			dest = self.free(newpath)
			self.logger.info("{0} -> {1}".format(self, dest))
			shutil.move(self.abspath, dest.abspath)
			self.path = dest.path
		
	def moveup(self):
		print(self.parent().parent().add(self.basename))
		self.move(self.parent().parent().add(self.basename))
	
	def cleanup(self):
		self.logger.debug(self)
		if self.isfile():
			if self.ext in ['.db', '.org', '.pdf', '.url', '.txt']:
				self.delete()
		else:
			for f in self.listfile():
				f.cleanup()
			
	def delete(self):
		self.logger.info(self)
		if self.isfile():
			os.remove(self.abspath)
		else:
			os.rmdir(self.abspath)
	
	def list(self, pattern='*'):
		if self.isfile():
			return None
		else:
			return [ Path(self.root, f) for f in glob.glob(self.abspath + '/' + pattern) ]
		
	def listdir(self):
		if self.isfile():
			return None
		else:
			return [ Path(self.root, os.path.join(self.abspath, f)) for f in os.listdir(self.abspath) if os.path.isdir(os.path.join(self.abspath, f)) ]
		
	def listfile(self):
		if self.isfile():
			return None
		else:
			return [ Path(self.root, os.path.join(self.abspath, f)) for f in os.listdir(self.abspath) if os.path.isfile(os.path.join(self.abspath, f)) ]
			
	def __str__(self):
		return self.path
	
	def __eq__(self, other):
		if not isinstance(other, self.__class__): return False
		return self.abspath == other.abspath
		
	def __ne__(self, other):
		return not self.__eq__(other)

	
class Sort:
	"""
	"""
	def __init__(self, path):
		self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
		self.path = path

	def listall2(self, path):
		path.cleanup()
		for p in path.list('*'):
			if p.isdir():
				print("{0}[{1}]".format('  ' * p.depth, p))
				self.listall2(p)
				if p.isempty():
					print(p, p.isempty())
					if len(p.basename) <= 5:
						p.delete()
			else:
				print("{0}{1} (size={2})".format('  ' * p.depth, p, p.size))
				if p.depth >= 2:
					p.moveup()
			
	def listall(self, limit=-1):
		for p in Path(self.path).listdir()[:limit]:
			print(p)
			p.move(p.normalize())
			self.listall2(p)
		return
		
		#~ if ext in ['.rar', '.zip']:
			#~ zfile = ZipFile(f).unpack()

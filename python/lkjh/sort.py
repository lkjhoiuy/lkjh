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
			
	def getfree(self, newpath):
		if self == newpath: return self
		if not newpath.exists(): return newpath
		
		while True:
			newpath = newpath.addsuffix()
			if not newpath.exists(): break
		return newpath

	def move(self, newpath):
		# no move, same path
		if self == newpath: return
		
		# TODO file exists, same size
		
		dest = self.getfree(newpath)
		self.logger.info("{0} -> {1}".format(self, dest))
		#~ shutil.move(self.abspath, dest.abspath)
		
	def list(self, pattern='*'):
		if self.isfile():
			return None
		else:
			return [ Path(self.root, f) for f in glob.glob(self.abspath + '/' + pattern) ]
		
	def listdir(self):
		if self.isfile():
			return None
		else:
			return [ Path(self.root, f) for f in os.listdir(self.abspath) if os.path.isdir(os.path.join(self.abspath, f)) ]
		
	def listfile(self):
		if self.isfile():
			return None
		else:
			return [ Path(self.root, f) for f in os.listdir(self.abspath)[:limit] if os.path.isfile(os.path.join(self.abspath, f)) ]
			
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
	#~ site = None
	#~ path = LIBRARIESPATH
	
	def __init__(self, path):
		self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
		self.path = path

	def newname(self, f):
		f = self.path + '/' + f
		if os.path.isfile(f):
			while os.path.exists(f):
				bn = os.path.basename(f)
				bbn, ext = os.path.splitext(bn)
				f = self.path + '/' + bbn + '_' + ext
		else:
			while os.path.exists(f):
				bn = os.path.basename(f)
				f = self.path + '/' + bn + '_'
		return f[len(self.path)+1:]
	
	def moveup(self, old):
		new = os.path.dirname(old)
		new = self.newname(new)
		old = self.path + '/' + old
		new = self.path + '/' + new

		print("move {0} -> \"{1}\"".format(old, new))
		try:
			#~ shutil.move(old, new)
			return True
		except:
			return False
		
	def movedir(self, old, new):
		new = self.newname(new)
		old = self.path + '/' + old
		new = self.path + '/' + new
		print("move {0} -> \"{1}\"".format(old, new))
		try:
			#~ shutil.move(old, new)
			return True
		except:
			return False
		
	def normdir(self, d):
		nd = repinside(d, '_')
		nd = repinside(nd, '.')
		print('"{0}"'.format(nd))
			
		if d != nd:
			self.movedir(d, nd)
		return d
		#~ return nd
	
	
	def listdir(self, rd, depth=1):
		d = self.path + '/' + rd
		if os.path.isfile(d): return
		
		l = glob.glob(d + '/*')
		if len(l) == 0:
			# dir is empty, delete it
			print('  ' * depth + "to delete")
			return
		
		for f in l:
			f = os.path.abspath(f)
			bn = os.path.basename(f)
			if os.path.isfile(f):
				size = os.path.getsize(f)
				print("{0}{1} (size={2})".format('  ' * depth, bn, size))
				if depth >= 2:
					#~ print("move up")
					self.moveup(f)
			else:
				print("{0}[{1}]".format('  ' * depth, bn))
				d = self.normdir(rd + '/' + bn)
				self.listdir(rd + '/' + bn, depth+1)
	
	def listall2(self, path, depth=1):
		for p in path.list('*'):
			if p.isfile():
				print("{0}{1} (size={2})".format('  ' * depth, p, p.size))
				if depth >= 2:
					print("move up")
			else:
				print("{0}[{1}]".format('  ' * depth, p))
				self.listall2(p, depth+1)
			
	def listall(self, limit=-1):
		#~ for p in Path(self.path).list('*')[:limit]:
		for p in Path(self.path).listdir()[:limit]:
			print(p, p.isempty())
			p.move(p.normalize())
			self.listall2(p)
		return
		
		for d in glob.glob(self.path + '/*')[:limit]:
			d = os.path.abspath(d)
			bn = os.path.basename(d)
			dn = os.path.dirname(d)
			ext = os.path.splitext(bn)[1].lower()
			isfile = os.path.isfile(d)
			size = os.path.getsize(d)
			
			d = bn
			print("[{0}]".format(d))
			d = self.normdir(d)
			self.listdir(d)
			
	def sortdirs(self):
		for dir in glob.glob(self.path + '/*')[:1]:
			self.sortdir(dir)
			
	def sortdir(self, path):
		if path.endswith('.zip'):
			os.mkdir(path[:-4])
			newpath = os.path.abspath(path[:-4] + '/' + os.path.basename(path))
			os.renames(path, newpath)
			files = [newpath]
		else:
			files = glob.glob(path + '/*.*')
			
		for f in files:
			f = os.path.abspath(f)
			bn = os.path.basename(f)
			dn = os.path.dirname(f)
			ext = os.path.splitext(bn)[1].lower()
			
			if ext in ['.db', '.org', '.pdf', '.url', '.txt']:
				os.remove(f)
			
			if ext in ['.rar', '.zip']:
				zfile = ZipFile(f).unpack()

	def guess(self, path, site):
		pass
		

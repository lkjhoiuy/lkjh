# -*- coding: utf-8 -*-
"""
Zipfile.
"""
import logging
import glob
import os
import time
from subprocess import call
import zipfile
from lkjh.cst import *

exe7z = "C:/Program Files/7-Zip/7z.exe"

from pprint import pprint

class ZipFile:
	"""
	"""
	site = None
	
	def __init__(self, zfile):
		self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
		self.zfile = os.path.abspath(zfile)
		self.bn = os.path.basename(zfile)
		self.dn = os.path.dirname(zfile)

	def test(self):
		zf = zipfile.ZipFile(self.filepath)  # mode='r', compression=zipfile.ZIP_STORED, allowZip64=False
		c = zf.read("updates.html")
		
		zf = zipfile.ZipFile(self.path + '/test2.zip', mode='w')
		zf.writestr('updates.html', c)
		zf.close()

		zf = zipfile.ZipFile(self.path + '/test3.zip', mode='w')
		zf.write(self.path + '/updates.html', 'updates.html')
		zf.close()

	def unpack(self):
		tmpdir = self.dn + '/_unzip_'
		
		args = 'e -y "{file}" -o"{dir}" *.* -r'.format(file=self.zfile, dir=tmpdir)
		rc = call('"{exe}" {args}'.format(exe=exe7z, args=args), shell=True)
		self.logger.info("{file} -> {rc}".format(file=self.bn, rc=rc))
		
		# move up
		for tmpf in glob.glob(tmpdir + '/*.*'):
			tmpf = os.path.abspath(tmpf)
			dtmpf = os.path.abspath(self.dn + '/' + os.path.basename(tmpf))
			try:
				# os.replace(tmpf, dtmpf)
				os.renames(tmpf, dtmpf)
			except:
				# verify same size
				if os.path.getsize(dtmpf) == os.path.getsize(tmpf):
					os.remove(dtmpf)
					os.renames(tmpf, dtmpf)
		
		# no more file
		if not os.path.exists(tmpdir):
			os.remove(self.zfile)

	def pack(self, path, date, h=0):
		zf = zipfile.ZipFile(self.zfile, mode='w')
		self.logger.info(path)
		
		filenames = sorted(glob.glob(path + '/*.*'), key=os.path.basename)
		
		(y,m,d) = (int(x) for x in date.split('-'))
		zinfodate = (y, m, d, 1, 0, 0)
		
		for f in filenames:
			f = os.path.abspath(f)
			zinfo = zipfile.ZipInfo()
			zinfo.filename = os.path.basename(f)
			zinfo.date_time = zinfodate
			#~ zf.write(f, os.path.basename(f))
			zf.writestr(zinfo, open(f, 'rb').read())
		zf.close()
		
		# set zip date/time
		t = time.mktime(time.strptime(date, '%Y-%m-%d'))
		os.utime(self.zfile, (t,t))

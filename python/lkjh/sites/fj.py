# -*- coding: utf-8 -*-
"""
FJ.
"""
import logging
import re
import time
from lkjh.cst import *
from lkjh.site import *
from lkjh.archive import *
from lkjh.update import *
from lkjh.model import *
from lkjh.author import *
from lkjh.cover import *
from lkjh.remotepage import *

from pprint import pprint

class xSite(Site):
	abb = 'fj'
	
	def __init__(self, dbtype='pickle'):
		super().__init__(dbtype)
		self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
		self.logger.debug(dbtype)
		
		self.init('model', xModel)
		self.init('author', xAuthor)
		self.init('cover', xCover)
		self.init('update', xUpdate)  # last position
		
		self.archive = xArchive()
		
		xArchive.site = self
		xUpdate.site = self
		xModel.site = self
		xAuthor.site = self
		xCover.site = self
		RemotePage.site = self
		JsonFile.site = self

class xArchive(Archive):
	rad = 'http://femjoy.com'
	
	def __init__(self):
		super().__init__()
	
	@property
	def urlpath(self):
		return 'sets?layout={"photo":{"max":100,"offset":0},"video":{"max":20,"offset":0}}&filter=date:' + '{0}-{1}/'.format(self.month, self.year)
		#~ return 'sets?layout={"photo":{"max":10,"offset":0},"video":{"max":1000,"offset":0}}&filter=date:' + '{0}-{1}/'.format(self.month, self.year)

	def get_updates(self, soup):
		return soup.select('div.set.data')
		
	def parse_update(self, update):
		upd_id = update.select('a.button')[0]['data-setcode']
		upd = self.site.updates.get(upd_id)
		
		#~ if not upd.open:
			#~ # verify date
			#~ if upd.date[:7] == '{0}-{1:02d}'.format(self.year, self.month):
				#~ return upd
			#~ else:
				#~ return None				
		
		upd.urlpath = upd.id
		
		date = update.select('h6')[0].get_text()
		# July 19, 2014
		date = time.strptime(date, "%B %d, %Y")
		upd.date = time.strftime("%Y-%m-%d", date)
		
		# verify date
		if not upd.date[:7] == '{0}-{1:02d}'.format(self.year, self.month):
			return None

		upd.name =  update.select('img')[0]['alt']
		if 'cover2_314x150.jpg' in update.select('img')[0]['src']:
			upd.type = 'vid'
			
		# ko: update.select('a[href|=/models/]')
		amodels = update.findAll(href=re.compile('^/models/'))
		for amodel in amodels:
			model_id = amodel['href'].split('/models/')[1]
			model = self.site.models.get(model_id)
			if model.open:
					model.name = amodel.get_text()
					if model.name.endswith('.'):
						model.name = model.name[:-1]
						model.urlpath = model.name
					model.save()
					model.update()
			upd.addmodel(model_id)

		aauth = update.findAll(href=re.compile('^/artists/'))[0]
		auth_id = aauth['href'].split('/artists/')[1]
		auth_urlpath = aauth['href'].replace(xAuthor.rad, '')
		
		auth = self.site.authors.get(auth_id)
		if auth.open:
			auth.urlpath = auth_urlpath
			auth.name = aauth.text
			auth.save()
		upd.author = auth_id

		cover = upd.getcover('cover')
		if not cover:
			cover = xCover(upd.id, 'cover')
			cover.update(upd.date)
			cover.save()
			upd.addcover(cover)

		#~ upd.update()
		upd.save()

		return upd

class xUpdate(Update):
	rad = 'http://femjoy.com/sets'
	
	def __init__(self, id=''):
		super().__init__(id)

	def parse(self, html):
		soup = super().parse(html)
		
		try:
			detail = soup.select('div#main')[0]	
			
			# delete div#set-comments
			for s in detail.select('div#set-comments'):
				s.extract()
			self.write_htmlc(detail.prettify())
		except:
			print('ERROR htmlc', self.id)
			return
		
		# if detail.select('video'):
		if not detail.select('div.cover-container div.cover img'):
			self.type = 'vid'
		
		if self.type == 'img':
			cover = self.getcover('cover')
			if not cover:
				cover = xCover(self.id, 'cover')
				img = detail.select('div.cover-container div.cover img')[0]
				try:
					cover.urlparam = img['src'].split('?')[1]
				except:
					pass
				cover.update(self.date)
				cover.save()
				self.addcover(cover)
		else:
			cover = self.getcover('wide')
			if not cover:
				cover = xCover(self.id, 'wide')
				a = detail.select('div.span-2.last a')[0]
				try:
					cover.urlparam = a['href'].split('?')[1]
				except:
					pass
				cover.update(self.date)
				cover.save()
				self.addcover(cover)
				
class xModel(Model):
	rad = 'http://femjoy.com/models?layout={"row":{"model":1},"models":{"max":30,"offset":0}}&filter=s:'
	# rad = 'http://femjoy.com/models?layout={"row":{"model":1},"models":{"max":10,"offset":0}}'
	# /models?layout={"row":{"model":1},"models":{"max":10,"offset":0}}
	# http://femjoy.com/index/models#/?s=Alba  => Alba O, Alba T
	# /models?layout={"row":{"model":1},"models":{"max":10,"offset":0}}&filter=s:maryella
	
	def __init__(self, id=''):
		super().__init__(id)

	@property
	def url(self):
		return '{0}{1}'.format(self.rad, self.urlpath.lstrip('/'))
		
	def parse(self, html):
		pass
		#~ cont = super().parse(html).select('div.model_container')[0]
		#~ self.write_htmlc(cont.prettify())

		#~ self.name = cont.select('span.model_title_name')[0].get_text()
		
		#~ cover = self.getcover('headshot')
		#~ if not cover:
			#~ cover = xCover(self.id, 'headshot')
			#~ cover.update()
			#~ cover.save()
			#~ self.addcover(cover)
		
		#~ infos = cont.select('td.model_data')
		#~ self.breasts = infos[1].get_text()
		#~ self.eyecolor = infos[2].get_text()
		#~ self.shaved = infos[3].get_text()
		#~ self.haircolor = infos[4].get_text()
		#~ self.measurements = infos[5].get_text()
		#~ self.height = infos[6].get_text()
		#~ self.country = infos[7].get_text()
		#~ self.weight = infos[8].get_text()
		#~ self.ethnicity = infos[9].get_text()
		#~ self.open = False

class xAuthor(Author):
	rad = 'http://femjoy.com/artists'
	
	def __init__(self, id=''):
		super().__init__(id)

class xCover(Cover):
	"""
	"""
	rad  = 'http://n2.femjoy.com/updates'
	_rad = 'http://n1.femjoy.com/updates'  # needs urlparam for the 2 covers of the day
	
	def __init__(self, refid='', type='cover'):
		super().__init__(refid, type)
		
		self.urls = {
			'cover'    : '{0}/{1}/{2}2_642x642.jpg'.format(self.rad, self.refid, 'cover'),
			'wide'     : '{0}/{1}/{2}2_970x463.jpg'.format(self.rad, self.refid, 'cover'),
			'headshot' : ''  # 	http://n2.femjoy.com/portraits/ashley.jpg
		}
		
		self._urls = {
			'cover'    : (lambda c: '{0}/{1}/{2}2_642x642.jpg?{3}'.format(c._rad, c.refid, 'cover', c.urlparam)),
			'wide'     : (lambda c: '{0}/{1}/{2}2_970x463.jpg?{3}'.format(c._rad, c.refid, 'cover', c.urlparam))
		}

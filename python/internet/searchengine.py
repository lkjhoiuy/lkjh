# -*- coding: utf-8 -*-
"""
"""
from collections import OrderedDict
import re
import urllib.request
from bs4 import BeautifulSoup
import json

from pprint import pprint

urlpatterns = {
	'google'     : 'http://www.google.com/search?q={query}&num=50',
	'indexxx'    : 'http://www.indexxx.com/search/?query={query}',
	'thenude'    : 'http://www.thenude.eu/index.php?page=search&action=searchModels&m_name={query}',
	'hornywhores': 'http://www.hornywhores.net/search/{query}',
}

class SearchEngine:
	def __init__(self, provider):
		self.provider = provider
		self.urlpattern = urlpatterns[provider]
		self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"}	
		self.lastquery = ""
		self.results = []
		# self.results = [{link, text}]

	def search(self, query):
		self.lastquery = urllib.parse.quote_plus(query)
		self.lastqueryurl = self.urlpattern.format(query=self.lastquery)
		try:
			req = urllib.request.Request(self.lastqueryurl, headers=self.headers)
			r = urllib.request.urlopen(req).read()
			with open(self.provider+'.'+self.lastquery+'.html', 'wb') as fp:
				fp.write(r)
			return r
		except Exception as e:
			print(e)

	def parse(self, html):
		return None
	
	def savesoup(self, soup):
		with open(self.provider+'.'+self.lastquery+'.soup.html', 'wb') as fp:
			fp.write(soup.prettify('utf-8'))
		
	def tojson(self):
		with open(self.provider+'.'+self.lastquery+'.json', 'w') as fp:
			json.dump(self.results, fp, indent=2)
			
	def tohtml(self):
		with open(self.provider+'.'+self.lastquery+'.result.html', 'wb') as fp:
			fp.write('<!-- {url} -->\n'.format(url=self.lastqueryurl).encode('utf-8'))
			fp.write(b'<html>\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n')
			for r in self.results:
				fp.write('<p><a href="{link}" target="_blank">{text}</a></p>\n'.format(link=r['link'], text=r['text']).encode('utf-8'))
			fp.write(b'</body>\n</html>\n')
	
	def __str__(self):
		return "provider: {0}, query: {1}, results: {2}".format(self.provider, self.lastquery, [r['text'].encode('utf-8') for r in self.results])


class GoogleSearchEngine(SearchEngine):

	def __init__(self):
		super().__init__('google')
		
	def parse(self, html):
		self.results = []
		soup = BeautifulSoup(html)
		
		r = soup.select('div#ires')[0]
		self.savesoup(r)
		
		links = [a['href'] for a in r.select('h3.r a')]
		entries = [span.get_text() for span in r.select('span.st')]
		
		for i in range(len(links)):
			self.results.append({'link': links[i], 'text': entries[i]})
			#~ self.results.append({'link': str.encode(links[i], 'utf-8'), 'text': str.encode(entries[i], 'utf-8')})
		

class IndexxxSearchEngine(SearchEngine):
	
	def __init__(self):
		super().__init__('indexxx')
		
	def parse(self, html):
		self.results = []
		
		r = html.split(b'<h3>Exact matches</h3>')[1].split(b'<h3>Similar names found</h3>')[0]
		soup = BeautifulSoup(r)

		self.savesoup(soup)
		
		matchs = soup.select('div.item.wrapper.model')
		for m in matchs:
			self.results.append({'link': 'http://www.indexxx.com' + m.select('a span')[0].find_parent('a')['href'], 'text': m.select('a span')[0].get_text()})

		
class ThenudeSearchEngine(SearchEngine):
	
	def __init__(self):
		super().__init__('thenude')
		
	def parse(self, html):
		self.results = []
		soup = BeautifulSoup(html)
		r = soup.select('div.blockIndexModels')[0]
		
		self.savesoup(r)
		
		links = [a['href'] for a in r.select('div.item > a:nth-of-type(1)')]
		entries = [span.get_text() for span in r.select('div.item > span')]
		
		for i in range(len(links)):
			self.results.append({'link': links[i], 'text': entries[i]})
	

class HornywhoresSearchEngine(SearchEngine):
	
	def __init__(self):
		super().__init__('hornywhores')
		
	def parse(self, html):
		self.results = []
		soup = BeautifulSoup(html)
		r = soup.select('div#content')[0]
		
		self.savesoup(r)
		
		# TODO goto post div.entry a.more-link
		matchs = soup.select('div.post h3 a')
		for m in matchs:
			self.results.append({'link': m['href'], 'text': m.get_text()})

if __name__ == "__main__":
	gse = GoogleSearchEngine()
	r = gse.search('toto tutu')
	gse.parse(r)
	gse.tojson()
	gse.tohtml()


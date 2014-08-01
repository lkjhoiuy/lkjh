# -*- coding: utf-8 -*-
"""
"""
from collections import OrderedDict
import re
import urllib.request

#~ import http.cookiejar
#~ self.cj      = cookiejar.LWPCookieJar()
#~ self.opener  = urlrequest.build_opener(urlrequest.HTTPCookieProcessor(self.cj))
#~ urlrequest.install_opener(self.opener)

#~ import email
#~ import imaplib

#~ from multiprocessing import Pool
#~ pool = Pool(processes=max_processes)
	#~ command = 'wget -q -O %s%s %s' % (data_directory, image_name, image_url)
	#~ pool.apply_async(running_command, (command, ))
#~ pool.close()
#~ pool.join()

#~ encoding = url_open.headers.getparam('charset')
#~ url_open.read().decode(encoding)

#~ user_page_url_md5 = hashlib.new('md5', user_page_url).hexdigest()
#~ url_cache = dict()
#~ if url_cache.get(user_page_url_md5) is None:
	
def myip():
	urls = OrderedDict([
		('dmiws',      'http://www.dmiws.com/myip/'),
		('curlmyip',   'http://curlmyip.com/'),
		('icanhazip',  'http://www.icanhazip.com/'),
		('dyndns',     'http://checkip.dyndns.org/'),
		('whatismyip', 'http://www.whatismyip.com/ip-address-host-name-lookup/'),
	])
	headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"}	
	
	for provider,url in urls.items():
		try:
			req = urllib.request.Request(url, headers=headers)
			r = urllib.request.urlopen(req).read().decode('utf-8')
			r = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", r)[0]
			#~ print(provider)
			return r
		except Exception as e:
			# print(provider, e)
			continue

def myuseragent():
	urls = OrderedDict([
		('whatismyip', 'http://www.whatismyip.com/user-agent-info//'),
		# <li class="user-agent">Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0</li>
	])
	headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0"}	
	
	for provider,url in urls.items():
		try:
			req = urllib.request.Request(url, headers=headers)
			r = urllib.request.urlopen(req).read().decode('utf-8')
			r = r.split('<li class="user-agent">')[1].split('</li>',1)[0]
			return r
		except Exception as e:
			continue

if __name__ == "__main__":
	print("'{0}'".format(myip()))
	print("'{0}'".format(myuseragent()))

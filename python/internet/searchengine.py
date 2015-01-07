# -*- coding: utf-8 -*-
"""
"""
from collections import OrderedDict
import os
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

SAVEPATH = 'd:/.lkjhdata/data'

class SearchEngine:
    def __init__(self, provider):
        self.provider = provider
        self.urlpattern = urlpatterns[provider]
        self.headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36"}
        self.lastsearch = ""
        self.lastquery = ""
        self.results = []  # [ {link, title, text} ]
        self.filename = None

    def openw(self, query, filesuffix):
        path = os.path.join(SAVEPATH, self.provider)
        if not os.path.exists(path):
            os.mkdir(path)
        file = os.path.join(path, self.lastquery + filesuffix)
        return open(file, 'wb')
            
    def read(self, url, save=True):
        #~ print("...read", url)
        try:
            req = urllib.request.Request(url, headers=self.headers)
            r = urllib.request.urlopen(req).read()
            if save:
                with self.openw(self.lastquery, ".html") as fp:
                    fp.write(r)
            return r
        except Exception as e:
            print(e)
            return None
        
    def search(self, query):
        self.lastsearch = query
        self.lastquery = urllib.parse.quote_plus(query)
        self.lastqueryurl = self.urlpattern.format(query=self.lastquery)
        return self.read(self.lastqueryurl)

    def parse(self, html):
        return None
    
    def savesoup(self, soup):
        with self.openw(self.lastquery, ".soup.html") as fp:
            fp.write(b'<html>\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n')
            fp.write(soup.prettify('utf-8'))
            fp.write(b'</body>\n</html>\n')
        
    def tojson(self):
        with self.openw(self.lastquery, ".json") as fp:
            json.dump(self.results, fp, indent=2)
            
    def tohtml(self):
        with self.openw(self.lastquery, ".result.html") as fp:
            fp.write('<!-- {url} -->\n'.format(url=self.lastqueryurl).encode('utf-8'))
            fp.write(b'<html>\n<head>\n<meta charset="utf-8">\n</head>\n<body>\n')
            for r in self.results:
                fp.write('<p><a href="{link}" target="_blank">{title}</a></p>\n<a href="{more}" target="_blank">more...</a>\n{text}\n'.format(link=r['link'], title=r['title'], more=r['more'], text=r['text']).encode('utf-8'))
            fp.write(b'</body>\n</html>\n')
    
    def __str__(self):
        return "provider: {0}, query: {1}, results: {2}".format(self.provider, self.lastquery, [r['text'].encode('utf-8') for r in self.results])


class GoogleSearchEngine(SearchEngine):

    def __init__(self):
        super().__init__('google')
        
    def parse(self, html):
        self.results = []
        if (html == None): return
        soup = BeautifulSoup(html)
        
        r = soup.select('div#ires')[0]
        self.savesoup(r)
        
        # self.results.append({'link': str.encode(links[i], 'utf-8'), 'text': str.encode(entries[i], 'utf-8')})
                    
        matchs = soup.select('div.rc')
        for m in matchs:
            link = m.select('h3.r a')[0]
            try:
                text = m.select('span.st')[0].get_text()
            except:
                text = ""
            self.results.append({'link': link['href'], 'title': link.get_text(), 'text': text})

class IndexxxSearchEngine(SearchEngine):
    
    def __init__(self):
        super().__init__('indexxx')
        
    def parse(self, html):
        self.results = []
        if (html == None): return
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
        if (html == None): return
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
        if (html == None): return
        
        soup = BeautifulSoup(html)
        r = soup.select('div#content')[0]
        self.savesoup(r)
        
        matchs = soup.select('div.post')
        #~ if not matchs:
            #~ print(self.lastsearch)
        for m in matchs:
            link = m.select('h3 a')[0]
            title = link.get_text()
            more = ""
            try:
                more = m.select('div.entry a.more-link')[0]['href']
            except:
                pass
            text = ""
            
            post = self.read(link['href'], False)
            post = post.decode('utf-8').replace('\n', ' ')
            
            if self.filename and not self.filename in post:
                continue
            
            # <meta name="description" content="2 Jan 2015 Meet Angie Koks http://uploaded.net/file/xbhe7694/Angie_Koks_Meet_Angie_Koks.mp4 or http://rapidgator.net/file/c90501d16d01e1fa26868805">
            # <meta name="description" content="Dreams Come True 7 Nov 2011 http://uploaded.net/file/m8u3uhmo/Alyona_Dreams_Come_True_HD.wmv or http://rapidgator.net/file/982ed27326d24c31afb2dc6">
            # <meta name="description" content="Behind The Bathroom Door 10/05/2013 http://uploaded.net/file/jklsmze6/Cindy_Behind_The_Bathroom_Door_HD.wmv or http://rapidgator.net/file/6df1e226">
            # <meta name="description" content="WowGirls.13.05.25.Addison.And.Silvie.Massage.My.Clit.XXX.1080p.MP4-KTR Download (Uploaded, Netload, Rapidgator):http://cosyupload.com/uploads/51a0a2">
            
            # <meta name="description" content="PlayBoyPlus - Chanel Elle - Pool Honey Cybergirl Chanel Elle cools it poolside in this set from photographer Damir K. As a native Californian, blonde-ha">
            # <title>Chanel Elle – Pool Honey | HornyWhores.net</title>
            # <p><strong>PlayBoyPlus - <a href="http://www.hornywhores.net/tag/chanel-elle/" class="st_tag internal_tag" rel="tag" title="Posts tagged with Chanel Elle">Chanel Elle</a> - Pool Honey</strong></p>
            
            # <meta name="description" content="NubileFilms - Jade Nile - Sensual Seduction At the end of a rough day, there's nothing quite like a lover who's willing to seduce your cares away. That'">
            # <title>Jade Nile – Sensual Seduction | HornyWhores.net</title>
            # <p><strong>NubileFilms - <a href="http://www.hornywhores.net/tag/jade-nile/" class="st_tag internal_tag" rel="tag" title="Posts tagged with Jade Nile">Jade Nile</a> - Sensual Seduction</strong></p>
            
            m = re.compile('<meta name="description" content="(.+?)(?:http://.+)?(?:XXX\.\d+p\.MP4-KTR[ :]Download .+)?(?: \w+:.+)?>').search(post)
            if m:
                text = m.group(1)
                # Delete dates " 7 Nov 2011", " 10/05/2013", "Jan 06, 2015", " January 6, 2015"
                m = re.compile('(\d?\d \w\w\w 20\d\d)').search(text)
                if m:
                    text = text.replace(m.group(1), "")
                m = re.compile('(\d\d/\d\d/20\d\d)').search(text)
                if m:
                    text = text.replace(m.group(1), "")
                m = re.compile('(\w\w\w\w* \d?\d, 20\d\d)').search(text)
                if m:
                    text = text.replace(m.group(1), "")
                # Delete dates ".14.02.23" => delete "."
                m = re.compile('(\d\d\.\d\d\.\d\d)').search(text)
                if m:
                    text = text.replace(m.group(1), "")
                    text = text.replace(".", " ")
            
            #~ m = re.compile('<title>(.+?)( \| .*)?</title>').search(post)
            #~ if m:
                #~ title = m.group(1)
                #~ title = title.replace("&#8211;", "-")
            
            #~ m1 = re.compile('</p> <p><strong>(.+?)(<br />Added:.+)?</strong>').search(post)
            #~ if m1:
                #~ text = m1.group(1)
                #~ # <a href="http://www.hornywhores.net/tag/cory-chase/" class="st_tag internal_tag" rel="tag" title="Posts tagged with Cory Chase">Cory Chase</a>
                #~ if "</a>" in text:
                    #~ m2 = re.compile('(<a href=.+?>(.+?)</a>)').findall(text)
                    #~ for m in m2:
                        #~ text = text.replace(m[0], m[1])
            #~ else:
                #~ # <p><span id="more-385141"></span><br>\nFucking A Schoolgirl 11 Jun 2012</p>
                #~ m1 = re.compile('<p><span id=.+?></span>(?:<br /> ?)?(.+?)</p>').search(post)
                #~ if m1:
                    #~ text = m1.group(1)
            
            title = title.replace("&#8211;", "-")
            title = title.replace(": ", " - ")
            text = text.strip()
            text = text.replace("  ", " ")
            text = text.replace("&amp;", "&")
            text = text.replace("&#039;", "'")
            text = text.replace("**", " - ")
            
            titles = title.split(" - ")
            texts = text.split(" - ")
            #~ pprint(titles)
            #~ pprint(texts)
            if titles == texts:
                titles = []
                    
            if len(titles) > 1 and titles[0] in text:
                titles.remove(titles[0])
            if len(titles) > 1 and titles[0] in text:
                titles.remove(titles[0])
            if len(titles) > 1:
                # No ' ' in site
                titles[0] = titles[0].replace(" ", "")
                # title in titles ?
                if len(titles) > 2 and text.endswith(titles[-1]):
                    titles.remove(titles[-1])
                title = " - ".join(titles)
                # site in texts ?
                if text.startswith(titles[0]):
                    text = text.replace(titles[0], "").lstrip()
                # models in texts ?
                if text.startswith(titles[-1] + " "):
                    text = text.replace(titles[-1] + " ", "").lstrip()
                if "," in titles[-1]:
                    mod = titles[-1].replace(",", " And")
                    if text.startswith(mod + " "):
                        text = text.replace(mod, "").lstrip()
                    mod = titles[-1].replace(",", " and")
                    if text.startswith(mod + " "):
                        text = text.replace(mod, "").lstrip()
                
            #~ print(" ", title, "|", text)
            if len(text) > 40:
                if title in text:
                    i = text.find(title)
                    if i > 0:
                        text = text[:(i+len(title))]
            if not title in text:
                text = title + " - " + text
                
            #~ print(" ", text)
            
            self.results.append({'link': link['href'], 'title': title, 'more': more, 'text': text})
        return self.results

if __name__ == "__main__":
    gse = GoogleSearchEngine()
    r = gse.search('toto tutu')
    gse.parse(r)
    gse.tojson()
    gse.tohtml()

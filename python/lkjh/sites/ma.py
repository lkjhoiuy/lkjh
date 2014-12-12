# -*- coding: utf-8 -*-
"""
MA.
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
    abb = 'ma'
    
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
    rad = 'http://guests.met-art.com/archive'
    
    def __init__(self):
        super().__init__()
        
    @property
    def urlpath(self):
        return '{0}/{1:02d}/'.format(self.year, self.month)

    def get_updates(self, soup):
        return soup.select('ul.table_list')
        
    def parse_update(self, update):
        lis = update.select('li')
        
        # .../media/6419A9D1A15B9EDC3B2D00A6A13C143D/t_cover_6419A9D1A15B9EDC3B2D00A6A13C143D.jpg
        upd_id = re.findall('.+/media/(.+)/t_cover_.+', lis[0].a.img['src'])[0]
        upd = self.site.updates.get(upd_id)
        
        if not upd.open:
            # verify date
            if upd.date[:7] == '{0}-{1:02d}'.format(self.year, self.month):
                return upd
            else:
                return None                
        
        # "/janika-a-and-kira-i-and-sylvie-deluxe/gallery/20100323/SPRAY/"
        upd.urlpath = lis[0].a['href'].replace(upd.rad, '')
        
        # vid ? no url
        if 'popMovieCover' in upd.urlpath:
            upd.urlpath = ''
            upd.type = 'vid'
        
        allmodels = []
        if upd.urlpath:
            allmodels = re.findall('/(.+)/gallery/.+', upd.urlpath)[0]
            allmodels = allmodels.split('-and-')  # /ennie-a-and-jenni-a-and-katerina-i/ split -> 3 models max
            
        date = lis[1].text
        # dd.mm.yyyy
        date = time.strptime(date, "%d.%m.%Y")
        upd.date = time.strftime("%Y-%m-%d", date)

        # verify date
        if not upd.date[:7] == '{0}-{1:02d}'.format(self.year, self.month):
            return None
        
        cover = upd.getcover('cover')
        if not cover:
            cover = xCover(upd.id, 'cover')
            cover.update(upd.date)
            cover.save()
            upd.addcover(cover)
        
        cover = upd.getcover('alt')
        if not cover:
            cover = xCover(upd.id, 'alt')
            cover.update(upd.date)
            cover.save()
            upd.addcover(cover)
        
        if upd.type == 'vid':
            cover = upd.getcover('wide')
            if not cover:
                cover = xCover(upd.id, 'wide')
                cover.update(upd.date)
                cover.save()
                upd.addcover(cover)
                
                # duree, cf http://m.met-art.com/model/olga-m/movie/20130630/NATARAN/
                # http://m.met-art.com/model/olga-m/gallery/20070608/PLENILUNA/
            
        i = 3 if (upd.type == 'img') else 2
        amodels = lis[i].select('a')  # only the 2 first models here
        
        for amodel in amodels:
            # /ketrin-b/
            model_urlpath = amodel['href'].replace(xModel.rad, '')
            model_id = re.findall('/(.+)/', model_urlpath)[0]
            model = self.site.models.get(model_id)
            if model.open:
                model.urlpath = model_urlpath
                model.name = model.id2name()  # predictif
                model.save()
                model.update()
                
            upd.addmodel(model_id)
            if allmodels:
                allmodels.remove(model_id)

        i += 1
        upd.name = lis[i].text
        
        i += 1
        auth_urlpath = lis[i].a['href'].replace(xAuthor.rad, '')
        auth_id = re.findall('/(.+)/', auth_urlpath)[0]
        auth = self.site.authors.get(auth_id)
        if auth.open:
            auth.urlpath = auth_urlpath
            auth.name = lis[i].text.replace('By ', '')
            auth.save()
        upd.author = auth_id
        
        # TODO delete By author formupd.name
        if upd.name.endswith(' By {0}'.format(auth.name)):
            upd.name = upd.name.replace(' By {0}'.format(auth.name), '')
        if ' by ' in upd.name.lower():
            self.logger.error(upd.name)
        
        if upd.type == 'img':
            i += 1
            upd.count = int(lis[i].text.replace(' photos', ''))

        # 3 models detected but not 4 models -> look for update
        if allmodels:
            # the 3rd model
            for model_id in allmodels:
                model = self.site.models.get(model_id)
                if model.open:
                    model.urlpath = '/{0}/'.format(model_id)
                    model.name = model.id2name()  # predictif
                    model.save()
                    model.update()

                upd.addmodel(model_id)
            upd.update()  # for the 4th model
        
        upd.open = False
        upd.save()
        return upd

class xUpdate(Update):
    rad = 'http://guests.met-art.com/model'
    
    def __init__(self, id=''):
        super().__init__(id)

    @property
    def localpath(self):
        return self.urlpath.split('gallery')[1]
        
    def parse(self, html):
        soup = super().parse(html)
        
        detail = soup.select('div.details_series')[0]
        self.write_htmlc(detail.prettify())
        
        actors = detail.select('span[itemprop="actor"]')
        for actor in actors:
            amodel = actor.find('a')
            model_urlpath = amodel['href'].replace(xModel.rad, '')
            model_id = re.findall('/(.+)/', model_urlpath)[0]
            
            if not model_id in self.models:
                model = self.site.models.get(model_id)
                if model.open:
                    model.urlpath = model_urlpath
                    model.save()
                    model.update()
                self.addmodel(model_id)
                
class xModel(Model):
    rad = 'http://www.elitebabes.com/model'
    rad = 'http://guests.met-art.com/model'
    
    def __init__(self, id='', data={}):
        super().__init__(id)
        if data:
            self.importFrom(data)

    def parse(self, html):
        if not html: return
        
        cont = super().parse(html)
        try:
            cont = cont.select('div.model_container')[0]
            self.write_htmlc(cont.prettify())
        except:
            # cf There is no model named Tina C.
            print("ERROR", self.id)
            self.write_htmlc("")
            return
        
        self.name = cont.select('span.model_title_name')[0].get_text()
        cover = self.getcover('headshot')
        if not cover:
            cover = xCover(self.id, 'headshot')
            cover.update()
            cover.save()
            self.addcover(cover)

        infos = cont.select('td.model_data')
        self.breasts = infos[1].get_text()
        self.eyecolor = infos[2].get_text()
        self.shaved = infos[3].get_text()
        self.haircolor = infos[4].get_text()
        self.measurements = infos[5].get_text()
        self.height = infos[6].get_text()
        self.country = infos[7].get_text()
        self.weight = infos[8].get_text()
        self.ethnicity = infos[9].get_text()
        self.open = False

class xAuthor(Author):
    rad = 'http://guests.met-art.com/photographer'
    
    def __init__(self, id=''):
        super().__init__(id)

class xCover(Cover):
    rad = 'http://static.met-art.com/media'
    
    def __init__(self, refid='', type='cover'):
        super().__init__(refid, type)
        
        self.urls = {
            'cover'    : '{0}/{1}/{2}_{3}.jpg'.format(self.rad, self.refid, 'cover', self.refid),
            'alt'      : '{0}/{1}/{2}_{3}.jpg'.format(self.rad, self.refid, 'clean', self.refid),
            'wide'     : '{0}/{1}/{2}_{3}.jpg'.format(self.rad, self.refid, 'wide', self.refid),
            'headshot' : '{0}/{1}/{2}.jpg'.format(self.rad, 'headshots', self.refid)
        }

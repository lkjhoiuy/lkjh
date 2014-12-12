# -*- coding: utf-8 -*-
"""
Archive.
"""
import os
from lkjh.cst import *
from lkjh.data import *

class Archive(Data):
    """
    """
    site = ''
    path = DATAPATH
    rad = ''
    offline = False
    fields = [
        'id',
        'year',
        'month'
    ]
    
    def __init__(self):
        super().__init__('archive')
        # self.id = id
        self.cur_htmlupdates = []
        self.cur_updates = []
        
    @property
    def urlpath(self):
        raise NotImplementedError
        
    @property
    def url(self):
        return '{0}/{1}'.format(self.rad, self.urlpath)
        
    @property
    def localpath(self):
        return '{0}-{1:02d}'.format(self.year, self.month)
        
    @property
    def csvfile(self):
        return '{0}/{1}/export/csv/{2}.csv'.format(self.path, self.site.abb, self.year)

    def read(self, year, month, force=False):
        self.year = year
        self.month = month
        return super().read(force)
        
    def get_updates(self, soup):
        raise NotImplementedError

    def parse_update(self, e):
        raise NotImplementedError
    
    def parse(self, html):
        soup = super().parse(html)
        htmlupdates = self.get_updates(soup)
        self.logger.info("{0}-{1:02d}: {2} updates...".format(self.year, self.month, len(htmlupdates)))
        
        htmlc = []
        self.cur_updates = []
        for htmlupdate in htmlupdates:
            update = self.parse_update(htmlupdate)
            htmlc.append(htmlupdate.prettify())
            if update:
                self.cur_updates.append(update.fmt4csv() + '\n')
                
        self.write_htmlc(htmlc)
        return not htmlc == []
        
    def writecsv(self):
        if self.cur_updates:
            with open(self.csvfile, 'a') as f:
                f.writelines(self.cur_updates)
    
    def delcsv(self, year):
        self.year = year
        if os.path.exists(self.csvfile):
            os.remove(self.csvfile)

    def concatcsv(self, year1, year2):
        with open('{0}/{1}/export/csv/{1}.csv'.format(self.path, self.site.abb), 'w') as allf:
            for year in range(year1, year2, -1):
                self.year = year
                if os.path.exists(self.csvfile):
                    with open(self.csvfile, 'r') as f:
                        allf.write(f.read())

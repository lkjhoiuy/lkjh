# -*- coding: utf-8 -*-
"""
Site.
"""
import logging
import operator
from lkjh.cst import *
from lkjh.archive import *
from lkjh.db_pickle import *
from lkjh.db_json import *
from lkjh.jsonfile import *

from pprint import pprint

class SiteElement:
    """
    """
    def __init__(self, cat, xclass, db=None):
        self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
        self.cat = cat  # 'update', 'model', 'author', 'cover'
        self.xclass = xclass
        self.db = db
        self.elements = {}  # dict, elements are Data

    def get(self, id):
        """If not known, retun a new element."""
        #~ self.logger.debug("(%s) %s", self.cat, id)
        if id in self.elements:
            return self.elements[id]
        else:
            return self.xclass(id)
    
    # cat = 'update'
    # Filter models in element
    def filtermodel(self, modelid):
        r = []
        for value in self.values():
            if modelid in value.models:
                r.append(value)
        return r
        
    def set(self, elem, id=None):
        id = id or elem.id
        self.elements[id] = elem
        #~ self.logger.debug("%s = %s", id, self.elements[id])
    
    # Unused
    #~ def setlist(self, elem, id=None):
        #~ id = id or elem.id
        #~ if not id in self.elements.keys():
            #~ self.elements[id] = []
        #~ if not elem in self.elements[id]:
            #~ self.elements[id].append(elem)
        #~ self.logger.debug("[%s] = %s", id, self.elements[id])
            
    def sortedkeys(self):
        return sorted(self.elements)
    
    def values(self):
        return self.elements.values()
    
    @property
    def count(self):
        return len(self.values())
    
    def sortedvalues(self):
        return [self.elements[k] for k in sorted(self.elements)]
    
    def sortedvalues_by(self, order='date', reverse=False):
        return sorted(self.values(), key=lambda elem: getattr(elem, order), reverse=reverse)
    
    # DB
    def load(self, db=None):
        db = db or self.db
        elems = db.load(self.cat)
        self.logger.debug(len(elems))
        for e in elems:
            o = self.xclass().importFrom(e)
            self.set(o)

    def save(self, db=None):
        db = db or self.db
        if self.cat == 'update':
            db.save(self.cat, self.dbexport_by('date', reverse=True))    
        else:
            db.save(self.cat, self.dbexport())
        
    def export(self, id=None):
        """Return given id or all elements."""
        if id:
            return self.elements[id].export()
        else:
            return [value.export() for value in self.sortedvalues()]
            
    def export_by(self, order='date', reverse=False):
        return [value.export() for value in self.sortedvalues_by(order, reverse)]

    def dbexport(self, id=None):
        """Return given id or all elements."""
        if id:
            return self.elements[id].dbexport()
        else:
            return [value.dbexport() for value in self.sortedvalues()]
            
    def dbexport_by(self, order='date', reverse=False):
        return [value.dbexport() for value in self.sortedvalues_by(order, reverse)]

#
# Site
#
class Site:
    """
    """
    abb = ''
    rad = ''
    
    def __init__(self, dbtype='pickle'):
        self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
        self.archive = None
        self.dbtype = dbtype
        self.colls = {}

    def init(self, cat, xclass, dbtype=None):
        dbtype = dbtype or self.dbtype
        self.logger.info("{0} ({1})".format(cat, dbtype))
        
        se = SiteElement(cat, xclass, self.db(dbtype))
        se.load()
        self.colls[cat] = se
    
    def db(self, dbtype):
        if dbtype == 'pickle':
            return DBPickle(self.abb)
        elif dbtype == 'json':
            return DBJson(self.abb)
        else:
            return None
        
    @property
    def cats(self):
        return self.colls
        
    @property
    def updates(self):
        return self.colls['update']
    @property
    def models(self):
        return self.colls['model']
    @property
    def authors(self):
        return self.colls['author']
    @property
    def covers(self):
        return self.colls['cover']
        
    def save(self, dbtype=None):
        #~ for cat in self.cats:
            #~ self.colls[cat].save()
        dbtype = dbtype or self.dbtype
        for se in self.colls.values():
            se.save(self.db(dbtype))
            
    def update(self, year, month, force=False):
        """Update site from archive."""
        
        html = self.archive.read(year, month, force)
        if not html:
            self.logger.error("{0}-{1:02d}: NOT read.".format(year, month))
        elif self.archive.parse(html):
            self.logger.info("{0}-{1:02d}: updated.".format(year, month))
        else:
            self.logger.error("{0}-{1:02d}: NOT updated.".format(year, month))
        
    def get_updateByFp(self, fp):
        return [upd for upd in self.updates.values() if upd.fingerprint == fp]
        
    def search_updateByFp(self, s):
        l = list(s.lower())
        l.sort()
        fp = ''.join(l).lstrip(' _-,.:?!&%"()/\'')
        self.logger.info(fp)
        return [upd.id for upd in self.get_updateByFp(fp)]

    def export_modelupdates(self, id):
        cat = 'model'
        r = self.colls[cat].get(id).export()
        upds = [upd.export() for upd in self.updates.filtermodel(id)]
        # order by date
        r['updates'] = sorted(upds, key=lambda upd: upd['date'], reverse=True)
        return r
    
    def json_export(self, cats=[]):
        cats = cats or self.cats
        for cat in cats:
            if cat == 'update':
                JsonFile(cat+'s').write(self.colls[cat].export_by('date', reverse=True), 2)    
            else:
                JsonFile(cat+'s').write(self.colls[cat].export(), 2)
    
    def importFrom(self, cat, elems):
        for e in elems:
            self.colls[cat].xclass().importFrom(e)

    def json_import(self, cats=[]):
        cats = cats or self.cats
        for cat in cats:
            self.logger.info(cat)
            self.importFrom(cat, JsonFile(cat+'s').read())

    def delcsv(self, year):
        self.archive.delcsv(year)

    def writecsv(self):
        self.archive.writecsv()
        
    def concatcsv(self, year1, year2):
        self.archive.concatcsv(year1, year2)
    
# -*- coding: utf-8 -*-
"""
DB Pickle.
"""
import logging
import os
import pickle
from lkjh.db import *

class DBPickle(DB):
    """
    """
    def __init__(self, siteabb):
        super().__init__(siteabb)
        self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
        self.path = "{0}/{1}/db/pickle".format(self.path, self.siteabb)
    
    def dbfile(self, cat):
        return '{0}/{1}s{2}'.format(self.path, cat, '.p')
    
    def load(self, cat):
        file = self.dbfile(cat)
        self.logger.info(file)
        
        if os.path.exists(file):
            with open(file, 'rb') as fp:
                return pickle.load(fp)
        else:
            return []
                
    def save(self, cat, elements):
        file = self.dbfile(cat)
        self.logger.info(file)
        
        with open(file, 'wb') as fp:
            pickle.dump(elements, fp)
        

    
# -*- coding: utf-8 -*-
"""
DB Json.
"""
import logging
import os
import json
from lkjh.db import *

class DBJson(DB):
    """
    """
    def __init__(self, siteabb):
        super().__init__(siteabb)
        self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
        self.path = "{0}/{1}/db/json".format(self.path, self.siteabb)

    def dbfile(self, cat):
        return '{0}/{1}s{2}'.format(self.path, cat, '.json')
        
    def load(self, cat):
        file = self.dbfile(cat)
        self.logger.info(file)
        
        if os.path.exists(file):
            with open(file, 'r') as fp:
                return json.load(fp)
        else:
            return []

    def save(self, cat, elements, indent=2):
        file = self.dbfile(cat)
        self.logger.info(file)
        
        with open(file, 'w') as fp:
            json.dump(elements, fp, indent=indent)


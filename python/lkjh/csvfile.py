# -*- coding: utf-8 -*-
"""
CSV.
"""
from lkjh.cst import *

class CsvFile:
    """
    """
    site = None
    path = DATAPATH
    
    def __init__(self, filename):
        self.filename = filename  # 'updates', 'models', ...
        
    @property
    def csvfile(self):
        return '{0}/{1}/export/csv/{2}.csv'.format(self.path, self.site.abb, self.filename)
        
    def write(self, o, indent):
        with open(self.csvfile, 'w') as fp:
            # json.dump(o, fp, indent=indent)
            pass

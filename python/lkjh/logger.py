# -*- coding: utf-8 -*-
"""
"""
import logging
from lkjh.cst import *

def init(filename, clevel=logging.INFO):
    logger = logging.getLogger('lkjh')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(clevel)
    fmt = logging.Formatter('{name}:{funcName} - {message}', style='{')
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    
    fh = logging.FileHandler(LOGPATH+'/'+filename)
    fh.setLevel(logging.DEBUG)
    fmt = logging.Formatter('{asctime} - {levelname:7s} - {name}:{funcName} - {message}', style='{', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    
    logger.debug('*'*30)

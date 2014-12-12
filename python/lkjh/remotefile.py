# -*- coding: utf-8 -*-
"""
File.
"""
import logging
import os
import urllib.request
import zlib
import hashlib
from lkjh.cst import *

class RemoteFile:
    """
    """
    
    def __init__(self, localfile, url=None):
        self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
        self.localfile = localfile
        self.url = url
        
    def localfile_exists(self):
        return os.path.exists(self.localfile)
        
    def download(self):
        self.logger.info('... download "{0}" ({1})'.format(os.path.basename(self.localfile), self.url))
        r = ''
        try:
            resp = urllib.request.urlopen(self.url)
            r = resp.read()
            resp.close()
        except Exception as e:
            self.logger.error(str(e))
            r = '\n'.join([self.url, str(e)])
        return r

    def testremote(self, buf):
        ext = os.path.splitext(self.localfile)[1].lower()
        try:
            if ext == '.jpg':
                buffertext = buf[:100].decode('utf-8').lower()
                if '<!doctype html>' in buffertext:
                    return ''
        except:
            pass
        return buf
        
    def readlocal(self):
        if self.localfile_exists():
            with open(self.localfile, 'rb') as f:
                return f.read()
        return None
    
    def read(self):
        self.logger.debug("{0} ...".format(os.path.basename(self.localfile)))
        if self.localfile_exists():
            return self.readlocal()
        else:
            r = self.download()
            # test redir
            if r:
                r = self.testremote(r)
            # write localfile
            try:
                self.writelocal(r)
            except:
                self.writelocal(r.encode('utf-8'))
            return r

    def writelocal(self, buf):
        if not os.path.exists(os.path.dirname(self.localfile)):
            os.makedirs(os.path.dirname(self.localfile))
        with open(self.localfile, 'wb') as f:
            f.write(buf)
        
    @property
    def isdownloaded(self):
        return os.path.exists(self.localfile)
        
    @property
    def size(self):
        try:
            return os.path.getsize(self.localfile)
        except:
            return -1
    
    @property
    def crc32(self):
        if not os.path.exists(self.localfile): return -1
        prev = 0
        with open(self.localfile, 'rb') as f:
            for eachLine in f:
                prev = zlib.crc32(eachLine, prev)
        return prev & 0xffffffff
        
    @property
    def xcrc32(self):
        return "%08x" % self.crc32

    @property
    def md5(self):
        if not os.path.exists(self.localfile): return ''
        
        md5 = hashlib.md5()
        # md5 on all the file?
        with open(self.localfile, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                md5.update(buf)            
                buf = f.read(65536)
        return md5.hexdigest()

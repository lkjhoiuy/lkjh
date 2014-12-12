# -*- coding: utf-8 -*-
"""
Downloaded.
"""
import logging
import glob
import os
import re
import shutil
from subprocess import call

from lkjh.cst import *
from lkjh.remotefile import *
from lkjh.zipfile import *

from pprint import pprint

class Downloaded:
    """
    """
    site = None
    path = LIBRARIESPATH
    
    def __init__(self, path):
        self.logger = logging.getLogger('lkjh.'+self.__class__.__name__)
        self.path = path

    def sortdirs(self):
        for dir in glob.glob(self.path + '/*')[:1]:    
            self.sortdir(dir)
            
    def sortdir(self, path):
        if path.endswith('.zip'):
            os.mkdir(path[:-4])
            newpath = os.path.abspath(path[:-4] + '/' + os.path.basename(path))
            os.renames(path, newpath)
            files = [newpath]
        else:
            files = glob.glob(path + '/*.*')
            
        for f in files:
            f = os.path.abspath(f)
            bn = os.path.basename(f)
            dn = os.path.dirname(f)
            ext = os.path.splitext(bn)[1].lower()
            
            if ext in ['.db', '.org', '.pdf', '.url', '.txt']:
                os.remove(f)
            
            if ext in ['.rar', '.zip']:
                zfile = ZipFile(f).unpack()

    def guess(self, path, site):
        prefix = '_'
        if path.endswith('.zip'):
            path = path[:-4]
            #~ prefix = '_'
        files = glob.glob(path + '/*.*')

        for f in files:
            f = os.path.abspath(f)
            bn = os.path.basename(f)
            dn = os.path.dirname(f)
            ext = os.path.splitext(bn)[1].lower()
            
            if ext in ['.db', '.org', '.pdf', '.url', '.txt']:
                os.remove(f)
                
            if bn.startswith('_') or bn.startswith('['):
                os.renames(f, dn + '/!' + bn[1:])
            elif 'cover' in bn and not bn.startswith('!'):
                os.renames(f, dn + '/!' + bn)

        filenames = sorted(glob.glob(path + '/*.*'), key=os.path.basename)
        filesizes = sorted(glob.glob(path + '/*.*'), key=os.path.getsize)
        
        #~ i = 0
        #~ if 'flogo.jpg' in filenames[i] or '-cover-clear.jpg' in filenames[i]:
            #~ i += 1
        
        for coverfile in filesizes[0:3]:
            cf = RemoteFile(coverfile)
            self.logger.info("cover = '{file}'".format(file=os.path.basename(coverfile)))
            md5 = cf.md5
            cover = site.covers.get(md5)
            if cover.open: continue
            
            id = cover.refid
            upd = site.updates.get(id)
            self.logger.info('  ({0}) {1} {2} {3}'.format(cover.ctype, upd.title, upd.date, upd.count))
            os.renames(coverfile, dn + '/' + '__0000' + '.jpg')
            
            if (upd.count) and len(filenames) <= int(upd.count):
                self.logger.error("%s (%s) -> %d (manque .jpg)", upd.title, upd.count, len(filenames))
                
            n = 0
            alt = False
            filenames = sorted(filenames)
            self.logger.info("    Renaming...")
            for f in filenames[1:]:
                bnf = os.path.basename(f)
                if bnf == "__0000.jpg": raise Error
                d = re.findall('.*_?([\d]+)\.jpg$', bnf)
                if d:
                    #~ pprint(d)
                    d = int(d[0])
                    n += 1
                    #~ print(d, n)
                    os.renames(f, dn + '/' + '__{0:04d}.jpg'.format(n))
                
                # TODO delete other files !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                else:
                    if not alt:
                        cover = upd.getcover('alt')
                        if cover and cover.id == RemoteFile(f).md5:
                                os.remove(f)
                                alt = True
                                break
                        if alt:
                            continue
                
            for f in glob.glob(path + '/*.*'):
                if os.path.basename(f).startswith('__'):
                    os.renames(f, dn + '/' + os.path.basename(f)[2:])
            
            dnf = os.path.dirname(dn) + '/' + upd.filename
            dnf = os.path.abspath(dnf)
            if dn != dnf:
                while os.path.exists(dnf):
                    dnf += '_'
                os.renames(dn, dnf)
            
            suffix = ''
            if n != upd.count:
                self.logger.error("%s (%s) -> %d", upd.title, upd.count, n)
                suffix = ' ERR'
                if len(filenames) < 8:
                    suffix = ' VID'
                
            dnff = os.path.dirname(dnf) + '/_old_/' + os.path.basename(dnf)
            self.gozip(dnf, upd.date, prefix, suffix, dnff)
            break
        else:
            #~ return
            # MetArt_Sumita_Solveig_high
            # Met_Art_13_08_20_Emmi_A_And_Marena_A_Ondeto_XXX_1080p_x264_PAYiSO
            dnb = os.path.basename(dn)
            if dnb.endswith('_high'):
                dnb = dnb[:-5]
            if dnb.endswith('_med'):
                dnb = dnb[:-4]
            if dnb.endswith('_h'):
                dnb = dnb[:-2]
            if dnb.endswith('_m'):
                dnb = dnb[:-2]
            self.logger.info("'{0}'...".format(dnb))
            ids = site.search_updateByFp(dnb)
            for id in ids:
                upd = site.updates.get(id)
                self.logger.info("-> {0} ({1}) {2} {3}".format(upd.title, upd.count, upd.date, upd.id))
                
                cover = upd.getcover('cover')
                if cover:
                    shutil.copy2(cover.localfile, dn+'/!'+upd.id+'.jpg')
            if ids:
                dnf = os.path.dirname(dn) + '/__ok__' + dnb
                os.renames(dn, dnf)
        
    def gozip(self, dnf, date, prefix, suffix, dnff):
        underscore = ''
        zipfile = '{0}/{1}{2}{3}{4}.zip'.format(os.path.dirname(dnf), prefix, os.path.basename(dnf), suffix, underscore)
        while os.path.exists(zipfile):
            underscore += '_'
            zipfile = '{0}/{1}{2}{3}{4}.zip'.format(os.path.dirname(dnf), prefix, os.path.basename(dnf), suffix, underscore)
        
        zfile = ZipFile(zipfile).pack(dnf, date)
        
        while os.path.exists(dnff):
            dnff += '_'
        os.renames(dnf, dnff)
        if os.path.exists(zipfile) and os.path.getsize(zipfile) > 20000000:
            print('delete', dnff)
            shutil.rmtree(dnff)
    
    def do(self, site, count=-1, ziponly=False, dironly=False):
        if ziponly:
            pattern = '/*.zip'
        elif dironly:
            pattern = '/*/'
        else:
            pattern = '/*'
        filespattern = self.path + pattern
        #~ print(filespattern)
        dirs = sorted(glob.glob(filespattern), key=os.path.basename)[:count]
        #~ print(dirs)
        for dir in dirs:
            dn = os.path.dirname(dir)
            if dn.endswith('_old_') or dn.endswith('_TODO_') or dn.endswith('__ok__'):
                continue
            self.logger.info(os.path.basename(dir))
            self.sortdir(dir)
            self.guess(dir, site)

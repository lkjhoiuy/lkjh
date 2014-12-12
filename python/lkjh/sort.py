# -*- coding: utf-8 -*-
"""
Sort.
"""
import logging
import glob
import os
import re
import shutil
from subprocess import call

from lkjh.remotefile import *
from lkjh.zipfile import *

from pprint import pprint

EXE7Z = "C:/Program Files/7-Zip/7z.exe"

class SortError(Exception):
    pass

class Path:
    """
    """
    def __init__(self, root, path=''):
        """
        """
        self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)
        if path != '':
            path = os.path.normpath(path)
        if isinstance(root, Path):
            self.root = root.root
            path = os.path.join(root.path, path)
        else:
            self.root = os.path.normpath(root)
        if path.startswith(self.root):
            self.path = path[len(self.root)+1:]
        else:
            self.path = path
        if self.path.startswith('/'): self.path = self.path[1:]
        #~ print(self.root, self.path, self.abspath)

    @property
    def abspath(self):
        return os.path.join(self.root, self.path)        
    
    @property
    def basename(self):
        return os.path.basename(self.path)

    @basename.setter
    def basename(self, value):
        if value == self.basename: return
        self.move(Path(self.root, os.path.join(self.dirname, value)))
        
    @property
    def dirname(self):
        return os.path.dirname(self.path)

    @property
    def absdirname(self):
        return os.path.dirname(self.abspath)

    @property
    def ddirname(self):
        return os.path.split(self.absdirname)[-1]
        
    @property
    def ext(self):
        try:
            return os.path.splitext(self.basename)[1].lower()
        except:
            return ''
    
    @property
    def bbasename(self):
        return os.path.splitext(self.basename)[0]
    
    @property
    def size(self):
        if self.isfile():
            return os.path.getsize(self.abspath)
        else:
            size = 0
            for p in self.list():
                size += p.size
            return size
        
    def isempty(self):
        return self.size == 0

    @property
    def depth(self):
        """Number of '/' in path."""
        return len(self.path.split(os.sep))-1
        
    def exists(self):
        return os.path.exists(self.abspath)
        
    def isfile(self):
        return os.path.isfile(self.abspath)
        
    def isdir(self):
        return os.path.isdir(self.abspath)
    
    def isvid(self):
        if self.isfile():
            pass
        else:
            return len(self.list('*.avi')) + len(self.list('*.mov')) + len(self.list('*.mp4')) + len(self.list('*.wmv')) + len(self.list('*.m4v')) > 0
    
    @staticmethod
    def delfrom(name, c):
        reb = re.compile('^' + '\\' + c + '*')
        ree = re.compile('\\' + c + '*' + '$')
        sb = reb.findall(name)[0]
        se = ree.findall(name)[0]
        if se == '':
            s = name[len(sb):]
        else:
            s = name[len(sb):-len(se)]
        s = s.replace(c, ' ')  # replace inside
        s = ' '.join(s.split())  # remove multiple whitespaces
        return sb + s + se
        
    def normalize(self):
        newbn = Path.delfrom(self.basename, '_')
        if self.isfile():
            if newbn.startswith('_') or newbn.startswith('['):
                newbn = '!' + newbn[1:]
            elif 'cover' in newbn and not newbn.startswith('!'):
                newbn = '!' + newbn
        else:
            newbn = Path.delfrom(newbn, '.')
            newbn = newbn.replace(' com ', ' ')
            newbn = re.sub(r' HD$', '', newbn)
            newbn = re.sub(r' FullHD$', '', newbn)
            newbn = re.sub(r' (video)$', '', newbn)
            newbn = re.sub(r' vid$', '', newbn)
            newbn = re.sub(r' mp4$', '', newbn)
            newbn = re.sub(r' [Pp]hotos$', '', newbn)
            newbn = re.sub(r' high$', '', newbn)
            newbn = re.sub(r' h$', '', newbn)
            newbn = re.sub(r' -$', '', newbn)
            # string.capwords(newbn)
        self.basename = newbn.strip()
    
    def addsuffix(self, suffix='_'):
        if self.isfile():
            return Path(self.root, os.path.join(self.dirname, self.bbasename + suffix + self.ext))
        else:
            return Path(self.root, os.path.join(self.dirname, self.basename + suffix))
            
    def free(self, newpath):
        if self == newpath: return self
        if not newpath.exists(): return newpath
        
        while True:
            newpath = newpath.addsuffix()
            if not newpath.exists(): break
        return newpath

    def parent(self):
        return Path(self.root, self.absdirname)
        
    def add(self, path):
        return Path(self.root, os.path.join(self.path, path))
        
    # same path -> no move
    # if file exists and same size -> same file, delete it
    def move(self, newpath):
        """
        """
        # string parameter -> path object
        if isinstance(newpath, str):
            newpath = self.add(newpath)
            
        if self == newpath:
            return
        if self.isfile() and newpath.exists() and self.size == newpath.size:
            self.logger.info("{0} -> {1}: newpath same -> deleted.".format(self, newpath))
            self.delete()
            return
        if self.isdir():
            if newpath.exists() and newpath.isdir() and self.size == newpath.size:
                self.logger.info("{0} -> {1}: newpath same -> deleted.".format(self, newpath))
                self.delete()
                return
            if newpath.exists() and newpath.isempty():
                self.logger.info("{0} -> {1}: newpath same -> deleted.".format(self, newpath))
                newpath.delete()
        dest = self.free(newpath)
        try:
            self.logger.debug("{0} -> {1}".format(self, dest))
        except:
            pass
        shutil.move(self.abspath, dest.abspath)
        self.path = dest.path
    
    def moveup(self):
        """Dir or file."""
        self.move(self.parent().parent().add(self.basename))

    def pack(self):
        if self.isfile(): return
    
    def unpack(self):
        tmp = Path(self.root, os.path.join(self.dirname, '_unpack_'))
        args = 'e -y "{file}" -o"{dir}" *.* -r'.format(file=self.abspath, dir=tmp.abspath)
        ret = call('"{exe}" {args}'.format(exe=EXE7Z, args=args), shell=True)
        tmp.move(Path(self.root, self.abspath[:-4]))
        if ret == 0:
            self.logger.info("{ret} ({file})".format(ret=ret, file=self))
            self.delete()
        else:
            self.logger.error("{ret} ({file})".format(ret=ret, file=self))
    
    def unpack_file(self):
        if self.isfile(): return
        for f in self.listfile():
            if f.ext in ['.rar', '.zip']:
                f.unpack()
            
    def cleanup_file(self):
        if self.isfile():
            if self.basename == '.DS_Store' \
                or self.ext in ['.db', '.nfo', '.org', '.pdf', '.txt', '.url']:
                self.delete()
        else:
            if self.basename == '__MACOSX': self.delete()
            for f in self.listfile():
                f.cleanup_file()
            
    def delete(self):
        self.logger.info(self)
        if self.isfile():
            os.remove(self.abspath)
        else:
            # os.rmdir() KO for non empty dir
            shutil.rmtree(self.abspath, ignore_errors=True)
    
    # TODO sorted file '_' before '0'
    def list(self, pattern='*', key=None):
        if self.isfile():
            return None
        else:
            if key:
                return [ Path(self.root, f) for f in sorted(glob.glob(self.abspath + '/' + pattern), key=key) ]
            else:
                return [ Path(self.root, f) for f in glob.glob(self.abspath + '/' + pattern) ]
        
    def listdir(self):
        if self.isfile():
            return None
        else:
            try:
                print(self.abspath)
            except:
                pass
            return [ self.add(f) for f in os.listdir(self.abspath) if os.path.isdir(os.path.join(self.abspath, f)) ]
        
    def listfile(self, key=None):
        if self.isfile():
            return None
        else:
            if key:
                l = [ os.path.join(self.abspath, f) for f in os.listdir(self.abspath) if os.path.isfile(os.path.join(self.abspath, f)) ]
                return [ self.add(f) for f in sorted(l, key=key) ]
            else:
                return [ self.add(f) for f in os.listdir(self.abspath) if os.path.isfile(os.path.join(self.abspath, f)) ]
            
    def __str__(self):
        return self.path
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__): return False
        return self.abspath == other.abspath
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def cleanup_dir(self):
        self.logger.info("[{0}]...".format(self))
        if self.isfile(): return
        if self.isempty():
            bn = self.basename
            if len(bn) <= 8:
                self.delete()
            elif bn.lower() in self.parent().basename.lower():
                self.delete()

class PathSite(Path):
    """
    """
    def __init__(self, root, path=''):
        """
        """
        super().__init__(root, path)

    def issite_18og(self):
        if self.basename.lower().startswith('18onlygirls'): return True
        return False

    def issite_18xg(self):
        if self.basename.lower().startswith('18xgirls'): return True
        return False

    def issite_21n(self):
        if self.basename.lower().startswith('21naturals'): return True
        return False

    def issite_aa(self):
        if self.basename.lower().startswith('amourangels'): return True
        if len(glob.glob(self.abspath + '/' + "AmourAngels*")) > 0: return True
        return False
        
    def issite_al(self):
        if self.basename.lower().startswith('al '): return True
        return False
        
    def issite_als(self):
        if self.basename.lower().startswith('alsscan'): return True
        if len(glob.glob(self.abspath + '/' + "als*")) > 0: return True
        return False
        
    def issite_amk(self):
        if self.basename.lower().startswith('amkingdom'): return True
        return False

    def issite_atk(self):
        if self.basename.lower().startswith('atkhairy'): return True
        if self.basename.lower().startswith('atkpetites'): return True
        if self.basename.lower().startswith('atkpremium'): return True
        return False
        
    def issite_ave(self):
        if self.basename.lower().startswith('ave '): return True
        if self.basename.lower().startswith('averotica '): return True
        if len(glob.glob(self.abspath + '/' + "square.jpg")) > 0: return True
        return False

    def issite_bbs(self):
        if self.basename.lower().startswith('babes '): return True
        if len(glob.glob(self.abspath + '/' + "s970x545.jpg")) > 0: return True
        return False

    def issite_bp(self):
        if self.basename.lower().startswith('bikinipleasure '): return True
        if len(glob.glob(self.abspath + '/' + "bikinipleasure*")) > 0: return True
        return False

    def issite_ddg(self):
        if self.basename.lower().startswith('dd '): return True
        if self.basename.lower().startswith('ddg '): return True
        if self.basename.lower().startswith('digitaldesire '): return True
        return False

    def issite_dom(self):
        if self.basename.lower().startswith('domai '): return True
        return False

    def issite_ea(self):
        if self.basename.lower().startswith('ea '): return True
        if self.basename.lower().startswith('erroticaarchive'): return True
        if self.basename.lower().startswith('errotica-archive'): return True
        if len(glob.glob(self.abspath + '/' + "ErroticaArchive*")) > 0: return True
        return False

    def issite_eb(self):
        if self.basename.lower().startswith('eb '): return True
        if self.basename.lower().startswith('eroticbeauty'): return True
        if len(glob.glob(self.abspath + '/' + "EB_*")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "EB *")) > 0: return True
        return False

    def issite_ed(self):
        if self.basename.lower().startswith('ed '): return True
        if self.basename.lower().startswith('eternaldesire'): return True
        if len(glob.glob(self.abspath + '/' + "Eternal*")) > 0: return True
        return False

    def issite_fg(self):
        if self.basename.lower().startswith('fgn '): return True
        return False
        
    def issite_fil(self):
        if self.basename.lower().startswith('fallinlust '): return True
        return False
        
    def issite_fj(self):
        if self.basename.lower().startswith('fj '): return True
        if len(glob.glob(self.abspath + '/' + "femjoy*")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "*970x463.jpg")) > 0: return True
        return False
        
    def issite_ha(self):
        if self.basename.lower().startswith('ha '): return True
        if self.basename.lower().startswith('hegreart'): return True
        if self.basename.lower().startswith('hegre-art'): return True
        if len(glob.glob(self.abspath + '/' + "Hegre-Art*")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "*001xxxxxl.jpg")) > 0: return True
        return False
        
    def issite_hr(self):
        if self.basename.lower().startswith('hollyrandall '): return True
        if self.basename.lower().startswith('hr '): return True
        if len(glob.glob(self.abspath + '/' + "Holly*")) > 0: return True
        return False
        
    def issite_gn(self):
        if self.basename.lower().startswith('gn '): return True
        if self.basename.lower().startswith('gn-'): return True
        if self.basename.lower().startswith('goddesses'): return True
        if self.basename.lower().startswith('goddessesnudes'): return True
        if len(glob.glob(self.abspath + '/' + "Goddess*")) > 0: return True
        return False
        
    def issite_itc(self):
        if self.basename.lower().startswith('itc '): return True
        if self.basename.lower().startswith('inthecrack'): return True
        if self.basename.lower().startswith('in the crack'): return True
        return False
        
    def issite_jm(self):
        if self.basename.lower().startswith('jm '): return True
        if self.basename.lower().startswith('joymii '): return True
        return False
    def issite2_jm(self):
        if len(glob.glob(self.abspath + '/' + "r-1280x720.jpg")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "r-1920x1080.jpg")) > 0: return True
        return False
        
    def issite_ma(self):
        if len(glob.glob(self.abspath + '/' + "MetArt*")) > 0: return True
        return False
        
    def issite_kha(self):
        if self.basename.lower().startswith('karupsha '): return True
        return False
        
    def issite_kpc(self):
        if self.basename.lower().startswith('karupspc '): return True
        return False
        
    def issite_mcn(self):
        if self.basename.lower().startswith('mcn '): return True
        if self.basename.lower().startswith('mc-nudes'): return True
        if self.basename.lower().startswith('mcnudes'): return True
        if len(glob.glob(self.abspath + '/' + "mc nudes*")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "mcnudes*")) > 0: return True
        return False
        
    def issite_mnd(self):
        if self.basename.lower().startswith('mnd '): return True
        if self.basename.lower().startswith('mynakeddolls'): return True
        return False
        
    def issite_mpl(self):
        if self.basename.lower().startswith('mp '): return True
        if self.basename.lower().startswith('mpl '): return True
        if self.basename.lower().startswith('mplstudios'): return True
        r = glob.glob(self.abspath + '/' + "????_lg.jpg")
        if len(r) == 0: return False
        name = r[0][len(self.abspath)+1:]
        return re.match('\d{4}_lg.jpg$', name)
        
    def issite_mr(self):
        if self.basename.lower().startswith('massageroom '): return True
        if len(glob.glob(self.abspath + '/' + "mr.*")) > 0: return True
        return False
    
    def issite_nb(self):
        if self.basename.lower().startswith('nubiles'): return True
        return False
    
    def issite_nf(self):
        if self.basename.lower().startswith('nubilefilms'): return True
        return False
    
    def issite_ntb(self):
        if self.basename.lower().startswith('nutabu '): return True
        if self.basename.lower().startswith('n '): return True
        return False
    
    def issite_pen(self):
        if self.basename.lower().startswith('penthouse'): return True
        return False
        
    def issite_pb(self):
        if self.basename.lower().startswith('playboyplus'): return True
        return False
    
    def issite_ra(self):
        if self.basename.lower().startswith('ra '): return True
        if self.basename.lower().startswith('rylskyart '): return True
        if self.basename.lower().startswith('rylsky-art '): return True
        if len(glob.glob(self.abspath + '/' + "RA_*")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "RA *")) > 0: return True
        return False
        
    def issite_sa(self):
        if self.basename.lower().startswith('sa '): return True
        if len(glob.glob(self.abspath + '/' + "SexArt*")) > 0: return True
        return False
        
    def issite_sb(self):
        if self.basename.lower().startswith('sb '): return True
        if self.basename.lower().startswith('showybeauty '): return True
        return False
        
    def issite_sfg(self):
        if self.basename.lower().startswith('sinfulgoddesses '): return True
        return False
        
    def issite_sk(self):
        if self.basename.lower().startswith('sk '): return True
        if self.basename.lower().startswith('skokoff '): return True
        return False
        
    def issite_st18(self):
        if self.basename.lower().startswith('stunning18 '): return True
        if len(glob.glob(self.abspath + '/' + "Stunning *")) > 0: return True
        return False
        
    def issite_tle(self):
        if self.basename.lower().startswith('tle '): return True
        if len(glob.glob(self.abspath + '/' + "TheLifeErotic*")) > 0: return True
        return False
        
    def issite_tlhc(self):
        if self.basename.lower().startswith('tlhc '): return True
        if len(glob.glob(self.abspath + '/' + "tlhc.*")) > 0: return True
        return False
        
    def issite_tm(self):
        if self.basename.lower().startswith('teenmodels '): return True
        return False
        
    def issite_tw(self):
        if self.basename.lower().startswith('t '): return True
        if self.basename.lower().startswith('twisty '): return True
        if self.basename.lower().startswith('twistys '): return True
        return False
        
    def issite_vt(self):
        if self.basename.lower().startswith('vt '): return True
        if self.basename.lower().startswith('vivthomas '): return True
        return False
        
    def issite_w4b(self):
        if self.basename.lower().startswith('w4b '): return True
        if self.basename.lower().startswith('watch4beauty '): return True
        return False
        
    def issite_wlt(self):
        if self.basename.lower().startswith('welivetogether '): return True
        return False
        
    def issite_wog(self):
        if self.basename.lower().startswith('wg '): return True
        if self.basename.lower().startswith('wowgirls '): return True
        if self.basename.lower().startswith('wow-girls '): return True
        return False
        
    def issite_wop(self):
        if self.basename.lower().startswith('wp '): return True
        if self.basename.lower().startswith('wowporn '): return True
        return False
        
    def issite_xa(self):
        if self.basename.lower().startswith('x '): return True
        if self.basename.lower().startswith('xa '): return True
        if self.basename.lower().startswith('x-art '): return True
        if self.basename.lower().startswith('x art '): return True
        if len(glob.glob(self.abspath + '/' + "x-art*")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "thumb 1.jpg")) > 0: return True
        if len(glob.glob(self.abspath + '/' + "thumb_1.jpg")) > 0: return True
        return False
        
    def issite_ylp(self):
        if self.basename.lower().startswith('ylp '): return True
        if self.basename.lower().startswith('younglegalporn '): return True
        return False
        
    def issite_zem(self):
        if self.basename.lower().startswith('zem '): return True
        if self.basename.lower().startswith('zemani '): return True
        if len(glob.glob(self.abspath + '/' + "!cover-big.jpg")) > 0: return True
        return False
        
    def issite(self, site):
        if self.isfile(): return
        if site == '18og': return self.issite_18og()
        if site == '18xg': return self.issite_18xg()
        if site == '21n' : return self.issite_21n()
        if site == 'aa'  : return self.issite_aa()
        if site == 'al'  : return self.issite_al()
        if site == 'als' : return self.issite_als()
        if site == 'amk' : return self.issite_amk()
        if site == 'atk' : return self.issite_atk()
        if site == 'ave' : return self.issite_ave()
        if site == 'bbs' : return self.issite_bbs()
        if site == 'bp'  : return self.issite_bp()
        if site == 'ddg' : return self.issite_ddg()
        if site == 'dom' : return self.issite_dom()
        if site == 'ea'  : return self.issite_ea()
        if site == 'eb'  : return self.issite_eb()
        if site == 'ed'  : return self.issite_ed()
        if site == 'fg'  : return self.issite_fg()
        if site == 'fil' : return self.issite_fil()
        if site == 'fj'  : return self.issite_fj()
        if site == 'gn'  : return self.issite_gn()
        if site == 'ha'  : return self.issite_ha()
        if site == 'hr'  : return self.issite_hr()
        if site == 'itc' : return self.issite_itc()
        if site == 'jm'  : return self.issite_jm()
        if site == 'kha'  : return self.issite_kha()
        if site == 'kpc'  : return self.issite_kpc()
        if site == 'ma'  : return self.issite_ma()
        if site == 'mcn' : return self.issite_mcn()
        if site == 'mnd' : return self.issite_mnd()
        if site == 'mpl' : return self.issite_mpl()
        if site == 'mr'  : return self.issite_mr()
        if site == 'nb'  : return self.issite_nb()
        if site == 'nf'  : return self.issite_nf()
        if site == 'ntb' : return self.issite_ntb()
        if site == 'pb'  : return self.issite_pb()
        if site == 'pen' : return self.issite_pen()
        if site == 'ra'  : return self.issite_ra()
        if site == 'sa'  : return self.issite_sa()
        if site == 'sb'  : return self.issite_sb()
        if site == 'sfg' : return self.issite_sfg()
        if site == 'sk'  : return self.issite_sk()
        if site == 'st18': return self.issite_st18()
        if site == 'tle' : return self.issite_tle()
        if site == 'tlhc': return self.issite_tlhc()
        if site == 'tm'  : return self.issite_tm()
        if site == 'tw'  : return self.issite_tw()
        if site == 'vt'  : return self.issite_vt()
        if site == 'w4b' : return self.issite_w4b()
        if site == 'wlt' : return self.issite_wlt()
        if site == 'wog' : return self.issite_wog()
        if site == 'wop' : return self.issite_wop()
        if site == 'xa'  : return self.issite_xa()
        if site == 'ylp'  : return self.issite_ylp()
        if site == 'zem' : return self.issite_zem()
        return False

    def issite2(self, site):
        if self.isfile(): return
        if site == 'jm'  : return self.issite2_jm()
        return False

    SITES = ['18og', '18xg', '21n', 'aa', 'al', 'als', 'amk', 'atk', 'ave', 'bbs', 'bp', 'ddg', 'dom',
        'ea', 'eb', 'ed', 'fg', 'fil', 'fj', 'gn', 'ha', 'hr', 'itc', 'jm', 'kha', 'kpc',
        'ma', 'mcn', 'mnd', 'mpl', 'mr', 'nb', 'nf', 'ntb', 'pb', 'ra',
        'sa', 'sb', 'sfg', 'sk', 'st18', 'tle', 'tlhc', 'tm', 'tw', 'vt',
        'w4b', 'wlt', 'wog', 'wop', 'xa', 'ylp', 'zem']

    def movesite(self):
        for site in PathSite.SITES:
            if self.issite(site):
                print(site, self.basename.encode())
                # character-code.com
                # \x92 (Right single quote) -> ' (single quote)
                # cp1252 par défaut
                self.basename = '_' + site + '/' + self.basename
        for site in PathSite.SITES:
            if self.issite2(site):
                print(site, self.basename.encode())
                self.basename = '_' + site + '/' + self.basename
    
class Sort:
    """
    """
    def __init__(self, p):
        self.logger = logging.getLogger('lkjh.' + self.__class__.__name__)

    def clean(self, p, depth=2):
        """Clean dir or file recursively."""
        if p.isdir():
            self.logger.info("{0}[{1}]".format('  '*p.depth, p.basename))
            p.normalize()
            p.unpack_file()
            p.cleanup_file()
            for pp in p.listfile():
                self.clean(pp)
            for pp in p.listdir():
                self.clean(pp)
            if p.depth >= 1:
                p.cleanup_dir()
        else:
            self.logger.debug("{0}{1} (size={2})".format('  '*p.depth, p.basename, p.size))
            p.normalize()
            # print(p.depth, p)
            if p.depth >= depth:
                p.moveup()
    
    def rename(self, p):
        """Rename dir with longer empty subdir name if exists."""
        for pp in p.listdir():
            if pp.isempty():
                if p.basename.lower() in pp.basename.lower():
                    bn = pp.basename
                    pp.delete()
                    p.basename = bn
    
    def guess(self, p, site):
        filenames = p.listfile(key=os.path.basename)
        filesizes = p.listfile(key=os.path.getsize)
        
        for coverfile in filesizes[0:3]:
            cf = RemoteFile(coverfile.abspath)
            self.logger.info("from file '{0}'".format(coverfile.basename))
            md5 = cf.md5
            cover = site.covers.get(md5)
            if cover.open: continue
            
            id = cover.refid
            upd = site.updates.get(id)
            self.logger.info("  ({0}) '{1}' / {2} / {3}".format(cover.ctype, upd.title, upd.date, upd.count))
            
            if cover.ctype == 'cover':
                # delete empty dir
                for d in p.listdir():
                    if d.isempty():
                        d.delete()
                # delete -clean.jpg
                alt = p.list('*-clean.jpg')
                if len(alt) == 1 and alt[0].size < 1024000:
                    alt[0].delete()
                    
                coverfile.basename = '__0000.jpg'
                if upd.count and len(filenames)-1 < upd.count:
                    self.logger.error("{0} ({1}) -> {2} missing.".format(upd.title, upd.count, upd.count-len(filenames)+1))
                    
                n = 0
                err = False
                for f in p.list(key=os.path.basename):
                    bnf = f.basename
                    if bnf == "__0000.jpg": continue
                    d = re.findall('.*?_?([\d]+)\.jpg$', bnf)  # .*? non-greedy
                    if not d:
                        err = True
                        #~ raise SortError("Error")
                    else:
                        d = int(d[0])
                        n += 1
                        while d > n:
                            err = True
                            n += 1
                        f.basename = '__{0:04d}.jpg'.format(n)
                    
                for f in p.list():
                    if f.basename.startswith('__'):
                        f.basename = f.basename[2:]
                
                if err:
                    zip = p.free(Path(p.root, upd.filename + '_ERR.zip'))
                else:
                    zip = p.free(Path(p.root, upd.filename + '.zip'))
                zfile = ZipFile(zip.abspath).pack(p.abspath, upd.date)
                if zip.exists() and zip.size > 20000000:
                    p.delete()
                break

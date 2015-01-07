    #-*- coding: utf-8 -*-
"""
Sort.
"""
import time
import lkjh.logger
from lkjh.sort import *
import lkjh.sites.ma as ma_
import lkjh.sites.fj as fj_


def sort_img_vid(p):
    img = Path(p, '_img')
    vid = Path(p, '_vid')
    s = Sort(p)
    
    for pp in p.listdir()[:]:
        if pp.basename.startswith('_'): continue
        s.clean(pp, depth=2)
        s.rename(pp)
        if pp.isvid():
            dest = PathSite(pp.root, os.path.join('_vid', pp.basename))
        else:
            dest = PathSite(pp.root, os.path.join('_img', pp.basename))
        pp.move(dest)
        dest.movesite()

def guess_img_vid(p):
    img = Path(p, '_img')
    vid = Path(p, '_vid')
    
    for pp in img.listdir()[:]:
        if pp.basename.startswith('_'): continue
        PathSite(pp.root, os.path.join('_img', pp.basename)).movesite()
    for pp in vid.listdir()[:]:
        if pp.basename.startswith('_'): continue
        PathSite(pp.root, os.path.join('_vid', pp.basename)).movesite()
    
def arch_img(p):
    s = Sort(p)
    ma = Path(p, '_img/_ma')
    site = ma_.xSite('json')
    for pp in ma.listdir()[:]:
        if pp.basename.startswith('_'): continue
        try:
            s.guess(pp, site)
        except SortError:
            continue

def resort_img(n, abb):
    p = "d:/.lkjhdata/ts"
    img = Path(p+"/img{0}/{1}".format(n, abb))
    vid = Path(p+"/vid{0}/{1}".format(n, abb))
    s = Sort(vid)
    
    for pp in vid.listdir()[:]:
        if pp.basename.startswith('_'): continue
        s.clean(pp, depth=2)
        s.rename(pp)
        if not pp.isvid():
            dest = PathSite(img, pp.basename)
            pp.move(dest)

def guess_img_vid2(p):
    img = Path(p, '_img')
    vid = Path(p, '_vid')
    
    for pp in vid.listdir()[:]:
        if pp.basename.startswith('_'): continue
        PathSite(pp.root, os.path.join('_vid', pp.basename)).movesite2()
        time.sleep(3)
    for pp in img.listdir()[:]:
        if pp.basename.startswith('_'): continue
        PathSite(pp.root, os.path.join('_img', pp.basename)).movesite2()
        time.sleep(3)

def all(p):
    sort_img_vid(p)
    print(len(PathSite.SITES), "sites")
    guess_img_vid(p)
    arch_img(p)
    guess_img_vid2(Path(path))

def sort5(path):
    gse = HornywhoresSearchEngine()
    for pp in path.listfile(key=os.path.basename)[:]:
        if pp.basename.startswith('_'): continue
        
        gse.filename = pp.basename
        pat = pp.bbasename.replace('_', ' ')
        r = gse.search(pat)
        results = gse.parse(r)
        gse.tohtml()
        if not results:
            pp.basename = '_' + '/' + pp.basename
        else:
            for r in results:
                try:
                    print(pp.basename + "\t" + r['text'] + pp.ext + "\t" + r['link'])
                except:
                    try:
                        print(pp.basename + "\t" + str(r['text'].encode('utf-8')) + pp.ext + "\t" + r['link'])
                    except:
                        pass

        time.sleep(1)


if __name__ == "__main__":
    lkjh.logger.init("sort.log")
    path = "d:/.lkjhdata/dl/tmp4"
    
    #~ all(Path(path))
    #~ # resort_img(4, 'ylp')
    
    path = "d:/.lkjhdata/dl/tbs5/_/test"
    #~ path = "d:/.lkjhdata/dl/tbs5/_TODO"
    #~ path = "d:/.lkjhdata/dl/dl3"
    #~ path = "d:/.lkjhdata/ts/vid5/wowg"
    sort5(Path(path))
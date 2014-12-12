    #-*- coding: utf-8 -*-
"""
Sort.
"""
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

def all(p):
    sort_img_vid(p)
    print(len(PathSite.SITES), "sites")
    guess_img_vid(p)
    arch_img(p)

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


if __name__ == "__main__":
    lkjh.logger.init("sort.log")
    
    path = "d:/.lkjhdata/dl/tmp4"
    all(Path(path))

    #~ resort_img(4, 'ylp')
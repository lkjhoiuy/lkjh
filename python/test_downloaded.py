# -*- coding: utf-8 -*-
"""
Test downloaded.
"""
import lkjh.logger
from lkjh.downloaded import *
import lkjh.sites.ma as ma_
import lkjh.sites.fj as fj_


if __name__ == "__main__":

	lkjh.logger.init("test.log")
	
	# TODO delete ...-clean.jpg
	
	path = "d:/.lkjhdata/ts/img2/ma/"
	
	d = Downloaded(path)
	d.do(ma_.xSite('json'), dironly=True)  # , ziponly=True)  # dironly=True)  #, ziponly=True)

	# Landysh A => Shereen A
	# Verona A => Verona B
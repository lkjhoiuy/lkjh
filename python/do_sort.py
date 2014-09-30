# -*- coding: utf-8 -*-
"""
Sort.
"""
import lkjh.logger
from lkjh.sort import *

from pprint import pprint


if __name__ == "__main__":

	lkjh.logger.init("sort.log")
	
	path = "d:/.lkjhdata/dl/tmp4"
	
	d = Sort(path)
	d.listall(10)
	
	#~ pprint(repinside("abcd_efgh", '_'))
	#~ pprint(repinside("abcd_efgh_", '_'))
	#~ pprint(repinside("_abcd_efgh", '_'))
	#~ pprint(repinside("_abcd_efgh_", '_'))
	#~ pprint(repinside("__abcd__efgh__", '_'))

	#~ pprint(repinside("abcd.efgh", '.'))
	#~ pprint(repinside("abcd.efgh.", '.'))
	#~ pprint(repinside(".abcd.efgh", '.'))
	#~ pprint(repinside(".abcd.efgh.", '.'))
	#~ pprint(repinside("..abcd..efgh..", '.'))

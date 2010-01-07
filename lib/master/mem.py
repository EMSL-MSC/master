#!/usr/bin/python
"""A library to use decode_dimms.pl to gather memory properties."""

import os
import master
import re
import time
import fcntl
import errno
import select
#from master.util import *

def getMemoryInfo():
	"""Gather memory info and return a dictionary"""

	memmap={}
	bank = ''
	found = ''

	if not os.access(master.config['decode-dimms'],os.X_OK):
		master.debug("Error finding:"+master.config['decode-dimms'])
		return {}

	p = os.popen(master.config['decode-dimms'],"r")

	for l in p.readlines():
		if 'bank' in l:
			bank = l.split().pop()

		found = foundMemInfo(l)
		if found:
			memmap["dimm."+bank+"."+found.keys()[0]] =  found[found.keys()[0]]

	return memmap
	

def foundMemInfo(line):	
	"""Check line for important memory info.
	Memory info is returned as a dictionary entry.  If no
	info is found then an empty string is returned.
	Possible matches include:
	1. Manufacturer  ('mem.manufacturer')
	2. Serial Number ('mem.serial')
	3. Part Number   ('mem.part_number')
	"""

	foundManufacturer = re.compile("Manufacturer")
	foundSerialNo = re.compile("Assembly")
	foundPartNo = re.compile("Part Number")

	if foundManufacturer.match(line):
		return {"manufacturer": line[12:].strip()}
		
	if foundSerialNo.match(line):
		return {"serial": line[22:].strip()}

	if foundPartNo.match(line):
		return{"part_number": line[11:].strip()}

	return ''

def _test():
	d=getMemoryInfo()
	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]


if __name__ == "__main__":
	_test()

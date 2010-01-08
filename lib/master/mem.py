#!/usr/bin/python
"""A library to use decode_dimms.pl to gather dimm properties."""

import os
import master
import re

def getMemoryInfo():
	"""getMemoryInfo() -> dictionary
	This function relies on 'decode-dimms' to gather 
	pertinent dimm information.  It also requires 
	kernel modules 'eeprom' and 'i2c-i801'.
	"""

	memmap={}
	bank = ''
	found = {}

	if not os.access(master.config['decode_dimms'],os.X_OK):
		master.debug("Error finding:"+master.config['decode_dimms'])

		return {}

	p = os.popen(master.config['decode_dimms'],"r")

	for l in p.readlines():
		if 'bank' in l:
			bank = l.split().pop()

		found = foundMemInfo(l)
		
		if found:
			memmap["dimm."+bank+"."+found.keys()[0]] =  found[found.keys()[0]]
	p.close()	

	if not memmap:
		master.debug("Error: No dimm information found. * Requires 'eeprom' and 'i2c-i801' kernel modules *")
	
	return memmap
	

def foundMemInfo(line):	
	"""foundMemInfo(line) -> (single dictionary entry)

	Memory info is returned as a dictionary entry.  If no
	info is found then an empty dictionary is returned.
	Possible matches include:
	1. Manufacturer  ('dimm.x.manufacturer')
	2. Serial Number ('dimm.x.serial')
	3. Part Number   ('dimm.x.part_number')
	** x = [dimm bank] **
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

	return {}

def _test():
	d=getMemoryInfo()
	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]


if __name__ == "__main__":
	_test()

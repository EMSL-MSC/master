#!/usr/bin/python
"""A library to use hpacucli to gather properties from the HP/compaq cciss Smart Array Cards."""

import os
import master
import re
from master.util import *

os.environ['LD_LIBRARY_PATH']="/home/efelix/hpacucli/bld/"

def getSmartArraySlotInfo(slot):
	slotmap = { 
			'Firmware Version'   : 'fwver',
			'Hardware Revision'  : 'hwrev',
			'Serial Number'      : 'serial',
	}
	drivemap = {
			'Model'              : 'model',
			'Size'               : 'capacity',
			'Serial Number'      : 'serial',
			'Firmware Revision'   : 'fwver',
	}

	if not os.access(master.config['hpacucli'],os.X_OK):
                return {}

	p = os.popen(master.config['hpacucli']+" ctrl slot="+slot+" show detail")
	info = doLineParse(p.readlines(),'smartarray.s'+slot,slotmap)
	p.close()

	p = os.popen(master.config['hpacucli']+" ctrl slot="+slot+" physicaldrive all show")
	lines =  p.readlines()
	p.close()

	findit = re.compile(".*physicaldrive ([^ ]*) .*")
	for line in lines:
		found = findit.match(line)
		if found:
			id = found.groups()[0]
			p = os.popen(master.config['hpacucli']+" ctrl slot="+slot+"  physicaldrive "+id+" show")
			info.update(doLineParse(p.readlines(),'smartarray.s'+slot+'.'+id,drivemap))
			p.close()

	return info


def getAllSmartArrayInfo():
	if not os.access(master.config['hpacucli'],os.X_OK):
		return {}

	info = {}

	p = os.popen(master.config['hpacucli']+" ctrl all show")
	lines = p.readlines()
	p.close()

	findit = re.compile("Smart Array ([^ ]*) in Slot ([0-9]*).*")
	
	for line in lines:
		found = findit.match(line)
		if found:
			type,slot = found.groups()
			info['smartarray.s'+slot+'.type']=type
			info.update(getSmartArraySlotInfo(slot))

	return info

def _test():
	d=getAllSmartArrayInfo()
	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]


if __name__ == "__main__":
		_test()


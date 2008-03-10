#!/usr/bin/python
"""A library to use omreport to gather properties from the DELL PERC Cards."""

import ssv
import os
import re
from master.util import *

def getControllerDiskInfo(id):
	"""getControllerDriveInfo(id,disktype) -> dictionary"""

	cmap = { 
		"Firmware Version":"fwver",
		"Driver Version":"driverver",
		"Serial Number":"serial",
		"Serial":"serial",
		"Model":"model",
		"Capacity":"capacity",
		"Status":"status",
 	}

	findit_p = re.compile("^(p[0-9]*) .*")
	info={}

	if not os.access("/usr/bin/tw_cli",os.X_OK):
		return {}

	p = os.popen("/usr/bin/tw_cli /"+id+" show all","r")
	clines = []
	ports = []
	for l in p.readlines():
		found = findit_p.match(l)
		if found:
			ports += [found.groups()[0]]
		if l.find("/"+id)==0:
			clines.append(l[len(id)+2:])
	p.close()

	info.update(doLineParse(clines,"amcc."+id,cmap,"="))

	for port in ports:
		name="/%s/%s"%(id,port)
		p = os.popen("/usr/bin/tw_cli "+name+" show all","r")
		plines = []
		for l in p.readlines():
			if l.find(name) == 0:
				plines.append(l[len(name)+1:])

		info.update(doLineParse(plines,"amcc"+name.replace("/","."),cmap,"="))

	return info


def getAllAMCCInfo():
	"""getAllAMCCInfo() -> dictionary"""
	findit_c = re.compile("^(c[0-9]*) .*")

	infos = {}

	if not os.access("/usr/bin/tw_cli",os.X_OK):
		return {}

	p=os.popen("/usr/bin/tw_cli show","r")
	ids = []
	for l in p.readlines():
		found = findit_c.match(l)
		if found:
			ids.append(found.groups()[0])
	p.close()
	
	for c in ids: 
		infos.update(getControllerDiskInfo(c))

	return infos

def _test():
	d=getAllAMCCInfo()
	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]


if __name__ == "__main__":
		_test()


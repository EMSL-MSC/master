#!/usr/bin/python
"""A library to use omreport to gather properties from the DELL PERC Cards."""

import ssv
from os import popen

def mapit(dict,map,prefix):
	"""mapit(dict,map,prefix) -> dictionary
	copy data from dictionary according to map, while appending prefix
	"""

	infos={}
	for key in dict.keys():
		if key in map.keys():
			infos[prefix+"."+map[key]]=dict[key]

	return infos

def getControllerDiskInfo(id,disktype):
	"""getControllerDriveInfo(id,disktype) -> dictionary"""

	dmap = { 
		"pdisk":{ "Capacity":"capacity","Vendor ID":"vendor","Product ID":"model","Serial No.":"serial" },
		"vdisk":{ "Capacity":"capacity","Status":"status","Name":"name","State":"state","Layout":"layout" }
	}
	info={}

	p=popen("omreport storage %s controller=%s -fmt ssv"%(disktype,id),"r")
	l=ssv.getSSVDicts(p)
	p.close()

	for d in l:
		did = d["ID"]
		info.update(mapit(d,dmap[disktype],"perc.c"+id+"."+disktype+"."+did))

	return info


def getAllPERCInfo():
	"""getAllPERCInfo() -> dictionary"""

	cmap = { "Firmware Version":"fwver","Name":"name" }
	infos = {}

	p=popen("omreport storage controller -fmt ssv","r")
	l=ssv.getSSVDicts(p)
	p.close()
	
	for d in l: 
		id=d["ID"]
		infos.update(mapit(d,cmap,"perc.c"+id))

		infos.update(getControllerDiskInfo(id,"pdisk"))
		infos.update(getControllerDiskInfo(id,"vdisk"))

	return infos

def _test():
	d=getAllPERCInfo()
	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]


if __name__ == "__main__":
		_test()


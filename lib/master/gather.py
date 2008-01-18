#!/usr/bin/python
"""A library of hardware gathering functions"""

import os

def _debug(msg):
	pass

def fileGrab(file):
	"""fileGrab(file) => list

	Return a list of all lines in given file
	"""
	f=open(file,"r")
	lines=f.readlines()
	f.close()
	return lines

def lineGrab(file):
	"""lineGrab(file) => string

	Grab the first line of a given filei
	"""
	return fileGrab(file)[0].rstrip()

def getMAC(interface):
	"""getMAC(interface) => dictionary
	
	get the MAC address of a given network interface
	"""
	return {interface+'.mac':lineGrab("/sys/class/net/"+interface+"/address")}

def getAllMAC():
	"""getALLMAC() => dictionary
	Return 
	"""

	ints = os.listdir("/sys/class/net/")
	d = {}
	for x in ints: 
		d.update(getMAC(x))
	return d


_scsibase="/sys/class/scsi_disk/"
def getScsiInfo(device):
	"""getScsiInfo(device) => dictionary

	device - chan:target:id:lun string from /sys/class/scsi_disk/
	Retrieve model number, serial number and firmware revision of a scsi device
	"""
	dir=_scsibase+device
	if not os.access(dir,os.X_OK):
		_debug("error reading:"+dir)
		return {}
	
	#Find the block device...  its kinda hackish... is there a better way
	#FIXME figure out a gooder way?
	l = os.listdir(dir):
	block=None
	for i in l:
		if i.find("block:")==0:
			block = i
			break
	
	if not block:
		_debug("error finding block in list")
		return {}

	dev = '/dev/'+block.split(':')[2]
	if not os.access(dev,os.R_OK|os.W_OK):
		_debug("Error on access for "+dev)
		return {}
	
	

def getAllScsiInfo():
	"""getAllScsiInfo() => dictionary

	retrive all information for scsi disks
	"""
	
	scsis = os.listdir(_scsibase)
	d = {}
	for x in scsis: 
		d.update(getScsiInfo(x))
	return d


def _test():
	global _debug
	def dbg(msg):
		print "DEBUG:",msg
	_debug = dbg

	d={}

	d.update(getAllMAC())
	d.update(getAllScsiInfo())

	for key in d.keys():
		print key," => ",d[key]


if __name__ == "__main__":
	_test()
	

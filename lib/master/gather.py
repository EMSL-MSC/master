#!/usr/bin/python
"""
A library of hardware gathering functions

FIXMES:
	dont hardcode paths, but put in a config?

"""

import os
from master import debug,dell
from master.util import *

verbs={}

def verb(verbname):
	def embedded(func):
		verbs[verbname]=func
		return func
	return embedded


def fileGrab(file):
	"""fileGrab(file) => list

	Return a list of all lines in given file
	"""
	f=open(file,"r")
	lines=f.readlines()
	f.close()
	return lines

#FIXME Do some sort of exception handling
def lineGrab(file):
	"""lineGrab(file) => string

	Grab the first line of a given file
	"""
	return fileGrab(file)[0].rstrip()

def getMAC(interface):
	"""getMAC(interface) => dictionary
	
	get the MAC address of a given network interface
	"""
	return {interface+'.mac':lineGrab("/sys/class/net/"+interface+"/address")}

@verb("mac")
def getAllMAC():
	"""getALLMAC() => dictionary
	Return 
	"""

	if not os.access("/sys/class/net/",os.F_OK):
		return {}
	ints = os.listdir("/sys/class/net/")

	d = {}
	for x in ints: 
		# dont scan loopback or ipv6 over ipv4 interface
		if not x in ("lo","sit0","br0","br1"):
			d.update(getMAC(x))
	return d

def _getSGdevice(scsi_id):
	"""_getSGdevice(scsi_id) => string
	device - chan:target:id:lun string from
	"""

	try:
		try:
			return _getSGdevice.sg_map[scsi_id]
		except AttributeError:
			_getSGdevice.sg_map={}
			if not os.access('/usr/bin/sg_map',os.X_OK):
				debug("failed to access sg_map or sg_inq " + str(e))
				return {}
			for line in os.popen("/usr/bin/sg_map -sd -x 2> /dev/null","r"):
				parts = line.split()
				if len(parts) == 7:
					(sg,c,t,i,l,type,dev)=parts
					key=":".join((c,t,i,l))
					_getSGdevice.sg_map[key]=dev
	except KeyError:
		return {}

def getScsiInfo(scsi_id):
	"""getScsiInfo(scsi_id) => dictionary

	scsi_id - chan:target:id:lun string from /sys/class/scsi_disk/
	Retrieve model number, serial number and firmware revision of a scsi device
	"""
	mymap = { 'Vendor identification':'vendor',
			  'Product identification':'model',
			  'Product revision level':'fwver',
			  'Unit serial number':'serial'
			  }

	smartmap = { 	'Device Model':'model',
				 	'Firmware Version':'fwver',
					'Serial Number':'serial'
				}

	if not os.access("/usr/bin/sg_inq",os.X_OK):
		debug("failed to access sg_map or sg_inq")
		return {}

	dev = _getSGdevice(scsi_id)
	if not dev:
		 debug("Failed to find a device for "+scsi_id+" MAP:"+`_getSGdevice.sg_map`)
		 return {}
	prefix="scsi."+scsi_id
	p = os.popen("/usr/bin/sg_inq "+dev,"r")
	infos = doLineParse(p,prefix,mymap)

	try:
		if infos[prefix+'.vendor']=='ATA' and os.access("/usr/sbin/smartctl",os.X_OK):
			p = os.popen("/usr/sbin/smartctl -i "+dev,"r")
			infos.update(doLineParse(p,prefix,smartmap))

		if "PERC" in infos[prefix+".model"]:
			infos.update(dell.getAllPERCInfo())

	except (IOError,KeyError):
		pass	#if info doesn't have a vendor key or if we don't have a smartctl command

	return infos

@verb("scsi")
def getAllScsiInfo():
	"""getAllScsiInfo() => dictionary

	retrive all information for scsi disks
	"""
	return _callOnDirList("/sys/class/scsi_device/",getScsiInfo)

#FIXME write a function signature
def _callOnDirList(dir,func):
	"""call a function on every file in a directory"""

	if not os.access(dir,os.F_OK):
		debug("failed to access "+dir)
		return {}
	entries = os.listdir(dir)
	d = {}
	for x in entries: 
		d.update(func(x))
	return d

_ibbase="/sys/class/infiniband/"
_ib="infiniband."
def getIBInfo(id):
	"""retrieve information about a specific IB card"""
	togather = [("fw_ver","fwver"),("node_guid","guid"),("hca_type","type")]
	d={}
	for (file,key) in togather:
		if os.access(_ibbase,os.R_OK): 
			d[_ib+id+"."+key] = lineGrab(_ibbase+"/"+id+"/"+file)
	return d

@verb("ib")
def getAllIBInfo():
	"""Gather all IB card info"""
	return _callOnDirList(_ibbase,getIBInfo)

@verb("system")
def getSystemInfo():
	"""getSystemInfo() -> dictionary
	
	Gather System information such as kernel version, processor info, etc..
	"""

	d={}

	d = dict(zip(('sysname', 'nodename', 'release', 'version', 'machine'),os.uname()))
	del(d['nodename'])
	
	d.update(doLineParse(open("/proc/meminfo","r"),"mem",{"MemTotal":"total","SwapTotal":"swap"}))

	return d

@verb("all")
def gatherALL():
	d={}
	for (v,f) in verbs.items():
		if v != "all":
			debug("Running :"+v+" Verb")
			d.update(f())
	return d

def _test():
	global debug,verbs
	def dbg(msg):
		print "DEBUG:",msg
	debug = dbg

	print verbs

	d=verbs["all"]()

	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]

if __name__ == "__main__":
	_test()
	

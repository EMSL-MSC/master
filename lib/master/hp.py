#!/usr/bin/python
"""A library to use hpacucli to gather properties from the HP/compaq cciss Smart Array Cards."""

import os
import master
import re
import time
import fcntl
import errno
import select
from master.util import *

_theproc=None
def getproc():
	global _theproc

	if not _theproc:
		if not os.access(master.config['hpacucli'],os.X_OK):
			return None
		_theproc = os.popen2(master.config['hpacucli'],"rw")
		fd=_theproc[1].fileno()
		fl = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, fl  | os.O_NONBLOCK)
		getlines(None,_theproc)
	return _theproc

def killproc():
	if _theproc:
		os.write(_theproc[0].fileno(),"exit\n")
		os.close(_theproc[0].fileno())
		os.close(_theproc[1].fileno())
	_thproc=None

def getlines(cmd,proc):
	"""send the cmd to proc, then read the output into a set of 'lines' that are returned"""

	if cmd:
		os.write(proc[0].fileno(),cmd+"\n")

	data=''
	l=1
	
	# wait for that prompt to appear
	while l:
		try:
			select.select([proc[1].fileno()],[],[],1.0)
			d=os.read(proc[1].fileno(),4096)
			l=len(d)
			data+=d
			if data.rfind("=>")>0:
				break
		except OSError, msg:
			if not msg.errno==errno.EAGAIN:
				print `msg`
				l=0

	lines=data.split("\n");
	#print lines
	return lines

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

	lines = getlines("ctrl slot="+slot+" show detail",getproc())
	info = doLineParse(lines,'smartarray.s'+slot,slotmap)

	lines =  getlines("ctrl slot="+slot+" physicaldrive all show",getproc())

	findit = re.compile(".*physicaldrive ([^ ]*) .*")
	for line in lines:
		found = findit.match(line)
		if found:
			id = found.groups()[0]
			lines = getlines("ctrl slot="+slot+"  physicaldrive "+id+" show",getproc())
			info.update(doLineParse(lines,'smartarray.s'+slot+'.'+id,drivemap))

	return info


def getAllSmartArrayInfo():
	info = {}

	lines = getlines("ctrl all show",getproc())

	findit = re.compile("Smart Array ([^ ]*) in Slot ([0-9]*).*")
	
	for line in lines:
		found = findit.match(line)
		if found:
			type,slot = found.groups()
			info['smartarray.s'+slot+'.type']=type
			info.update(getSmartArraySlotInfo(slot))

	killproc()
	return info

def _test():
	d=getAllSmartArrayInfo()
	keys = d.keys()
	keys.sort()
	for key in keys:
		print key," => ",d[key]


if __name__ == "__main__":
		_test()


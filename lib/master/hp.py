#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright © 2008,2009, Battelle Memorial Institute
# All rights reserved.
#
# 1.	Battelle Memorial Institute (hereinafter Battelle) hereby grants permission
# 	to any person or entity lawfully obtaining a copy of this software and
# 	associated documentation files (hereinafter “the Software”) to redistribute
# 	and use the Software in source and binary forms, with or without
# 	modification.  Such person or entity may use, copy, modify, merge, publish,
# 	distribute, sublicense, and/or sell copies of the Software, and may permit
# 	others to do so, subject to the following conditions:
#
# 	•	Redistributions of source code must retain the above copyright
# 		notice, this list of conditions and the following disclaimers.
# 	•	Redistributions in binary form must reproduce the above copyright
# 		notice, this list of conditions and the following disclaimer in the
# 		documentation and/or other materials provided with the distribution.
# 	•	Other than as used herein, neither the name Battelle Memorial
# 		Institute or Battelle may be used in any form whatsoever without the
# 		express written consent of Battelle.
# 	•	Redistributions of the software in any form, and publications based
# 		on work performed using the software should include the following
# 		citation as a reference:
#
# 			(A portion of) The research was performed using EMSL, a
# 			national scientific user facility sponsored by the
# 			Department of Energy's Office of Biological and
# 			Environmental Research and located at Pacific Northwest
# 			National Laboratory.
#
# 2.	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# 	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# 	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# 	ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY
# 	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# 	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# 	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# 	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# 	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# 	THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# 3.	The Software was produced by Battelle under Contract No. DE-AC05-76RL01830
# 	with the Department of Energy.  The U.S. Government is granted for itself
# 	and others acting on its behalf a nonexclusive, paid-up, irrevocable
# 	worldwide license in this data to reproduce, prepare derivative works,
# 	distribute copies to the public, perform publicly and display publicly, and
# 	to permit others to do so.  The specific term of the license can be
# 	identified by inquiry made to Battelle or DOE.  Neither the United States
# 	nor the United States Department of Energy, nor any of their employees,
# 	makes any warranty, express or implied, or assumes any legal liability or
# 	responsibility for the accuracy, completeness or usefulness of any data,
# 	apparatus, product or process disclosed, or represents that its use would
# 	not infringe privately owned rights.
#
"""A library to use hpacucli to gather properties from the HP/compaq cciss Smart Array Cards."""

import os
import master
import re
import time
import fcntl
import errno
import select
from master.util import *

_theproc = None


def getproc():
	global _theproc

	if not _theproc:
		if not os.access(master.config['hpacucli'], os.X_OK):
			return None
		_theproc = os.popen2(master.config['hpacucli'], "rw")
		fd = _theproc[1].fileno()
		fl = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
		getlines(None, _theproc)
	return _theproc


def killproc():
	if _theproc:
		os.write(_theproc[0].fileno(), "exit\n")
		os.close(_theproc[0].fileno())
		os.close(_theproc[1].fileno())
	_thproc = None


def getlines(cmd, proc):
	"""send the cmd to proc, then read the output into a set of 'lines' that are returned"""

	if cmd:
		os.write(proc[0].fileno(), cmd + "\n")

	data = ''
	l = 1

	# wait for that prompt to appear
	while l:
		try:
			select.select([proc[1].fileno()], [], [], 1.0)
			d = os.read(proc[1].fileno(), 4096)
			l = len(d)
			data += d
			if data.rfind("=>") > 0:
				break
		except OSError as msg:
			if not msg.errno == errno.EAGAIN:
				print(repr(msg))
				l = 0

	lines = data.split("\n")
	# print lines
	return lines


def getSmartArraySlotInfo(slot):
	slotmap = {
            'Firmware Version': 'fwver',
         			'Hardware Revision': 'hwrev',
         			'Serial Number': 'serial',
	}
	drivemap = {
            'Model': 'model',
         			'Size': 'capacity',
         			'Serial Number': 'serial',
         			'Firmware Revision': 'fwver',
	}

	lines = getlines("ctrl slot=" + slot + " show detail", getproc())
	info = doLineParse(lines, 'smartarray.s' + slot, slotmap)

	lines = getlines("ctrl slot=" + slot + " physicaldrive all show", getproc())

	findit = re.compile(".*physicaldrive ([^ ]*) .*")
	for line in lines:
		found = findit.match(line)
		if found:
			id = found.groups()[0]
			lines = getlines("ctrl slot=" + slot +
			                 "  physicaldrive " + id + " show", getproc())
			info.update(doLineParse(lines, 'smartarray.s' + slot + '.' + id, drivemap))

	return info


def getAllSmartArrayInfo():
	info = {}

	lines = getlines("ctrl all show", getproc())

	findit = re.compile("Smart Array ([^ ]*) in Slot ([0-9]*).*")

	for line in lines:
		found = findit.match(line)
		if found:
			type, slot = found.groups()
			info['smartarray.s' + slot + '.type'] = type
			info.update(getSmartArraySlotInfo(slot))

	killproc()
	return info


def _test():
	d = getAllSmartArrayInfo()
	keys = list(d.keys())
	keys.sort()
	for key in keys:
		print(key, " => ", d[key])


if __name__ == "__main__":
		_test()

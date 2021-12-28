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

	memmap = {}
	bank = ''
	found = {}

	if not os.access(master.config['decode_dimms'], os.X_OK):
		master.debug("Error finding:" + master.config['decode_dimms'])

		return {}

	p = os.popen(master.config['decode_dimms'], "r")

	for l in p.readlines():
		if 'bank' in l:
			bank = l.split().pop()

		found = foundMemInfo(l)

		if found:
			memmap["dimm." + bank + "."
                            + list(found.keys())[0]] = found[list(found.keys())[0]]
	p.close()

	if not memmap:
		master.debug(
			"Error: No dimm information found. * Requires 'eeprom' and 'i2c-i801' kernel modules *")

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
	d = getMemoryInfo()
	keys = list(d.keys())
	keys.sort()
	for key in keys:
		print(key, " => ", d[key])


if __name__ == "__main__":
	_test()

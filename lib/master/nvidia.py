#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Copyright © 2019, Battelle Memorial Institute
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
"""A library to use omreport to gather properties from NVidia GPU Cards."""

from . import ssv
import os
import re
from master.util import *
from master import debug


def getGPUInfo(id, uuid):
	"""getCGPUInfo(id,uuid) -> dictionary"""

	mapping = {"Driver Version": "driver.version", "Product Name": "name",
            "CUDA Version": "cuda.version",
            "Serial Number": "serial", "GPU UUID": "uuid",
            "VBIOS Version": "version", "GPU Part Number": "model"}
	info = {}

	if not os.access("/usr/bin/nvidia-smi", os.X_OK):
		return {}

	p = os.popen(f"/usr/bin/nvidia-smi -i {uuid} -q", "r")
	lines = p.readlines()
	p.close()

	info = doLineParse(lines, id, mapping)

	return info


def getAllGPUInfo():
	"""getAllGPUInfo() -> dictionary"""

	infos = {}

    # sample nvidia-smi -L
    # GPU 0: Tesla V100-PCIE-16GB (UUID: GPU-5d5f184f-88ca-3a1a-ebed-6417cd5a07ca)
    # GPU 1: Tesla V100-PCIE-16GB (UUID: GPU-e48e0338-3f4e-406b-591f-d36ce2aeb169)

	if not os.access("/usr/bin/nvidia-smi", os.X_OK):
		return {}

	p = os.popen("/usr/bin/nvidia-smi -L", "r")
	l = p.readlines()
	p.close()

	for d in l:
		grp = re.match("(GPU \d+):.*UUID: (GPU-[a-z0-9\-]+)", d)
		if grp:
			theid = grp.group(1).replace(" ", ".").lower()
			uuid = grp.group(2)
			debug(f"processing {theid} {uuid}")
			infos.update(getGPUInfo(theid, uuid))

	return infos


def _test():
	global debug

	def dbg(msg):
		print("DEBUG:", msg)
	debug = dbg

	d = getAllGPUInfo()
	for key in sorted(d.keys()):
		print(f"{key} => {d[key]}")


if __name__ == "__main__":
		_test()

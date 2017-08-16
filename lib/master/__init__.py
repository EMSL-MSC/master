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
# -*- coding: latin-1 -*-
"""

This file is part of the MASTER project, which is goverened by the following License

Copyright © 2007,2008,2009,2010 Battelle Memorial Institute
All rights reserved.

1.	Battelle Memorial Institute (hereinafter Battelle) hereby grants permission
	to any person or entity lawfully obtaining a copy of this software and
	associated documentation files (hereinafter “the Software”) to redistribute
	and use the Software in source and binary forms, with or without
	modification.  Such person or entity may use, copy, modify, merge, publish,
	distribute, sublicense, and/or sell copies of the Software, and may permit
	others to do so, subject to the following conditions:

	•	Redistributions of source code must retain the above copyright
		notice, this list of conditions and the following disclaimers.
	•	Redistributions in binary form must reproduce the above copyright
		notice, this list of conditions and the following disclaimer in the
		documentation and/or other materials provided with the distribution.
	•	Other than as used herein, neither the name Battelle Memorial
		Institute or Battelle may be used in any form whatsoever without the
		express written consent of Battelle.
	•	Redistributions of the software in any form, and publications based
		on work performed using the software should include the following
		citation as a reference:

			(A portion of) The research was performed using EMSL, a
			national scientific user facility sponsored by the
			Department of Energy's Office of Biological and
			Environmental Research and located at Pacific Northwest
			National Laboratory.

2.	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
	ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY
	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
	THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

3.	The Software was produced by Battelle under Contract No. DE-AC05-76RL01830
	with the Department of Energy.  The U.S. Government is granted for itself
	and others acting on its behalf a nonexclusive, paid-up, irrevocable
	worldwide license in this data to reproduce, prepare derivative works,
	distribute copies to the public, perform publicly and display publicly, and
	to permit others to do so.  The specific term of the license can be
	identified by inquiry made to Battelle or DOE.  Neither the United States
	nor the United States Department of Energy, nor any of their employees,
	makes any warranty, express or implied, or assumes any legal liability or
	responsibility for the accuracy, completeness or usefulness of any data,
	apparatus, product or process disclosed, or represents that its use would
	not infringe privately owned rights.

"""


def debug(msg):
	pass


def basicdebug(msg):
	print "DEBUG:" + msg


config = {
	"config_file": "/etc/mcp.conf",
    "privileged_conf": "/etc/mcp-priv.conf",
	"server_url": "http://master:627",
	"sark_modules": ("all",),
	"database_server": "",
	"database_name": "master",
	"database_user": "master",
	"database_password": "",
	"database_min_connections": 3,
	"database_max_connections": 5,
	"decode_dimms": "/usr/bin/decode-dimms",
	"hpacucli": "/usr/sbin/hpacucli",
	"mcp_port": 627,
	"mcp_host_authorization": True,
	"web_interface": False,
	"web_directory": "/usr/share/mcp/web",
	"mcp_pid_file": "/var/run/mcp.pid",
	"sma_server_username": "root",
	"sma_username": "Administrator",
	"micinfo": "/usr/bin/micinfo"
}


def load_config():
    load_config_file("config_file")


def load_privileged_config():
    load_config_file("privileged_conf")


def load_config_file(param):
    """Loads the configuration file defined in config[param]"""

    global config

    try:
		crap = {}
		exec open(config[param]) in crap, config
		for (k, v) in config.items():
			debug("Config: " + str(k) + " => " + str(v))
    except IOError:
		debug("Error Loading Config file: " + config["config_file"])

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: noet:ts=4:sw=4:
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

import xmlrpc.client
import pgdb
import time
import datetime

server_url = 'http://127.0.0.1:627'
server = xmlrpc.client.Server(server_url)


def wipeDatabase(user, database):
	conn = pgdb.connect(user=user, database=database)
	tables = ("node_properties_log", "node_status_log", "node_event_log",
           "node", "property", "status", "users", "event",)
	for tbl in tables:
		curs = conn.cursor()
		curs.execute("delete from " + tbl)
		curs.close()
		conn.commit()
	return True


def try_call(function, args, result):
	retval = None
	try:
		retval = function(*args)
	except xmlrpc.client.ProtocolError as inst:
		print(f"ProtocolError: - {inst}")
	except xmlrpc.client.ResponseError as inst:
		print(f"ResponseError: - {inst}")
	except xmlrpc.client.Fault as inst:
		print(f"Fault: - {inst}")
		retval = xmlrpc.client.Fault
	except Exception as inst:
		print(f"Unexpected error: {inst}")
		raise

	str = f"{function._Method__name}({args})"
	spcs = 100 - len(str)
	print(str, " " * spcs, end=' ')
	if retval == result:
		print(f"Success: {repr(retval)}")
	elif type(retval) == type({}) and type(result) == type({}):
		if list(result.keys()) == list(retval.keys()):
			print("Success")
		else:
			print("Dictionary Failure", result, retval)
	else:
		print(f"Error retval == {repr(retval)}")

	return retval


wipeDatabase("master", "master")
now = datetime.datetime.fromtimestamp(server.master.serverTime())
tendaysago = int(time.mktime((now - datetime.timedelta(10)).timetuple()))
tendaysfromnow = int(time.mktime((now + datetime.timedelta(10)).timetuple()))

try_call(server.master.addNode, ["n0"], True)
try_call(server.master.addStatus, ["bad", "Things are Bad"], True)
try_call(server.master.addProperty, [
         "LogicalThinking", "Something that happens to Evan once a day"], True)
try_call(server.master.addUser, ["AbooDaba", "Yoda"], True)
try_call(server.master.updateStatus, [
         ["n0"], "bad", "AbooDaba", "this job sucks", "10 years from now"], xmlrpc.client.Fault)
try_call(server.master.updateStatus, [
         ["n0"], "bad", "AbooDaba", "life is cruel for a tester"], True)
try_call(server.master.updateStatus, [["n0"], "bad", "AbooDaba"], True)
try_call(server.master.getNodeStatus, [["n0"]], {'n0': 0})
try_call(server.master.getNodeStatus, [["n0", "n1"]], {'n0': 0})
try_call(server.master.getNodeStatus, [["CRAP!", "Id0n73xC157"]], {})
try_call(server.master.getStatusHistory, [["n0", "n1"]], {'n0': 0})
time.sleep(2)
try_call(server.master.getStatusHistory, [
         ["n0"], False, "now", "infinity"], {})
try_call(server.master.getStatusHistory, [
         ["n0"], ["bad"], 1200000000, "now"], {'n0': 0})
try_call(server.master.getStatusHistory, [
         ["n0"], ["booboobear"], 1200000000, "-infinity"], {})
try_call(server.master.updateNodeProperty, [
         ["n0"], "LogicalThinking", "-1"], True)
try_call(server.master.updateNodeProperty, [
         ["n0"], "LogicalThinking", "-1", "<insert evil laugh here>", "-1"], xmlrpc.client.Fault)
try_call(server.master.getNodeProperties, [["n0", "n0"]], {'n0': 0})
try_call(server.master.getNodeProperties, [
         ["n0"], ["LogicalThinking"]], {'n0': 0})
try_call(server.master.getNodePropertyHistory, [["n0"]], {'n0': 1})
try_call(server.master.getNodePropertyHistory, [
         ["n0", "n0"], False, tendaysago, 'now'], {'n0': 1})
try_call(server.master.getNodePropertyHistory, [
         ["n0", "n1"], False, "now", tendaysfromnow], {})
try_call(server.master.getNodePropertyHistory, [
         ["n0", "n1"], ["n0"], "now", tendaysfromnow], {})
try_call(server.master.getNodePropertyHistory, [["n0", "n0"], ["n0"]], {})

try_call(server.master.addEvent, ["Stuff", "Does happen"], True)
try_call(server.master.addEvent, ["Strange", "Things do happen"], True)
try_call(server.master.getEvent, [], {'Stuff': 'Does happen',
                                      'Strange': 'Things do happen'})
try_call(server.master.getEvent, [['Stuff']],
         {'Stuff': 'Does happen'})
try_call(server.master.storeNodeEvent,
         [['n0'], 'Stuff', 'AbooDaba', 'Did happen'],
         True)
try_call(server.master.getNodeEventHistory,
         [['n0']], {'n0': 0})

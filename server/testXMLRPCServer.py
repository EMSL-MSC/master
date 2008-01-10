#!/usr/bin/python

import xmlrpclib
import errno
import exceptions

server_url = 'http://127.0.0.1:627';
server = xmlrpclib.Server(server_url);

def try_call(function, args):
	try:
		retval = function(*args)

	except xmlrpclib.ProtocolError, inst:
		print "ProtocolError: - %s" % inst
	except xmlrpclib.ResponseError, inst:
		print "ResponseError: - %s" % inst
	except xmlrpclib.Fault, inst:
		print "Fault: - %s" % inst
	except Exception, inst :
		print "Unexpected error: %s" % inst
		raise

	if retval:
		print "Success %s" % retval
	else:
		print "Error retval == None"

	return retval

try_call(server.master.addNode, ["n0"])
try_call(server.master.addStatus, ["n0", "description"])
try_call(server.master.addProperty, ["n0", "description"])
try_call(server.master.addUser, ["AbooDaba", "Yoda"])
try_call(server.master.updateStatus, ["n0", "bad", "AbooDaba","this job sucks","10 years from now"])
try_call(server.master.updateStatus, ["n0", "bad", "AbooDaba","life is cruel for a tester"])
try_call(server.master.updateStatus, ["n0", "bad", "AbooDaba"])
try_call(server.master.getCurrentStatus, [["n0"]])
try_call(server.master.getCurrentStatus, [["n0", "n1"]])
try_call(server.master.getCurrentStatus, [["n0", "Id0n73xC157"]])
try_call(server.master.getStatusHistory, [["n0", "n1"]])
try_call(server.master.getStatusHistory, [["n0"], False, "now", "infinity"])
try_call(server.master.getStatusHistory, [["n0"], ("n0"), "Wed Jan  9 15:41:52 PST 2008", "now"])
try_call(server.master.getStatusHistory, [["n0"], ("booboobear"), "Wed Jan  9 15:41:52 PST 2008", "-infinity"])
try_call(server.master.updateProperty, [["n0"], "LogicalThinking", "-1"])
try_call(server.master.updateProperty, [["n0"], "LogicalThinking", "-1", "<insert evil laugh here>", "-1"])
try_call(server.master.getCurrentProperties, [["n0", "n0"]])
try_call(server.master.getCurrentProperties, [["n0"], ["LogicalThinking"]])
try_call(server.master.getPropertyHistory, [["n0", "n0"], False, "10 days ago", "now"])
try_call(server.master.getPropertyHistory, [["n0", "n1"], False, "now", "10 days ago"])
try_call(server.master.getPropertyHistory, [["n0", "n1"], ["n0"], "now", "10 days ago"])
try_call(server.master.getPropertyHistory, [["n0", "n0"], ["n0"]])

#!/usr/bin/python

import xmlrpclib
import errno
import exceptions

server_url = 'http://127.0.0.1:8000';
server = xmlrpclib.Server(server_url);

def try_call(function, args):
	try:
		print function(*args)

	except xmlrpclib.ProtocolError, inst:
		print "ProtocolError: - %s" % inst
	except xmlrpclib.ResponseError, inst:
		print "ResponseError: - %s" % inst
	except xmlrpclib.Fault, inst:
		print "Fault: - %s" % inst
	except Exception, inst :
		print "Unexpected error: %s" % inst
		raise

try_call(server.master.addNode, ["n0"])
try_call(server.master.addStatus, ["n0", "description"])
try_call(server.master.addProperty, ["n0", "description"])
try_call(server.master.addUser, ["AbooDaba", "Yoda"])
try_call(server.master.updateStatus, ["n0", "bad", "AbooDaba","this job sucks","10 years from now"])
try_call(server.master.getCurrentStatus, ["n0"])
try_call(server.master.getStatusHistory, ["n0"])
try_call(server.master.updateProperty, ["n0", "LogicalThinking", "-1"])
try_call(server.master.getCurrentProperties, ["n0"])
try_call(server.master.getPropertyHistory, ["n0"])

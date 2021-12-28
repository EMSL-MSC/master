#!/usr/bin/python

import xmlrpc.client
import errno
import exceptions
import pgdb
import time
import datetime

server_url = 'http://127.0.0.1:627'
server = xmlrpc.client.Server(server_url)


def wipeDatabase(user, database):
	conn = pgdb.connect(user=user, database=database)
	for tbl in ("node_properties_log", "node_status_log", "node", "property", "status", "users"):
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
		print("ProtocolError: - %s" % inst)
	except xmlrpc.client.ResponseError as inst:
		print("ResponseError: - %s" % inst)
	except xmlrpc.client.Fault as inst:
		print("Fault: - %s" % inst)
		retval = xmlrpc.client.Fault
	except Exception as inst:
		print("Unexpected error: %s" % inst)
		raise

	str = "%s(%s)" % (function._Method__name, args)
	spcs = 100 - len(str)
	print(str, " " * spcs, end=' ')
	if retval == result:
		print("Success: %s" % repr(retval))
	elif type(retval) == type({}) and type(result) == type({}):
		if list(result.keys()) == list(retval.keys()):
			print("Success")
		else:
			print("Dictionary Failure", result, retval)
	else:
		print("Error retval == %s" % repr(retval))

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

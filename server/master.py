#!/usr/bin/python
"""
Below any parameter requiring a node, status, user, or property accepts a symbolic name such as 'eth0' or 'cu3cn34'
"""

import os
import sys
import socket
import pwd
import masterXMLRPCServer as mxs
import pgdb

debug = False

connection = None


@mxs.rpc
def addNode(name):
	"""addNode(name) -> Boolean

	Create a new node.
	Returns new nodes unique ID or None on Error"""
	curs = connection.cursor()
	try:
		curs.execute("insert into node (name) values (%(name)s)", {"name": name})
		connection.commit()
		curs.close()
		return True
	except pgdb.DatabaseError:
		connection.rollback()
		return False


@mxs.rpc
def getNodes(filter=False):
	"""getNodes(filter=False) -> ['name1','name2',...]

	Get a list of nodes
	filter - A filter on what names should be returned. uses standard sql wildcards (i.e. n% matches n10)
	"""
	retList = []
	curs = connection.cursor()
	try:
		curs.execute("select name from node" +
		             {True: " where name like %(filter)s", False: ""}[filter != False], {"filter": filter})
		connection.commit()
		retList = curs.fetchall()
		curs.close()
		return retList
	except pgdb.DatabaseError:
		connection.rollback()
		return False


@mxs.rpc
def addStatus(name, desc=None):
	"""addStatus(name,description) -> Boolean

	Create a new status type, with name and descripition.
	Returns new status ID or None on error"""
	curs = connection.cursor()
	try:
		curs.execute("insert into status (name, description) values (%(name)s, %(desc)s)", {
		             "name": name, "desc": desc})
		connection.commit()
		curs.close()
		return True
	except pgdb.DatabaseError:
		connection.rollback()
		raise


@mxs.rpc
def getStatus(names=False):
	"""getStatus(names=False) -> {'name':'Description',...}

	Get a list of statuses.
	names - a list of status names, if list is empty return all statuses
	"""
	curs = connection.cursor()
	try:
		curs.execute("select name, description from status" +
		             {True: " where name in %(names)s", False: ""}[names != False], {"names": names})
		connection.commit()
		retDict = dict(curs.fetchall())
		curs.close()
		return retDict
	except pgdb.DatabaseError:
		connection.rollback()
		return False


@mxs.rpc
def addProperty(name, desc):
	"""addProperty(name,description) -> Boolean

	Create a new property type, with name and descripition.
	Returns new status ID or None on Error"""
	curs = connection.cursor()
	try:
		curs.execute("insert into property (name, description) values (%(name)s, %(desc)s)", {
		             "name": name, "desc": desc})
		connection.commit()
		curs.close()
		return id
	except pgdb.DatabaseError:
		connection.rollback()
		raise


@mxs.rpc
def getProperties(names=False):
	"""getProperties(names=[]) -> {'name':'Description',...}

	Get a list of properties as a dictionary
	names - a list of property names, if list is empty return all properties
	"""
	curs = connection.cursor()
	try:
		curs.execute("select name, description from property" +
		             {True: " where name in %(names)s", False: ""}[names != False], {"names": names})
		connection.commit()
		retDict = dict(curs.fetchall())
		curs.close()
		return retDict
	except pgdb.DatabaseError:
		connection.rollback()
		return False


@mxs.rpc
def addUser(name, fullname):
	"""addUser(name,fullname) -> Boolean

	Add a user in the database.
	name - unique username, should match unix username such as 'efelix'
	fullname - Printable Name of the user such as 'Evan J. Felix'
	"""
	curs = connection.cursor()
	try:
		curs.execute("insert into users (username,name) values (%(name)s,%(fullname)s)", {
		             "name": name, "fullname": fullname})
		connection.commit()
		curs.close()
		return True
	except pgdb.DatabaseError:
		connection.rollback()
		return False

# FIXME I may need to get a static time when "now" is passed


@mxs.rpc
def getUsers(names=False):
	"""getUsers(names=[]) -> {'username':'fullname',...}

	Get a list of users.
	names - a list of usernames, if list is empty return all users
	"""
	curs = connection.cursor()
	try:
		curs.execute("select username, name from users" +
		             {True: " where username in %(names)s", False: ""}[names != False], {"names": names})
		connection.commit()
		retDict = dict(curs.fetchall())
		curs.close()
		return retDict
	except pgdb.DatabaseError:
		connection.rollback()
		return False


@mxs.rpc
def updateStatus(nodes, status, user, comment="", time="now"):
	"""updateStatus(nodes,status,user,comment,time) -> Boolean

	Change the status of a list of nodes.
	Comments and time stamp are optional
	Returns True on success
	Returns timestamp of change, or None on error"""
	retVal = []
	curs = connection.cursor()
	try:
		curs.executemany("insert into node_status_log (node_id, status_id, time, comment, user_id) values ((select id from node where name = %(node)s), (select id from status where name = %(status)s), %(time)s, %(comment)s, (select id from users where username = %(user)s))", [
		                 {"node": i, "status": status, "time": time, "comment": comment, "user": user} for i in nodes])
		connection.commit()
		curs.close()
		return True
	except pgdb.DatabaseError:
		connection.rollback()
		raise

# TODO add user field


@mxs.rpc
def getCurrentStatus(nodes):
	"""getCurrentStatus(nodes) -> {'node1':(statusName,timeStamp,user,comment),...}

	Retrieve the current status of a node or set of nodes
	The nodes parameter is a list of nodes to get status for
	"""
	retDict = {}
	curs = connection.cursor()
	try:
		# should I use subqueries for these views?
		curs.execute("select node.name, status.name, last_change, users.username, comment from node_status, node, status, users where node_status.node_id = node.id and node_status.status_id = status.id and users.id = user_id and node.name in %(nodes)s", {
		             "nodes": nodes})
		for i in curs.fetchall():
			retDict[i[0]] = i[1:]
		return retDict
	except pgdb.DatabaseError as e:
		connection.rollback()
		raise


@mxs.rpc
def getStatusHistory(nodes, filter=False, startTime='-infinity', endTime='infinity'):
	"""getStatusHistory(nodes,filter=false,startTime=-infinity,endTime=inifinity) -> {'node1':[(statusName,timestamp,user,comment),...],'node2':...}

	Retrieve a ordered list of status changes in a time period for a list of nodes

	filter - set of status id's or status names that are allowed to be returned
	*Time - Date & Time for start and end of data requested
	"""
	retDict = {}
	curs = connection.cursor()
	try:
		sql = ("""select node.name, s.name, time, users.username, comment
				from node_status_log, node, status s, users
				where node.id = node_id and s.id = status_id and users.id = user_id
				and node.name in %(nodes)s and time between %(start)s and %(end)s """ +
                    {True: "", False: "and s.name in %(status)s "}[filter == False] +
                    "order by time")
		curs.execute(sql, {"nodes": nodes, "status": filter,
                     "start": startTime, "end": endTime})
		for i in curs.fetchall():
			try:
				retDict[i[0]] += [i[1:]]
			except KeyError:
				retDict[i[0]] = [i[1:]]
		return retDict
	except pgdb.DatabaseError as e:
		connection.rollback()
		raise


@mxs.rpc
def updateProperty(node, property, propertyValue, comment="", time="now"):
	"""updateProperty(node,property,propertyValue,comment="",time="now") -> timestamp

	Update a property value of a list of nodes.
		nodes		- node to set the property on
		property	- Property to change, name
		propertyValue	- value to change property to.
		comment		- user comment on this change
		time		- a timestamp for the change.  Defaults to 'now'

		Returns timestamp of change, or None on error"""
	retVal = []
	curs = connection.cursor()
	try:
		curs.execute("insert into node_properties_log (node_id, property_id, time, value, comment) values ((select id from node where name = %(node)s), (select id from property where name = %(property)s), %(time)s, %(propertyValue)s, %(comment)s)", {
		             "node": node, "property": property, "time": time, "propertyValue": propertyValue, "comment": comment})
		connection.commit()
		curs.close()
		return True
	except pgdb.DatabaseError:
		connection.rollback()
		raise


@mxs.rpc
def getCurrentProperties(nodes, filter=False):
	"""getCurrentProperties(nodes,filter=False) -> {'node1':[(propName,value,timestamp,comment),...],'node2':[...],...}

	Retrieve the current properties of the given nodes.
	a filter is a list of id's allowed ("eth0mac","eth1mac")
	Returns a dictionary of tuples containing (propName,value,timestamp,comment)
	"""

	retVal = {}
	curs = connection.cursor()
	if type(filter) == type(""):
		filter = [filter]
	try:
		curs.execute("""select node.name, property_id, property.name, value, last_change, comment
				from node_properties, node, property
				where node_properties.node_id = node.id and node_properties.property_id = property.id
				and node.name in %(nodes)s """ +
                    {True: "", False: "and property.name in %(filter)s"}[filter != False] +
                    "order by last_change",
                    {"nodes": nodes, "filter": filter})
		for i in curs.fetchall():
			try:
				retVal[i[0]].append(i[1:])
			except KeyError:
				retVal[i[0]] = [i[1:]]
		return retVal
	except pgdb.DatabaseError as e:
		connection.rollback()
		raise


@mxs.rpc
def getPropertyHistory(nodes, filter=False, startTime='-infinity', endTime='infinity'):
	"""getPropertyHistory(nodes,filter=False,startTime='-infinity',endTime='infinity') -> {'node1':[(propName,value,timestamp,comment),...],'node2':[...],...}

	Retrieve all property change logs for a given period.
	If a time period is not specified returns all records.
	a filter is a list of id's allowed (1,2,3,"eth0mac")
	Returns a dictionary list of tuples containing (propName,value,timestamp,comment)
	"""
	retDict = {}
	curs = connection.cursor()
	try:
		curs.execute("""select node.name, property_id, p.name, last_change, comment
				from node_properties, node, property p where node.id = node_id and p.id = property_id
				and node.name in %(nodes)s and last_change between %(start)s and %(end)s """ +
                    {True: "", False: "and p.name in %(filter)s "}[filter == False] +
                    "order by last_change",
                    {"nodes": nodes, "filter": filter, "start": startTime, "end": endTime})
		for i in curs.fetchall():
			try:
				retDict[i[0]] += [i[1:]]
			except KeyError:
				retDict[i[0]] = [i[1:]]
		return retDict
		connection.commit()
		curs.close()
		return retDict
	except pgdb.DatabaseError:
		connection.rollback()
		raise


def authConnection(rh):
	"Always allow localhost, only authenticate clients which are already inserted in the db"

	if rh.client_address[0] == "127.0.0.1":
		return 1
	else:
		client = socket.gethostbyaddr(rh.client_address[0])
		client_name = client[0].split(".")[0]
		if socket.gethostbyname(client_name) not in client[2]:
			return 0
		curs = connection.cursor()
		curs.execute("select * from node where name = %(client_name)s",
		             {"client_name": client_name})
		return curs.rowcount


def daemonize(user=None, group=None):
	pid = os.fork()
	if pid > 0:
		sys.exit(0)

	os.chdir("/")
	os.setsid()
	os.umask(0)

	pid = os.fork()
	if pid > 0:
		sys.exit(0)

	sys.stdout.close()
	sys.stderr.close()
	os.close(0)
	os.close(1)
	os.close(2)

	if user:
		os.seteuid(pwd.getpwnam(user)[2])
	if group:
		os.setegid(group)


def main():
	"""Function to start up the server and serve the pages till the end of time."""
	global connection

	if not debug:
		daemonize()

	connection = pgdb.connect(user="master", database="master")
	srv = mxs.MasterXMLRPCServer(("", 627), authConnection)
	while True:
		try:
			srv.serve_forever()
		except pgdb.OperationalError:
			connection = pgdb.connect(user="root", database="master")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass

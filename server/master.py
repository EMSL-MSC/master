#!/usr/bin/python
"""
Below any parameter requiring a node, status, user, or property accepts a symbolic name such as 'eth0' or 'cu3cn34'
"""

import masterXMLRPCServer as mxs

@mxs.rpc
def addNode(name):
	"""addNode(name) -> id
	
	Create a new node. 
	Returns new nodes unique ID or None on Error"""
	return False

@mxs.rpc
def addStatus(name,description):
	"""addStatus(name,description) -> id
	
	Create a new status type, with name and descripition.  
	Returns new status ID or None on error"""
	return False

@mxs.rpc
def addProperty(name,description):
	"""addProperty(name,description) -> id
	
	Create a new property type, with name and descripition.  
	Returns new status ID or None on Error"""
	return False

@mxs.rpc
def addUser(name,fullname):
    """addUser(name,fullname) -> id

    Add a user in the database.
    name - unique username, should match unix username such as 'efelix'
    fullname - Printable Name of the user such as 'Evan J. Felix'
    """
    return False

@mxs.rpc
def updateStatus(nodes,status,user,comment="",time="now"):
	"""updateStatus(nodes,status,user,comment,time) -> Boolean
	
	Change the status of a list of nodes.  
	Comments and time stamp are optional
	Returns True on success
    """
	return False

@mxs.rpc
def getCurrentStatus(nodes):
	"""getCurrentStatus(nodes) -> {'node1':(nodeName,statusName,timeStamp,user,comment),...}
	
	Retrieve the current status of a node or set of nodes
	The nodes parameter is a list of nodes to get status for
	"""
	return False

@mxs.rpc
def getStatusHistory(nodes,filter=False,startTime='-infinity',endTime='inifinity'):
	"""getStatusHistory(nodes,filter=false,startTime=-infinity,endTime=inifinity) -> {'node1':[(statusName,timestamp,user,comment),...],'node2':...}

	Retrieve a ordered list of status changes in a time period for a list of nodes

	filter - set of status id's or status names that are allowed to be returned
    *Time - Date & Time for start and end of data requested
	"""
	return False

@mxs.rpc
def updateProperty(node,property,propertyValue,comment="",time="now"):
	"""updateProperty(node,property,propertyValue,comment="",time="now") -> timestamp
	
	Update a property value of a node.
		nodes		 - List of nodes to set the property on
		property	  - Property to change, id or name
		propertyValue - value to change property to.
		comment	   - user comment on this change
		time		  - a timestamp for the change.  Defaults to 'now'
	
	Returns timestamp of change, or None on error"""
	return False

@mxs.rpc
def getCurrentProperties(nodes,filter=False):
	"""getCurrentProperties(nodes,filter=False) -> {'node1':[(propName,value,timestamp,comment),...],'node2':[...],...}
	
	Retrieve the current properties of the given node.
	a filter is a list of id's allowed ("eth0mac","eth1mac")
	Returns a dictionary of tuples containing (propName,value,timestamp,comment)

	"""
	return False

@mxs.rpc
def getPropertyHistory(nodes,filter=False,startTime='-infinity',endTime='inifinity'):
	"""getPropertyHistory(nodes,filter=False,startTime='-infinity',endTime='inifinity') -> {'node1':[(propName,value,timestamp,comment),...],'node2':[...],...}
	
	Retrieve all property change logs for a given period.
	If a time period is not specified returns all records.
	a filter is a list of id's allowed (1,2,3,"eth0mac")
	Returns a dictionary list of tuples containing (propName,value,timestamp,comment)
	"""
	return False

def authConnection(rh):
	return rh.client_address[0] == "127.0.0.1"

def main():
	"""Function to start up the server and serve the pages till the end of time."""
	srv = mxs.MasterXMLRPCServer(("127.0.0.1",627), authConnection)
	srv.serve_forever()

if __name__ == "__main__":
	main()



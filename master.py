#!/usr/bin/python
"""
Below any parameter requiring a node, status, or property will accept a UniqueID or the symbolic name such as 'eth0' or 'cu3cn34'
"""

def addNode(name):
    """addNode(name) -> name
    
    Create a new node. 
    Returns new nodes unique ID or None on Error"""

def addStatus(name,description):
    """addStatus(name,description) -> id
    
    Create a new status type, with name and descripition.  
    Returns new status ID or None on error"""

def addProperty(name,description):
    """addProperty(name,description) -> id
    
    Create a new property type, with name and descripition.  
    Returns new status ID or None on Error"""

def updateStatus(node,status,comment="",time="now"):
    """updateStatus(node,status,comment,time) -> id
    
    Change the status of a node.  
    Comments and time stamp are optional
    Returns timestamp of change, or None on error"""

def getCurrentStatus(nodes):
    """getCurrentStatus(nodes) -> [(nodeID,nodeName,statusID,statusName,timeStamp,comment),...]
    
    Retrieve the current status of a node or set of nodes
    If there is a single node return info only for that node.
    If the nodes parameter is a list, return data for every node in the list
    """

def getStatusHistory(node,startTime=None,endTime=None):
    """getStatusHistory(node,startTime=None,endTime=None) -> [(statusID,statusName,timestamp,comment),...]

    Retrieve a list of status changes in a time period
    """

def updateProperty(node,property,propertyValue,comment="",time="now"):
    """updateProperty(node,property,propertyValue,comment="",time="now") -> timestamp
    
    Update a property value of a node.
    property value is required.
    Returns timestamp of change, or None on error"""

def getCurrentProperties(node,filter=None):
    """getCurrentProperties(node,filter=None) -> [(propID,propName,value,timestamp,comment),...]
    
    Retrieve the current properties of the given node.
    a filter is a list of id's allowed (1,2,3,"eth0mac")
    Returns a list of tuples containing (propID,propName,value,timestamp,comment)

    FIXME: should this take alist of nodes???
    """

def getPropertyHistory(node,filter=None,startTime=None,endTime=None):
    """getPropertyHistory(node,filter=None,startTime=None,endTime=None) -> [(propID,propName,value,timestamp,comment),...]
    
    Retrieve all property change logs for a given period.
    If a time period is not specified returns all records.
    a filter is a list of id's allowed (1,2,3,"eth0mac")
    Returns a list of tuples containing (propID,propName,value,timestamp,comment)
    """


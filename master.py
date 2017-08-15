#!/usr/bin/python
"""
Below any parameter requiring a node, status, or property will accept a UniqueID or the symbolic name such as 'eth0' or 'cu3cn34'
"""


def addNode(name):
    """addNode(name) -> name

    Create a new node.
    Returns new nodes unique ID or None on Error"""


def addStatus(name, description):
    """addStatus(name,description) -> id

    Create a new status type, with name and descripition.
    Returns new status ID or None on error"""


def addProperty(name, description):
    """addProperty(name,description) -> id

    Create a new property type, with name and descripition.
    Returns new status ID or None on Error"""


def updateStatus(nodes, status, comment="", time="now"):
    """updateStatus(nodes,status,comment,time) -> [id,...]

    Change the status of a list of nodes.
    Comments and time stamp are optional
    Returns timestamp of change, or None on error"""


def getCurrentStatus(nodes):
    """getCurrentStatus(nodes) -> [(nodeID,nodeName,statusID,statusName,timeStamp,comment),...]

    Retrieve the current status of a node or set of nodes
    The nodes parameter is a list of nodes to get status for
    """


def getStatusHistory(nodes, filter=None, startTime=None, endTime=None):
    """getStatusHistory(nodes,filter=None,startTime=None,endTime=None) -> {'node1':[(statusID,statusName,timestamp,comment),...],'node2':...}

    Retrieve a list of status changes in a time period for a list of nodes

    filter - set of status id's or status names that are allowed to be returned
    """


def updateProperty(node, property, propertyValue, comment="", time="now"):
    """updateProperty(node,property,propertyValue,comment="",time="now") -> timestamp

    Update a property value of a node.
        nodes         - List of nodes to set the property on
        property      - Property to change, id or name
        propertyValue - value to change property to.
        comment       - user comment on this change
        time          - a timestamp for the change.  Defaults to 'now'

    Returns timestamp of change, or None on error"""


def getCurrentProperties(nodes, filter=None):
    """getCurrentProperties(nodes,filter=None) -> {'node':[(propID,propName,value,timestamp,comment),...],'node2':[...],...}

    Retrieve the current properties of the given node.
    a filter is a list of id's allowed (1,2,3,"eth0mac")
    Returns a list of tuples containing (propID,propName,value,timestamp,comment)

    """


def getPropertyHistory(nodes, filter=None, startTime=None, endTime=None):
    """getPropertyHistory(nodes,filter=None,startTime=None,endTime=None) -> {'nodeid1':[(propID,propName,value,timestamp,comment),...],'nodeid2':[...],...}

    Retrieve all property change logs for a given period.
    If a time period is not specified returns all records.
    a filter is a list of id's allowed (1,2,3,"eth0mac")
    Returns a list of tuples containing (propID,propName,value,timestamp,comment)
    """

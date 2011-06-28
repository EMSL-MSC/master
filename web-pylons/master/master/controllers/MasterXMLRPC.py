import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort

from pylons.controllers import XMLRPCController
from master.lib.base import *

from master.model import meta
import master.model as model

import datetime

log = logging.getLogger(__name__)

class MasterxmlrpcController(XMLRPCController):

    def addNode(self, name):
        """addNode(name) -> Boolean

        Create a new node.
        Returns True on success, False on Failure.
        """
        meta.Session.add(model.Node(name))
        meta.Session.commit()
        return True
    addNode.signature = [ ['bool', 'string'] ]

    def getNodes(self, filter=False):
        """getNodes(filter=False) -> ['node1','node2',...,'nodeN']

        Get a list of nodes.
        filter - A filter on what names should be returned. uses standard sql wildcards (i.e. n% matches n10)
        """
        node_q = meta.Session.query(model.Node.name)
        if filter:
            node_q = node_q.filter(model.Node.name.like(filter))
        return [node.name for node in node_q]
    getNodes.signature = [["array"], ["array", "string"]]

    def addStatus(self, name, desc = ''):
        """addStatus(name,desc = '') -> Boolean

        Create a new status type, with name and descripition.
        Returns True or xmlrpclib.Fault on error
        """
        meta.Session.add(model.Status(name, desc))
        meta.Session.commit()
        return True
    addStatus.signature = [["bool", "string"], ["bool", "string", "string"]]


    def getStatus(self, names=False):
        """getStatus(names=False) -> {'name':'Description',...}

        Get a list of statuses.
        names - a list of status names, if list is empty return all statuses
        """
        status_q = meta.Session.query(model.Status)
        if names:
            status_q = status_q.filter(model.Status.name.in_(names))
        return dict([(status.name, status.description) for status in
                     status_q])
    getStatus.signature = [["struct"],["struct", "array"]]

    def addEvent(self, name, description=''):
        """addEvent(name, description = '') -> Boolean

        Creates a new event, with name and description.
        Returns True or xmlrpclib.Fault on error.
        """
        meta.Session.add(model.Event(name, description))
        meta.Session.commit()
        return True
    addEvent.signature = [["bool", "string"],
                                ["bool", "string", "string"]]

    def getEvent(self, names=False):
        """getEvent(names=False) -> {'name': 'Description',...}

        Get a list of events.
        names - a list of event names, if list is empty return all events
        """
        event_q = meta.Session.query(model.Event)
        if names:
            event_q = event_q.filter(model.Event.name.in_(names))
        return dict([(event.name, event.description) for event in
                     event_q])
    getEvent.signature = [["struct"], ["struct", "array"]]

    def addProperty(self, name, desc = ''):
        """addProperty(name,desc = '') -> Boolean

        Create a new property type, with name and descripition.
        Returns True or xmlrpclib.Fault on Error
        """
        meta.Session.add(model.Property(name, desc))
        meta.Session.commit()
        return True
    addProperty.signature = [["bool", "string"], ["bool", "string", "string"]]

    def getProperties(self, names=False):
        """getProperties(names=[]) -> {'name':'Description',...}

        Get a list of properties as a dictionary
        names - a list of property names, if list is empty return all properties
        """
        property_q = meta.Session.query(model.Property)
        if names:
            property_q = property_q.filter(model.Property.name.in_(names))
        return dict([(property.name, property.description) for property in
                     property_q])
    getProperties.signature = [["struct"], ["struct", "array"]]

    def addUser(self, name,fullname):
        """addUser(name,fullname) -> Boolean

        Add a user in the database.
        name - unique username, should match unix username such as 'efelix'
        fullname - Printable Name of the user such as 'Evan J. Felix'
        """
        meta.Session.add(model.Users(name, fullname))
        meta.Session.commit()
        return True
    addUser.signature = [["bool", "string", "string"]]

    def getUsers(self, names=False):
        """getUsers(names=[]) -> {'username':'fullname',...}

        Get a list of users.
        names - a list of usernames, if list is empty return all users
        """
        user_q = meta.Session.query(model.Users)
        if names:
            user_q = user_q.filter(model.Users.username.in_(names))
        return dict([(user.username, user.name) for user in user_q])
    getUsers.signature = [["struct"], ["struct", "array"]]

    def updateStatus(self, nodes, status, user, comment="", time=""):
        """updateStatus(nodes,status,user,comment,timeistamp) -> Boolean

        Change the status of a list of nodes.
        Comments and timestamp are optional
        Returns True on success, xmlrpclib.Fault on Error
        """
        node_q = meta.Session.query(
                model.Node).filter(model.Node.name.in_(nodes))
        user_q = meta.Session.query(
                    model.Users).filter(model.Users.username == user)[0]
        status_q = meta.Session.query(
                    model.Status).filter(model.Status.name == status)[0]
        if time:
            the_time = datetime.datetime.fromtimestamp(time)
        else:
            the_time = datetime.datetime.now()

        for node in node_q:
            node_status_log = model.NodeStatusLog(node=node, status=status_q,
                                                 comment=comment, user=user_q,
                                                 time=the_time)
            meta.Session.add(node_status_log)

        meta.Session.commit()
        return True
    updateStatus.signature = [
        ["bool", "array", "string", "string"],
        ["bool", "array", "string", "string", "string"],
        ["bool", "array", "string", "string", "string", "dateTime.iso8601"]]

    def getNodeStatus(self, nodes):
        """getCurrentStatus(nodes) -> {'node1':(statusName,timeStamp,user,comment),...}

        Retrieve the current status of a node or set of nodes
        The nodes parameter is a list of nodes to get status for
        Timestamps are a POSIX timestamp
        """
        node_q = meta.Session.query(model.NodeStatus).join(model.Node)

        if nodes:
            node_q = node_q.filter(model.Node.name.in_(nodes))

        retval = {}
        for status in node_q:
            retval[status.node.name] = (
                status.status.name,
                time.mktime(status.last_change.timetuple()),
                status.user.name,
                status.comment
            )
        return retval
    getNodeStatus.signature = [
            ["struct"],
            ["struct", "array"],
    ]

    def getStatusHistory(self, nodes, filter=False, startTime='',
                         endTime=''):
        """getStatusHistory(nodes,filter=false,startTime=-infinity,endTime=inifinity) -> {'node1':[(statusName,timestamp,user,comment),...],'node2':...}

        Retrieve a ordered list of status changes in a time period for a list of nodes
        Nodes that are not in the system will be silently ignored.

        filter - set of status names that are allowed to be returned
        *Time - Date & Time for start and end of data requested.

        Timestamp values are the strings 'now','-infinity', 'infinity' or a integer representing a POSIX timestamp
        """
        node_status_log_q = meta.Session.query(
                                model.NodeStatusLog
                            ).join(
                                model.Node
                            ).join(
                                model.Users
                            ).join(
                                model.Status
                            ).filter(
                                model.Node.name.in_(nodes)
                            )
        if startTime:
            node_status_log_q = node_status_log_q.filter(
                model.NodeStatusLog.time >=
                datetime.datetime.fromtimestamp(startTime))
        if endTime:
            node_status_log_q = node_status_log_q.filter(
                model.NodeStatusLog.time <=
                datetime.datetime.fromtimestamp(endTime))

        if filter:
            node_status_log_q = node_status_log_q.filter(
                model.Status.name == filter)
        retval = {}
        for status_log in node_status_log_q:
            retval.setdefault(status_log.node.name,[]).append(
                (status_log.status.name,
                 time.mktime(status_log.time.timetuple()),
                 status_log.user.username, status_log.comment)
            )
        return retval
    getStatusHistory.signature = [
                    ["struct", "array"],
                    ["struct", "array", "bool"],
                    ["struct", "array", "string"],
                    ["struct", "array", "bool", "int"],
                    ["struct", "array", "string", "int"],
                    ["struct", "array", "bool", "int", "int"],
                    ["struct", "array", "string", "int", "int"]]


    def storeNodeEvent(self, nodes, event, user, comment="", time=""):
        """storeNodeEvent(nodes, event, user, comment, time) -> Boolean

        Creates an event log entry for a list of nodes.
        Comment and timestamp are optional.
        Returns True on success, xmlrpclib.Fault on error.
        """
        event = meta.Session.query(model.Event.name == event).first()
        user = meta.Session.query(model.Users.username == user).first()

        nodes_q = meta.Session.query(model.Node.name.in_(nodes))
        for node in nodes_q:
            event = model.NodeEventLog(node, event, comment, user)
            if time:
                event.time = datetime.datetime.fromtimestamp(time)
            meta.Session.add(event)
        meta.Session.commit()
    storeNodeEvent.signature = [
        ["bool", "array", "string", "string"],
        ["bool", "array", "string", "string", "string"],
        ["bool", "array", "string", "string", "string", "dateTime.iso8601"]]

    def getNodeEventHistory(self, nodes, status=False,
                                startTime='', endTime=''):
        """getNodeEventHistory(nodes, filter=False, startTime='-infinity', endTime='infinity') -> {'node1': [('eventName,timestamp,comment),...],'node2':...}

        Retrieve an ordered list of node events in a given time period for a
        list of nodes.

        Nodes that are not in the system will be silently ignored.

        filter - set of events that are to be returned.
        *Time - Datem & Time for start and end of requested data.

        Timestamp values are the strings 'now', '-infinity', 'infinity' or an
        integer representing a POSIX timestamp.
        """
        history_q = meta.Session.query(model.NodeEventLog
                                ).join(
                                    model.Node,
                                ).join(
                                    model.Event,
                                ).join(
                                    model.Users
                                ).filter(
                                    model.Node.name.in_(nodes)
                                )
        if status:
            history_q = history_q.filter(model.Event.name == status)
        if startTime:
            history_q = history_q.filter(
                model.NodeEventLog.time >=
                datetime.datetime.fromtimestamp(startTime))
        if endTime:
            history_q = history_q.filter(
                model.NodeEventLog.time <=
                datetime.datetime.fromtimestamp(endTime))
        retval = {}
        for event_log in history_q:
            retval.setdefault(event_log.node.name, []).append(
                (event_log.event.name,
                 time.mktime(event_log.time.timetuple()),
                 event_log.comment))
        return retval
    getNodeEventHistory.signature = [
                    ["struct", "array"],
                    ["struct", "array", "string"],
                    ["struct", "array", "string", "int"],
                    ["struct", "array", "string", "int", "int"]]

    def updateNodeProperty(self, node,property,propertyValue,comment="",time=""):
        """updateProperty(node,property,propertyValue,comment="",time="now") -> timestamp

        Update a property value of a list of nodes.
            node        - node to set the property on
            property    - Property to change, name
            propertyValue    - value to change property to.
            comment        - user comment on this change
            time        - a timestamp for the change.  Defaults to 'now'

        Returns timestamp of change, or xmlrpclib.Fault on error

        Timestamp values are the strings 'now','-infinity', 'infinity' or a integer representing a POSIX timestamp
        """
        node = meta.Session.query(model.Node.name == node).first()
        property = meta.Session.query(model.Property.name == property).first()
        entry = model.NodePropertyLog(node, property, comment, value)
        if time:
            entry.time = datetime.datetime.fromtimestamp(time)
        meta.Session.add(entry)
        meta.Session.commit()
    updateNodeProperty.signature = [
        ["dateTime.iso8601", "string", "string", "string"],
        ["dateTime.iso8601", "string", "string", "string", "string"],
        ["dateTime.iso8601", "string", "string", "string", "string", "dateTime.iso8601"]
    ]

    def getNodeProperties(self, nodes, filter=False):
        """getNodeProperties(nodes,filter=False) -> {'node1':[(propName,value,timestamp,comment),...],'node2':[...],...}

        Retrieve the current properties of the given nodes.
        a filter is a list of id's allowed ("eth0mac","eth1mac")
        Returns a dictionary of tuples containing (propName,value,timestamp,comment)
        Timestamps are a POSIX timestamp
        """
        property_q = meta.Session.query(model.NodeProperties
                                       ).join(
                                           model.Node
                                       ).join(
                                           model.Property
                                       ).filter(
                                           model.Node.name.in_(nodes)
                                       )
        if filter:
            if type(filter) == list:
                property_q = property_q.filter(
                    model.Property.name.in_(filter))
            else:
                property_q = property_q.filter(
                    model.Property.name == filter)
        retval = {}
        for event in property_q:
            retval.setdefault(event.node.name, []).append(
                (event.property.name,
                 event.value,
                 time.mktime(event.last_change.timetuple()),
                 event.comment))
        return retval

    getNodeProperties.signature = [
            ["struct", "array"],
            ["struct", "array", "string"],
            ["struct", "array", "array"]]

    def getNodePropertyHistory(self, nodes, filter=False,
                               startTime='', endTime=''):
        """getNodePropertyHistory(nodes,filter=False,startTime='-infinity',endTime='infinity') -> {'node1':[(propName,value,timestamp,comment),...],'node2':[...],...}

        Retrieve all property change logs for a given period.
        If a time period is not specified returns all records.

        filter is a list of property names allowed ("eth0mac","eth1mac")
        *Time - Date & Time for start and end of data requested
        Timestamp values are the strings 'now','-infinity', 'infinity' or a integer representing a POSIX timestamp
        """
        history_q = meta.Session.query(model.NodePropertyLog
                                        ).join(
                                          model.Node
                                        ).join(
                                            model.Property
                                        ).filter(
                                            model.Node.name.in_(nodes)
                                        )
        if filter:
            history_q = history_q.filter(model.Property.name.in_(filter))
        if startTime:
            history_q = history_q.filter(
                model.NodePropertyLog.time >=
                datetime.datetime.fromtimestamp(startTime))
        if endTime:
            history_q = history_q.filter(
                model.NodePropertyLog.time <=
                datetime.datetime.fromtimestamp(endTime))
        retval = {}
        for event in history_q:
            retval.setdefault(event.node.name, []).append(
                (event.property.name,
                 event.value,
                 time.mktime(event.time.timetuple()),
                 event.comment))
        return retval
    getNodePropertyHistory.signature = [
        ["struct", "array"],
        ["struct", "array", "array"],
        ["struct", "array", "array", "int"],
        ["struct", "array", "array", "int", "int"]]


    def getNodesFilter(self,filt):
        """getNodesFilter(filt) -> list

        The following keyword arguments take a string or list of strings

        status
        statuslike
        property
        propertylike
        propvalue
        propvaluelike
        node
        nodelike
        user
        userlike

        These arguments take a time value the is a string value such as 'now','-infinity', 'infinity' or a integer representing a POSIX timestamp
        startTime
        endTime

        Examples:
                getNodesFilter(nodelike="cut",status="ok")
                getNodesFilter(nodelike=("cut","director"),status="dead")
        """
        node_q = meta.Session.query(model.Node)
        if any([test in filt for test in
                ['status', 'statuslike', 'user', 'userlike']]):
            node_q = node_q.join(model.NodeStatusLog
                                ).join(model.Status
                                ).join(model.Users)
        if any([test in filt for test in
                ['property', 'propertylike', 'propvalue', 'propvaluelike']]):
            node_q = node_q.join(model.NodePropertyLog
                                ).join(model.Property
                                ).join(model.Users)

        if 'status' in filt:
            if type(filt['status']) == list:
                node_q = node_q.filter(model.Status.name.in_(filt['status']))
            else:
                node_q = node_q.filter(model.Status.name == filt['status'])

        if 'statuslike' in filt:
            if type(filt['statuslike']) == list:
                for item in filt['statuslike']:
                    node_q = node_q.filter(model.Status.name.like(item))
            else:
                node_q = node_q.filter(
                    model.Status.name.like(filt['statuslike']))

        if 'property' in filt:
            if type(filt['property']) == list:
                node_q = node_q.filter(model.Property.name.in_(filt['property']))
            else:
                node_q = node_q.filter(model.Property.name == filt['property'])

        if 'propertylike' in filt:
            if type(filt['propertylike']) == list:
                for case in filt['propertylike']:
                    node_q = node_q.filter(model.Property.name.like(case))
            else:
                node_q = node_q.filter(
                    model.Property.name.like(filt['propertylike']))

        if 'node' in filt:
            if type(filt['node']) == list:
                node_q = node_q.filter(model.Node.name.in_(filt['node']))
            else:
                node_q = node_q.filter(model.Node.Name == filt['node'])

        if 'nodelike' in filt:
            if type(filt['nodelike']) == list:
                for case in filt['nodelike']:
                    node_q = node_q.filter(model.Node.name.like(case))
            else:
                node_q = node_q.filter(model.Node.name.like(filt['nodelike']))

        if 'user' in filt:
            if type(filt['user']) == list:
                node_q = node_q.filter(model.Users.name.in_(filt['user']))
            else:
                node_q = node_q.filter(model.User.name == filt['user'])

        if 'userlike' in filt:
            if type(filt['userlike']) == list:
                for like in filt['userlike']:
                    node_q = node_q.filter(model.User.name.like(like))
            else:
                node_q = node_q.filter(model.User.name.like(filt['userlike']))

        retval = []
        for node in node_q:
            retval.append(node.name)
        return retval
    getNodesFilter.signature = [ ["struct","struct"] ]

    def serverTime(self):
        """serverTime -> float

        returns the current time of the server as a POSIX timestamp
        """
        date = meta.Session.query('now'
                                 ).from_statement('SELECT NOW()').first()
        return int(time.mktime(date[0].timetuple()))
    serverTime.signature = [["int"]]

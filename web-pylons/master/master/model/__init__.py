"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from master.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #

    meta.Session.configure(bind=engine)
    meta.engine = engine


## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#

DeclarativeBase = declarative_base()

class Users(DeclarativeBase):
    __tablename__ = 'users'
    id = sa.Column("id", sa.types.Integer,
              sa.schema.Sequence('users_id_seq', optional=True),
              primary_key=True)
    username = sa.Column("username", sa.types.String(32), unique=True, nullable=False)
    name = sa.Column("name", sa.types.String(64))

    def __init__(self, username='', name=''):
        if username != '':
            self.username = username
        if name != '':
            self.name = name

    def __repr__(self):
        return "<User('%d', '%s', '%s')>"% (self.id, self.username, self.name)


class Status(DeclarativeBase):
    __tablename__ = 'status'
    id = sa.Column('id', sa.types.Integer,
                  sa.schema.Sequence('status_id_seq', optional=True),
                  primary_key=True)
    name = sa.Column('name', sa.types.String(32), unique=True, nullable=False)
    description = sa.Column('description', sa.types.String(255))

    def __init__(self, name='', description=''):
        if name:
            self.name = name
        if description:
            self.description = description


class Event(DeclarativeBase):
    __tablename__ = 'event'
    id = sa.Column('id', sa.types.Integer,
                  sa.schema.Sequence('event_id_seq',optional=True),
                  primary_key=True)
    name = sa.Column('name', sa.types.String(32), unique=True, nullable=False)
    description = sa.Column('description', sa.types.String)
    events = sa.orm.relation("NodeEventLog")

    def __init__(self, name='', description=''):
        if name:
            self.name = name
        if description:
            self.description = description


class Node(DeclarativeBase):
    __tablename__ = 'node'
    id = sa.Column("id", sa.types.Integer,
                  sa.schema.Sequence('node_id_seq', optional=True),
                  primary_key=True)
    name = sa.Column("name", sa.types.String(255), unique=True, nullable=False)
    properties = sa.orm.relation("NodeProperties")
    property_history = sa.orm.relation("NodePropertyLog")
    events = sa.orm.relation("NodeEventLog")
    status = sa.orm.relation("NodeStatus")
    status_history = sa.orm.relation("NodeStatusLog")

    def __init__(self, name=''):
        if name:
            self.name = name


class Property(DeclarativeBase):
    __tablename__ = 'property'
    id = sa.Column('id', sa.types.Integer,
                   sa.schema.Sequence('property_id_seq', optional=True),
                   primary_key=True)
    name = sa.Column('name', sa.types.String(32), nullable=False)
    description = sa.Column('description', sa.types.String(255))

    def __init__(self, name='', description=''):
        if name:
            self.name = name
        if description:
            self.description = description

class NodeStatusLog(DeclarativeBase):
    __tablename__ = 'node_status_log'
    id = sa.Column('id', sa.types.Integer,
              sa.schema.Sequence('node_status_log_id_seq', optional=True),
              primary_key=True)
    node_id = sa.Column('node_id', sa.types.Integer,
              sa.ForeignKey('node.id'), nullable=False)
    node = sa.orm.relation(Node, primaryjoin=node_id == Node.id)
    status_id = sa.Column('status_id', sa.types.Integer,
                sa.ForeignKey('status.id'), nullable=False)
    status = sa.orm.relation(Status, primaryjoin=status_id == Status.id)
    time = sa.Column('time', sa.types.DateTime, server_default='NOW()')
    comment = sa.Column('comment', sa.types.String, default='')
    user_id = sa.Column('user_id', sa.types.Integer,
               sa.ForeignKey('users.id'), nullable=False)
    user = sa.orm.relation(Users, primaryjoin=user_id == Users.id)

    def __init__(self, node=None, status=None, time=None, comment=None,
                 user=None):
        if node:
            self.node = node
        if status:
            self.status = status
        if time:
            self.time = time
        if comment:
            self.comment = comment
        if user:
            self.user = user

    def __repr__(self):
        return "<NodeStatusLog(id=%s, node=%s, status=%s, time=%s, comment=%s, user=%s)>"% (
            self.id, self.node, self.status,
            self.time, self.comment, self.user)

class NodeProperties(DeclarativeBase):
    __tablename__ = 'node_properties'
    id = sa.Column('id', sa.types.Integer, primary_key=True)
    node_id = sa.Column('node_id', sa.types.Integer,
                      sa.ForeignKey('node.id'), nullable=False)
    node = sa.orm.relation("Node", primaryjoin=node_id == Node.id)
    property_id = sa.Column('property_id', sa.types.Integer,
                    sa.ForeignKey('property.id'), nullable=False)
    property = sa.orm.relation(Property,
                               primaryjoin=property_id == Property.id)
    last_change = sa.Column('last_change', sa.types.DateTime,
                            server_default='NOW()')
    value = sa.Column('value', sa.types.String(64))
    comment = sa.Column('comment', sa.types.String)


class NodeEventLog(DeclarativeBase):
    __tablename__ = 'node_event_log'
    id = sa.Column('id', sa.types.Integer,
              sa.schema.Sequence('node_event_log_id_seq',
                                  optional=True),
              primary_key=True)
    node_id = sa.Column('node_id', sa.types.Integer,
              sa.ForeignKey('node.id'), nullable=False)
    node = sa.orm.relation(Node, primaryjoin=node_id == Node.id)

    event_id = sa.Column('event_id', sa.types.Integer,
                sa.ForeignKey('event.id'), nullable=False)
    event = sa.orm.relation(Event, primaryjoin=event_id == Event.id)

    time = sa.Column('time', sa.types.DateTime, server_default='NOW()')
    comment = sa.Column('comment', sa.types.String)

    user_id = sa.Column('user_id', sa.types.Integer,
              sa.ForeignKey('users.id'), nullable=False)
    user = sa.orm.relation(Users, primaryjoin=user_id == Users.id)

    def __init__(self, node=None, event=None, comment=None,
                 user=None, time=None):
        if node:
            self.node = node
        if event:
            self.event = event
        if time:
            self.time = time
        if comment:
            self.comment = comment
        if user:
            self.user = user


class NodePropertyLog(DeclarativeBase):
    __tablename__ = 'node_properties_log'
    id = sa.Column('id', sa.types.Integer,
              sa.schema.Sequence('node_properties_log_id_seq', optional=True),
              primary_key=True)
    node_id = sa.Column('node_id', sa.types.Integer,
              sa.ForeignKey('node.id'), nullable=False)
    node = sa.orm.relation(Node, primaryjoin=node_id == Node.id)
    property_id = sa.Column('property_id', sa.types.Integer,
                sa.ForeignKey('property.id'), nullable=False)
    property = sa.orm.relation(Property,
                               primaryjoin = property_id == Property.id)
    time = sa.Column('time', sa.types.DateTime, server_default='NOW()')
    value = sa.Column('value', sa.types.String(64))
    comment = sa.Column('comment', sa.types.String)


    def __init__(self, node=None, property=None, comment=None,
                 value=None, time=None):
        if node:
            self.node = node
        if property:
            self.property = property
        if time:
            self.time = time
        if comment:
            self.comment = comment
        if value:
            self.value = value


class NodeStatus(DeclarativeBase):
    __tablename__ = 'node_status'

    id = sa.Column('id', sa.types.Integer, primary_key=True)
    node_id = sa.Column('node_id', sa.types.Integer,
                     sa.ForeignKey('node.id'), nullable=False)
    node = sa.orm.relation(Node, primaryjoin=node_id == Node.id)
    status_id = sa.Column('status_id', sa.types.Integer,
                       sa.ForeignKey('status.id'), nullable=False)
    status = sa.orm.relation(Status, primaryjoin=status_id == Status.id)
    last_change = sa.Column('last_change', sa.types.DateTime)
    comment = sa.Column('comment', sa.types.String)
    user_id = sa.Column('user_id', sa.types.Integer,
                     sa.ForeignKey('users.id'), nullable=False)
    user = sa.orm.relation(Users, primaryjoin=user_id == Users.id)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass


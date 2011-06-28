import logging

from pylons import request, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
import webhelpers.paginate as paginate
from pylons.decorators import jsonify

from master.lib.base import BaseController, render
import datetime

from master.model import meta
import master.model as model

from sqlalchemy import func as s_func

log = logging.getLogger(__name__)

class NodeController(BaseController):
    def index(self):
        self.list()

    def view(self, id):
        node_q = model.meta.Session.query(model.Node)
        node = node_q.get(int(id))
        if not node:
            abort(404)
        c.node_name = node.name
        c.node_properties = [(property.property.name, property.value)
                             for property in node.properties]
        c.node_properties.sort()
        c.node_status = {'status': None, 'comment': None, 'user': None}
        if node.status:
            c.node_status = {'status': node.status[0].status.name,
                             'comment': node.status[0].comment,
                             'user': node.status[0].user.name}

        c.content = "Stuff"
        c.node_id = node.id
        c.event_history = self._get_event_history(node.id)
        c.event_keys = ['time', 'event', 'user', 'comment']
        c.status_history = self._get_status_history(node.id)[1]
        c.status_keys = ['time', 'status', 'user', 'comment']
        return render('/derived/node/view.html')

    def list(self):
        nodes = model.meta.Session.query(model.Node)
        c.paginator = paginate.Page(
            nodes,
            page = int(request.params.get('page', 1)),
            items_per_page = 50
        )
        return render('/derived/node/list.html')

    def name(self, id):
        query = meta.Session.query(model.Node)
        query = query.filter(model.Node.name == id)
        return self.view(query.first().id)

    def search(self):
        node_q = model.meta.Session.query(model.Node)
        nodes = node_q.filter(
            model.Node.name.like(unicode(request.POST['q']))).all()
        if len(nodes) == 1:
            return redirect(url(controller=u'node', action=u'name',
                                 id=nodes[0].name))
        else:
            c.paginator = paginate.Page(
                nodes,
                page = int(request.params.get('page', 1)),
                items_per_page = 50
            )
            return render('/derived/node/list.html')

    def _build_history_query(self, id, history_table, name_table, entries=10,
                 start_time=None, end_time=None, exclude_job_related = False):
        history_q = meta.Session.query(
                                    history_table
                                ).join(
                                    model.Node,
                                ).join(
                                    name_table,
                                ).join(
                                    model.Users
                                ).filter(
                                    model.Node.id == id
                                )
        if start_time:
            history_q = history_q.filter(
                history_table.time >= datetime.datetime.strptime(
                                                start_time, '%Y-%m-%d'))
        if end_time:
            history_q = history_q.filter(
                history_table.time <= datetime.datetime.strptime(
                                            end_time, '%Y-%m-%d'))

        if exclude_job_related:
            history_q = history_q.filter("comment not like 'Starting%'"
                ).filter("comment not like 'Completing%'")

        history_q = history_q.order_by(history_table.time.desc())

        if entries > 0 and not start_time and not end_time:
            history_q = history_q.limit(entries)
        return history_q

    def _get_status_history(self, id, entries=10, start_time=None,
                            end_time=None, exclude_job_related=False):
        node_status_log_q = self._build_history_query(
                                    id,
                                    model.NodeStatusLog,
                                    model.Status,
                                    entries,
                                    start_time,
                                    end_time,
                                    exclude_job_related)
        retval = []
        for status_log in node_status_log_q:
            retval.append({'name': status_log.node.name,
                           'status': status_log.status.name,
                           'time': status_log.time.strftime('%c'),
                           'user': status_log.user.name,
                           'comment': status_log.comment})
        return ('status', retval)

    @jsonify
    def status_history(self, id, entries=10, start_date=None, end_date=None, filter=None):
        return self._get_status_history(id, entries, start_date, end_date, filter)

    def _get_event_history(self, id, entries=10, start_time=None,
                           end_time=None):
        history_q = self._build_history_query(
            id,
            model.NodeEventLog,
            model.Event,
            entries,
            start_time,
            end_time
        )
        retval = []
        for event_log in history_q:
            retval.append({'name': event_log.node.name,
                           'event': event_log.event.name,
                           'time': event_log.time.strftime('%c'),
                           'user': event_log.user.name,
                           'comment': event_log.comment})
        return retval

    @jsonify
    def event_history(self, id, entries=10, start_date=None, end_date=None):
        return self._get_event_history(id, entries, start_date, end_date)

    @jsonify
    def heirarchical_properties(self, id):
        node = meta.Session.query(model.Node).get(int(id))
        retval = {'data': 'Properties', 'children': []}
        # We need to convert names of the form
        # dimm.3.manufacturer = Qimonda
        # dimm.3.part_number = 72T512220EP3SC2
        # to hashes of the form
        # {
        #   'data': 'dimm', 
        #   'children': [
        #       {
        #           'data': '3',
        #           'children': [
        #               {
        #                   'data': 'manufacturer',
        #                   'children': [{'data': 'Qimonda'},]
        #               },
        #               {
        #                   'data': 'part_number',
        #                   'children': [{'data': '72T512220EP3SC2'}]
        #               },
        #           ],
        #       },
        #   ],
        # }
        for property in node.properties:
            name = property.property.name
            name_parts = name.split('.')
            tree_location = retval
            for part in name_parts:
                found_tree = False
                if part == 'mem':
                    mem = True
                if tree_location['data'] == part:
                    # We are still at the root of the current tree location
                    # wait until next round to search the children.
                    found_tree = True
                for child in tree_location['children']:
                    if child['data'] == part:
                        tree_location = child
                        found_tree = True
                        break
                if not found_tree:
                    # We need add a new child as the tree_location.
                    tmp_child = {'data': part, 'children': []}
                    tree_location['children'].append(tmp_child)
                    tree_location['state'] = 'closed'
                    tree_location = tmp_child
            tree_location['state'] = 'open'
            tree_location['children'].append({'data': property.value})

        return retval

    @jsonify
    def top(self, what, how_many=10, period=7):
        """top(what, how_many) -> [[node, count]...]

        top returns the top how_many nodes and the count of events
        of type what period days.
        """

        start_date = datetime.date.today() - datetime.timedelta(int(period))
        status_q = meta.Session.query(
                        model.Node.name, s_func.count(model.Node.name)
                    ).join(
                        model.NodeStatusLog
                    ).join(
                        model.Status
                    ).filter(
                        model.Status.name == what
                    ).filter(
                        model.NodeStatusLog.time >= start_date
                    ).group_by(
                        model.Node.name
                    ).order_by(
                        s_func.count(model.Node.name).desc()
                    ).limit(how_many)
        result = []
        for row in status_q:
            result.append([row[0], row[1]])

        return {'results': result}

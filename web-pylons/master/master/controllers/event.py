import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

import webhelpers.paginate as paginate

from master.lib.base import BaseController, render
import master.model as model

import master.lib.helpers as helpers

log = logging.getLogger(__name__)


class EventController(BaseController):
    def __init__(self):
        self.query = model.meta.Session.query(model.Event)

    def list(self):
        events_q = model.meta.Session.query(model.Event)
        c.paginator = paginate.Page(
            events_q,
            page=int(request.params.get('page', 1)),
            items_per_page=10,
        )

        return render('/derived/event/list.html')

    def view(self, id):
        events_q = model.meta.Session.query(model.Event)
        event = events_q.get(int(id))
        if not event:
            abort(404, "Event not found.")
        c.id = event.id
        c.event_id = event.id
        c.event_name = event.name
        c.event_description = event.description
        return render('/derived/event/view.html')

    @jsonify
    def rate(self, id, period=24, start_date=None, end_date=None):
        (start_date, end_date) = helpers.setup_dates_for_rate(start_date,
                                                              end_date)
        self.me = self.query.get(int(id))
        self.frequency_q = model.meta.Session.query(
            "count", "time"
        ).from_statement(
            """SELECT
                        COUNT(*),
                        date_trunc('hour', time) AS time
                        FROM node_event_log
                        WHERE
                            event_id = :eventid
                            and time >= :start
                            and time <= :end
                        GROUP BY
                            time
                """
        ).params(
            eventid=self.me.id,
            start=start_date,
            end=end_date
        )
        return self.build_frequency(period)

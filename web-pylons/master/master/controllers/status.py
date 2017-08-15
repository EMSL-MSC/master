import logging

from pylons import request, tmpl_context as c
from pylons.controllers.util import abort
from pylons.decorators import jsonify

import webhelpers.paginate as paginate

from master.lib.base import BaseController, render
import master.lib.helpers as helpers
import master.model as model

log = logging.getLogger(__name__)


class StatusController(BaseController):
    def __init__(self):
        self.query = model.meta.Session.query(model.Status)

    def index(self):
        self.list()

    def list(self):
        status_q = model.meta.Session.query(model.Status)
        c.paginator = paginate.Page(
            status_q,
            page=int(request.params.get('page', 1)),
            items_per_page=10,
        )

        return render('/derived/status/list.html')

    def view(self, id):
        status_q = model.meta.Session.query(model.Status)
        status = status_q.get(int(id))
        if not status:
            abort(404, "Status not found.")
        c.id = status.id
        c.status_id = status.id
        c.status_name = status.name
        c.status_description = status.description
        return render('/derived/status/view.html')

    @jsonify
    def rate(self, id, period=24, start_date=None, end_date=None):
        (start_date, end_date) = helpers.setup_dates_for_rate(start_date,
                                                              end_date)
        status = self.query.get(int(id))
        self.me = status

        self.frequency_q = model.meta.Session.query(
            "count", "time"
        ).from_statement(
            """SELECT
                                COUNT(*),
                                date_trunc('hour', time) AS time
                                FROM node_status_log
                                WHERE
                                    status_id = :status_id
                                    and time >= :start
                                    and time <= :end
                                GROUP BY
                                    date_trunc('hour', time)
                        """
        ).params(
            status_id=status.id,
            start=start_date,
            end=end_date)
        return self.build_frequency(period)

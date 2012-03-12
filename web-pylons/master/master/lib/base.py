"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging

from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons.decorators import jsonify

from master.model import meta
import time

log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

    @jsonify
    def fetch_name(self, id):
        my_data = self.query.get(int(id))
        return {"id": unicode(id), "name": unicode(my_data.name)}

    def build_frequency(self, period):
        events_per_period = {}
        rows = self.frequency_q.all()
        for event_instance in rows:
            period_bucket = time.mktime(event_instance.time.timetuple()) \
                    - (time.mktime(event_instance.time.timetuple()) \
                       % (int(period)*3600))
            events_per_period[period_bucket] = events_per_period.get(
                                                    period_bucket, 0) + event_instance.count
        periods = events_per_period.keys()
        periods.sort()
        frequency_dataset = []
        index = 0
        for period_bucket in periods:
            index += 1
            frequency_dataset.append((int(period_bucket)*1000,
                                      events_per_period[period_bucket]))
        return {u"label": unicode(self.me.name), u"data": frequency_dataset }

"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html.tags import *

from routes import URLGenerator
from pylons import url

def setup_dates_for_rate(start_date=None, end_date=None):
    import datetime
    if start_date == None:
        start_date = datetime.date.today() - datetime.timedelta(30)
    else:
        start_date = datetime.date(*(datetime.datetime.strptime(
                         start_date, '%Y-%m-%d').timetuple()[0:3]))
    if end_date == None:
        end_date = datetime.date.today() + datetime.timedelta(1)
    else:
        end_date = datetime.date(*(datetime.datetime.strptime(
                        end_date, '%Y-%m-%d').timetuple()[0:3]))

    return start_date, end_date

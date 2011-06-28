import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from master.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PropertyController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/property.mako')
        # or, return a response
        return 'Hello World'

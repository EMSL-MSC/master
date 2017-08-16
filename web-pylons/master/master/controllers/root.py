import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from master.lib.base import BaseController, render

log = logging.getLogger(__name__)


class RootController(BaseController):

    def index(self):
        # Return a rendered template
        # return render('/root.mako')
        # or, return a response
        return render('/derived/root/index.html')

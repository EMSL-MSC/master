from master.tests import *


class TestXmlrpcController(TestController):

    def test_get_nodes(self):
        response = self.app.get(url(controller='xmlrpc', action='index'))

from master.tests import *

class TestNodeController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='node', action='index'))
        # Test response...
        response == 'e'

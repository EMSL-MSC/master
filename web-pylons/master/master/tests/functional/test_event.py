from master.tests import *


class TestEventController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='event', action='index'))
        # Test response...

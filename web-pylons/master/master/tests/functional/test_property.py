from master.tests import *

class TestPropertyController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='property', action='index'))
        # Test response...

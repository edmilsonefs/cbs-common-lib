import unittest

from helper.platform.bugger import create_bug
from helper.tests.testify import data_helper


class ResultsPublishTest(unittest.TestCase):

    def _test_e2e_publish_flow(self):
        self.assertTrue('Issue should be created', create_bug(data_helper.mock_response))

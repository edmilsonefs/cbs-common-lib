import os
import unittest

from helper.platform.api import authenticator
from helper.platform.api.data_collector import DataCollector


class DataCollectorTest(unittest.TestCase):
    data_collector = DataCollector()

    def test_collections_not_empty(self):
        token = authenticator.login(os.getenv('testlio_username'), os.getenv('testlio_password'))
        self.data_collector.token = token
        print(token)

        query = 'Heartbeat /livetv/check availability pageName'
        json_data = self.data_collector.get_issues(query)
        print json_data

        issue_exists = self.data_collector.get_filtered_result(json_data, state='new')
        self.assertTrue(issue_exists)


if __name__ == '__main__':
    unittest.main()

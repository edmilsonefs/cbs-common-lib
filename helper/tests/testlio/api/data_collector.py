import os
import unittest

from helper.platform.api import authenticator
from helper.platform.api.data_collector import DataCollector


class AuthenticatorTest(unittest.TestCase):
    data_collector = DataCollector()

    def test_collections_not_empty(self):
        token = authenticator.login(os.getenv('testlio_username'), os.getenv('testlio_password'))
        self.data_collector.token = token
        print(token)

        json_data = self.data_collector.get_collections()
        self.assertEquals("", json_data)


if __name__ == '__main__':
    unittest.main()

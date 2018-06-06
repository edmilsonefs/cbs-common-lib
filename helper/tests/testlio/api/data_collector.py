import unittest

from helper.testlio.api import authenticator
from helper.testlio.api.data_collector import DataCollector


class AuthenticatorTest(unittest.TestCase):

    data_collector = DataCollector()

    def test_collections_not_empty(self):
        token = authenticator.login("denys.zaiats@gmail.com", "")
        self.data_collector.token = token

        json_data = self.data_collector.get_collections()
        self.assertEquals("", json_data)


if __name__ == '__main__':
    unittest.main()

import unittest
from time import sleep

from helper.testlio.api import authenticator
from helper.testlio.api.data_collector import DataCollector


class AuthenticatorTest(unittest.TestCase):

    data_collector = DataCollector()

    def test_collections_not_empty(self):
        count = 0
        while count < 10:
            token = authenticator.login("denys.zaiats@gmail.com", "")
            if token is not None:
                self.data_collector.token = token
                break
            sleep(3)
            count += 1

        json_data = self.data_collector.get_collections()
        self.assertEquals("", json_data)


if __name__ == '__main__':
    unittest.main()

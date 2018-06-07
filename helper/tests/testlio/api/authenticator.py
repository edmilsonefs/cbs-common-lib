import os
import unittest

from helper.testlio.api import authenticator


class AuthenticatorTest(unittest.TestCase):

    def test_login_fail(self):
        token = authenticator.login(os.getenv('testlio_username'), os.getenv('testlio_password'))
        self.assertNotEquals(None, token)


if __name__ == '__main__':
    unittest.main()

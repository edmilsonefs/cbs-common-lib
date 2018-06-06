import unittest

from helper.testlio.api import authenticator


class AuthenticatorTest(unittest.TestCase):

    def test_login_success(self):
        expected = authenticator.login("denys.zaiats@gmail.com", "")
        self.assertNotEquals(None, expected)


if __name__ == '__main__':
    unittest.main()

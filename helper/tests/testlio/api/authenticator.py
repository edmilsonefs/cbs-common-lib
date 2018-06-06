import unittest

from helper.testlio.api import authenticator


class AuthenticatorTest(unittest.TestCase):

    def test_login_fail(self):
        expected = authenticator.login("denys.zaiats@gmail.com", "")
        self.assertEquals(None, expected)


if __name__ == '__main__':
    unittest.main()

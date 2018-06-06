import unittest

from helper.testlio.api import authenticator


class AuthenticatorTest(unittest.TestCase):

    def test_login_fail(self):
        token = authenticator.login("denys.zaiats@gmail.com", "")
        self.assertEquals(None, token)


if __name__ == '__main__':
    unittest.main()

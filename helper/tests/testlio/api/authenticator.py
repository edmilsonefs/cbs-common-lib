import unittest

from helper.testlio.api import authenticator


class AuthenticatorTest(unittest.TestCase):

    def test_login_success(self):
        expected = authenticator.login("", "")
        self.assertEquals("", str(expected))


if __name__ == '__main__':
    unittest.main()

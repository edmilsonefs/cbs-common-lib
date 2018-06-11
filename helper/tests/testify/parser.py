import unittest

from helper.testify import parser
from helper.tests.testify import data_helper
from helper.tests.testify.data_helper import actual


class ParserTest(unittest.TestCase):

    def test_parser(self):
        expected = parser.parse_response_to_set(data_helper.mock_response)
        self.assertEquals(actual, str(expected))


if __name__ == '__main__':
    unittest.main()

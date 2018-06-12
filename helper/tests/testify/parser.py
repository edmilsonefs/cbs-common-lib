import unittest

from helper.testify import parser
from helper.tests.testify import data_helper
from helper.tests.testify.data_helper import actual, actual_empty, actual_short


class ParserTest(unittest.TestCase):

    def test_parser(self):
        expected = parser.parse_response_to_set(data_helper.mock_response)
        self.assertEquals(actual, str(expected))

    def test_parser_short(self):
        expected = parser.parse_response_to_set(data_helper.mock_response_short)
        self.assertEquals(actual_short, str(expected))

    def test_parser_empty_response(self):
        expected = parser.parse_response_to_set(data_helper.mock_response_empty)
        self.assertEquals(actual_empty, str(expected))

    def test_parser_empty_text_response(self):
        expected = parser.parse_response_to_set(data_helper.mock_response_empty_text)
        self.assertEquals(actual_empty, str(expected))

    def test_parser_empty_json(self):
        expected = parser.parse_response_to_set(data_helper.mock_response_empty_text)
        self.assertEquals(actual_empty, str(expected))


if __name__ == '__main__':
    unittest.main()

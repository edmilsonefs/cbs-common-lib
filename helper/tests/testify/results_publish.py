import json
import os
import unittest

from helper.platform.api import authenticator
from helper.platform.api.data_collector_publisher import DataCollectorPublisher
from helper.testify import parser
from helper.tests.testify import data_helper


class ResultsPublishTest(unittest.TestCase):

    def test_e2e_publish_flow(self):
        set_issues = parser.parse_response_to_set(data_helper.mock_response)

        token = authenticator.login(os.getenv('testlio_username'), os.getenv('testlio_password'))

        self.data_collector_publisher = DataCollectorPublisher()
        self.data_collector_publisher.token = token

        for issue in set_issues:
            i = json.loads(issue)
            if str(i['status']) == 'Fail':
                query = '{0} {1} {2} {3}'.format(str(i['profile']), str(i['required']), str(i['Name']), str(i['value']))
                json_data = self.data_collector_publisher.get_issues(query)
                issue_exists = self.data_collector_publisher.get_filtered_result(json_data, state='new')
                if not issue_exists:
                    title = '[AUTOMATION] - {0} ({1})'.format(query, str(hash(query)))
                    description = issue
                    app_version = os.getenv("BUILD_VERSION")
                    self.assertTrue('Issue {0} should be created'.format(description),
                                    self.data_collector_publisher.post_issue(title, description, app_version))

import json
import os

from helper.platform.api import authenticator
from helper.platform.api.data_collector_publisher import DataCollectorPublisher
from helper.testify import parser


def create_bug(response):
    set_issues = parser.parse_response_to_set(response)

    token = authenticator.login(os.getenv('testlio_username'), os.getenv('testlio_password'))

    data_collector_publisher = DataCollectorPublisher()
    data_collector_publisher.token = token

    success_responses_counter = 0

    for issue in set_issues:
        i = json.loads(issue)
        if str(i['status']) == 'Fail':
            query = '{0} {1} {2} {3}'.format(str(i['profile']), str(i['required']), str(i['Name']), str(i['value']))
            json_data = data_collector_publisher.get_issues(query)
            issue_exists = data_collector_publisher.get_filtered_result(json_data, state='new')
            if not issue_exists:
                title = '[AUTOMATION][{0}] - {1} {2} {3} ({4})'.format(str(i['profile']), str(i['required']), str(i['Name']), str(i['value']), str(hash(query)))
                description = issue
                app_version = 'CBS' + os.getenv("BUILD_VERSION")
                if data_collector_publisher.post_issue(title, description, app_version):
                    success_responses_counter += 1

    return success_responses_counter == len(set_issues)

# -*- coding: utf-8 -*-
import json
import os

from helper.platform.api import authenticator
from helper.platform.api.data_collector_publisher import DataCollectorPublisher
from helper.platform.data_helper import str_to_int_sum
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
            profile = ''
            required = ''
            name = ''
            value = ''

            try:
                profile = str(i['profile'])
            except:
                pass

            try:
                required = str(i['required'])
            except:
                pass

            try:
                name = str(i['Name'])
            except:
                pass

            try:
                value = str(i['value'])
            except:
                pass

            query = '{0} {1} {2} {3}'.format(profile, required, name, value)
            json_data = data_collector_publisher.get_issues(query)
            issue_exists = data_collector_publisher.get_filtered_result(json_data, state='new')
            if not issue_exists:
                title = '[AUTOMATION][{0}] - {1} {2} {3} ({4})'.format(profile, required, name, value, str(str_to_int_sum(query)))
                description = issue
                app_version = 'CBS' + os.getenv("BUILD_VERSION")
                if data_collector_publisher.post_issue(title, description, app_version):
                    success_responses_counter += 1
import json

import requests

from helper.platform.api.issue import Issue

PROJECT_ID = '03e98be0-c099-4037-a515-de77ef8d7efb'
BASE_API_URL = 'https://api.testlio.com'


class DataCollector:
    token = ''

    def __init__(self):
        pass

    def get_issues(self, query):
        headers = {"Authorization": 'Bearer ' + self.token}
        response = requests.get(
            BASE_API_URL + '/issue/v1/collections/' + PROJECT_ID + '/issues/?isDeleted=false&q=' + query,
            headers=headers, allow_redirects=True)
        return json.loads(response.text)

    def get_filtered_result(self, json_data, **kwargs):
        issues = json_data['issues']
        issues_collection = set()

        filter_state = None
        filter_app_version = None
        filter_device = None

        try:
            if kwargs['state'] is not None:
                filter_state = kwargs['state']
            if kwargs['app_version'] is not None:
                filter_app_version = kwargs['app_version']
            if kwargs['device'] is not None:
                filter_device = kwargs['device']
        except:
            pass

        for issue in issues:
            state = issue['state']

            try:
                app_version = issue['calculatedData']['environment']['testableAppVersion']
                device = issue['calculatedData']['environment']['deviceAndOs']
            except:
                app_version = None
                device = None

            if (filter_state == str(state) if filter_state is not None else True) \
                    and (filter_app_version == str(app_version) if filter_app_version is not None else True) \
                    and (filter_device == str(device) if filter_device is not None else True):
                issues_collection.add(Issue(state, app_version, device))

        return len(issues_collection) > 0

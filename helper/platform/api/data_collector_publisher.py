import json
from urllib import quote

import requests

from helper.platform.api.data_keeper import PROJECT_ID, BASE_API_URL
from helper.platform.api.issue import Issue


class DataCollectorPublisher:
    token = ''

    def __init__(self):
        pass

    def get_issues(self, query):
        headers = {"Authorization": 'Bearer ' + self.token}
        response = requests.get(
            BASE_API_URL + '/issue/v1/collections/' + PROJECT_ID + '/issues/?isDeleted=false&q=' + quote(str(hash(query))),
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

    def post_issue(self, title, description_body, app_version):
        body = {
            "title": title,
            "description": "Data validation is failed with failures: " + description_body,
            "assignedTo": {
                "href": "https://api.testlio.com/user/v1/users/5727"
            },
            "isApproved": "false",
            "severity": "low",
            "labels": ["bug", "automation"],
            "isClosed": "false",
            "isDeleted": "false",
            "buildVersion": app_version,
            "isStarred": "false"
        }

        headers = {"Authorization": 'Bearer ' + self.token}
        response = requests.post(url=BASE_API_URL + '/issue/v1/collections/' + PROJECT_ID + '/issues', data=json.dumps(body), headers=headers)

        return response.status_code == 200


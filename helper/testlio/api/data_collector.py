import json

import requests

BASE_API_URL = 'https://api.testlio.com'


class DataCollector:
    token = ''

    def __init__(self):
        pass

    def get_collections(self):
        headers = {"Authorization": 'Bearer ' + self.token}
        response = requests.get(BASE_API_URL + '/issue/v1/collections/e6e01903-aa70-40e6-aeb1-dd812d19b9dd/issues',
                                headers=headers, allow_redirects=True)
        return json.loads(response.text)

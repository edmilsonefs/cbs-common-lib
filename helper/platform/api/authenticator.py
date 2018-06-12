import re
from time import sleep
from urllib import quote

import requests

from helper.platform.api.data_keeper import BASE_PLATFORM_URL


def login(email, password):
    token = None
    count = 0
    while count < 10:
        response = requests.get(BASE_PLATFORM_URL + '/login')
        body = response.text
        csfr_token = re.search('"csfrtoken":"(.+)"', body).group(1)

        login_url = '/login?next=https%3A%2F%2Fplatform.testlio.com%2Foauth%2Ftokens%3Fresponse_type%3Dtoken%26client_id%3Dautomated_tests%26redirect_uri%3Dhttp%253A%252F%252Flocalhost:4723'
        headers = {'Referer': BASE_PLATFORM_URL + login_url,
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Upgrade-Insecure-Requests': '1',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}

        post_body = quote('user[email]') + '=' + quote(email) + '&' + quote('user[password]') + '=' + quote(
            password) + '&csrf-token=' + quote(csfr_token)

        response = requests.post(url=BASE_PLATFORM_URL + login_url, data=post_body, headers=headers, cookies=response.cookies)

        if response.status_code == 200:
            url = response.url
            s = re.search('access_token=(.+)&token_type', url)
            if s:
                token = s.group(1)
                break
            sleep(3)
            count += 1
        else:
            sleep(3)
            count += 1

    return token

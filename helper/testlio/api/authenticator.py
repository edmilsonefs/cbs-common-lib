import requests

BASE_URL = 'https://platform.testlio.com'


def login(email, password):
    r = requests.get(BASE_URL + '/login')
    print(r.content)

import json
from time import sleep

import subprocess

import os
from pip._vendor import requests

"""
Usage:

1. Set the configuration in the testable class:
    - TestifyConfig.platform = 'Android' or 'iOS'
    - TestifyConfig.testify_url = '{url}'

2. Call method upload, as:
    - TestifyConfig.upload(TestifyConfig.video_profile({video_type})), where video type: clips, shows, live tv, movies
    - TestifyConfig.upload(TestifyConfig.sign_in_profile({omniture_profile}))

    methods return Boolean
"""

testify_url = None
platform = None
buildversion = os.getenv("BUILD_VERSION")


def video_profile(video_type, testtype):
    # return {
    #     'p_name': "{'Omniture':'" + "OM " + platform + " CBS Ent App" + "',"
    #               "'Heartbeat':'" + "HB CBSAPP " + platform + "'}",
    #     'skip_pass': "True", 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com', 'kristjan@testlio.com']",
    #     'appname': "CBS App", 'platform': platform, 'buildversion': str(buildversion), 'videotype': video_type}
    return _get_testify_config({
        'omniture': 'OM ' + platform + ' CBS Ent App',
        'heartbeat': 'HB CBSAPP ' + platform,
        'platform': platform,
        'buildversion': str(buildversion),
        'videotype': video_type,
        'testtype': testtype
        })


def sign_in_profile(omniture_profile, testtype):
    # return {
    #     'p_name': "{'Omniture':'" + omniture_profile + "',"
    #               "'Heartbeat':'" + "HB CBSAPP " + platform + "'}",
    #     'skip_pass': "True", 'email_list': "['bryan.gaikwad@cbsinteractive.com','joael.harbi@cbsinteractive.com','kristjan@testlio.com']",
    #     'appname': "CBS App", 'platform': platform, 'buildversion': str(buildversion)}
    return _get_testify_config({
        'omniture': omniture_profile,
        'platform': platform,
        'buildversion': str(buildversion),
        'testtype': testtype
        })


def _get_testify_config(params=[]):
    """Unified method for returning all variations of Testify upload profile.

    It also features built-in checks on required fields. Returns dictionary.
    """
    config = {}

    if 'omniture' in params and 'heartbeat' in params:
        profiles = {'Omniture': params['omniture'],
                    'Heartbeat': params['heartbeat']}
    elif 'omniture' in params:
        profiles = {'Omniture': params['omniture']}
    elif 'heartbeat' in params:
        profiles = {'Heartbeat': params['heartbeat']}
    else:
        raise Exception("At least one profile is required")
    config['p_name'] = str(profiles)

    # config['email_list'] = ['bryan.gaikwad@cbsinteractive.com','joael.harbi@cbsinteractive.com','kristjan@testlio.com']
    config['email_list'] = str(['valdo@testlio.com', 'kristjan@testlio.com'])
    config['platform'] = params['platform']
    config['appname'] = 'CBS App'
    config['buildversion'] = str(params['buildversion'])
    config['skip_pass'] = 'True'
    config['testtype'] = params['testtype']

    if 'videotype' in params:
        config['videotype'] = params['videotype']

    return config


def upload_dump(payload):
    print("Start uploading of dump.har file")
    print("1. Kill proxy")
    subprocess.call(["bash", "-c", "kill_proxy"])
    sleep(60)  # wait until dum.har is ready
    print("2. Wait 60 seconds")
    try:
        # Open file and send contents
        print("3. Start POST request")
        files = {'file': open("./dump.har", 'rb')}
        # Generate a post request and pass the information r=
        r = requests.post(testify_url, files=files, data=payload)

        print("4. Request payload data: " + str(payload))
        print("\n5. Response from Testify API:\n")
        print(r.content)

        return True
    except Exception, e:
        payload = json.dumps({'status': 'error', 'message': '' + str(e)})
        print("3. Dump.har uploading is failed. " + str(payload))

        return False

import json
from time import sleep
import subprocess
import os
import requests

from helper.platform.bugger import create_bug

"""
Usage:

1. Set the configuration in the testable class:
    - TestifyConfig.platform = 'Android' or 'iOS'
    - TestifyConfig.testify_url = '{url}'

2. Call method upload, as:
    - TestifyConfig.upload(TestifyConfig.video_profile({video_type, testtype}))
            where video type: clips, shows, live tv, movies
    - TestifyConfig.upload(TestifyConfig.omniture_profile({omniture_profile, testtype}))

    methods return Boolean
"""

testify_url = None
platform = None
buildversion = os.getenv("BUILD_VERSION")


def video_profile_shows():
    return _get_testify_config({
        'omniture': 'OM ' + platform + ' CBS Ent App',
        'heartbeat': 'HB CBSAPP ' + platform,
        'platform': platform,
        'buildversion': str(buildversion),
        'videotype': 'shows',
        'testtype': 'Show Page'
    })


def video_profile_livetv():
    return _get_testify_config({
        'omniture': 'OM ' + platform + ' CBS Ent App',
        'heartbeat': 'HB CBSAPP ' + platform + ' - Live TV',
        'platform': platform,
        'buildversion': str(buildversion),
        'videotype': 'live tv',
        'testtype': 'Live TV Page'
    })


def video_profile_clips():
    return _get_testify_config({
        'omniture': 'OM ' + platform + ' CBS Ent App',
        'heartbeat': 'HB CBSAPP ' + platform + ' - Clips',
        'platform': platform,
        'buildversion': str(buildversion),
        'videotype': 'clips',
        'testtype': 'Clips Page'
    })


def video_profile_movies():
    return _get_testify_config({
        'omniture': 'OM ' + platform + ' CBS Ent App',
        'heartbeat': 'HB CBSAPP ' + platform + ' - Movies',
        'platform': platform,
        'buildversion': str(buildversion),
        'videotype': 'movies',
        'testtype': 'Movie Page'
    })


def omniture_profile(omniture_profile, testtype):
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

    config['email_list'] = str([
        'bryan.gaikwad@cbsinteractive.com',
        'joael.harbi@cbsinteractive.com',
        'cbs-automation@testlio.com'
    ])
    # config['email_list'] = str(['valdo@testlio.com', 'kristjan@testlio.com'])
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
        print("4. Request payload data: " + str(payload))
        r = requests.post(testify_url, files=files, data=payload)

        print("\n5. Response from Testify API:\n")
        print(r.content)
        print("\n6. Post bugs to Tetslio:\n")

        # if str(platform).lower() == 'android':
        #     try:
        #         return create_bug(r.content)
        #     except Exception, e:
        #         print("6. Failure in bug creation. " + str(e))
        #         return False

        return True
    except Exception, e:
        payload = json.dumps({'status': 'error', 'message': '' + str(e)})
        print("3. Dump.har uploading is failed. " + str(payload))

        return False

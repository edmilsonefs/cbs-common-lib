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


def video_profile(video_type):
    return {
        'p_name': "{'Comscore':'CS CBSNAPP',"
                  "'Omniture':'" + "OM " + platform + " CBS Ent App" + "',"
                  "'LEVT': 'Video LEVT CBSS App',"
                  "'Heartbeat':'" + "HB CBSAPP " + platform + "'}",
        'skip_pass': "True", 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com']",
        'appname': "Video LEVT CBSS App", 'platform': platform, 'buildversion': str(buildversion), 'videotype': video_type}


def sign_in_profile(omniture_profile):
    return {
        'p_name': "{'Comscore':'CS CBSNAPP',"
                  "'Omniture':'" + omniture_profile + "',"
                  "'LEVT': 'Video LEVT CBSS App',"
                  "'Heartbeat':'" + "HB CBSAPP " + platform + "'}",
        'skip_pass': "True", 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com']",
        'appname': "Video LEVT CBSS App", 'platform': platform, 'buildversion': str(buildversion)}


def upload_dump(payload):
    print("Start uploading of dump.har file")
    print("1. Kill proxy")
    subprocess.call(["bash", "-c", "kill_proxy"])
    sleep(120)  # wait until dum.har is ready
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

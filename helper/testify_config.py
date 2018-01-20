import json
from time import sleep

import subprocess

import os
from pip._vendor import requests


testify_url = None
platform = None
buildversion = os.getenv("BUILD_VERSION")


def video_profile(video_type):
    return {
        'p_name': "{'Comscore':'" + "CS CBSNAPP" + "','Omniture':'" + "OM " + platform + " CBS Ent App" + "','LEVT':'" + "Video LEVT CBSS App" + "','Heartbeat':'" + "HB CBSAPP " + platform + "'}",
        'skip_pass': "True", 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com']",
        'appname': "Video LEVT CBSS App", 'platform': platform, 'buildversion': str(buildversion), 'videotype': video_type}


def sign_in_profile(omniture_profile):
    return {
        'p_name': "{'Comscore':'" + "CS CBSNAPP" + "','Omniture':'" + omniture_profile + "','LEVT':'" + "Video LEVT CBSS App" + "','Heartbeat':'" + "HB CBSAPP " + platform + "'}",
        'skip_pass': "True", 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com']",
        'appname': "Video LEVT CBSS App", 'platform': platform, 'buildversion': str(buildversion)}


def upload_dump(payload):
    print("Start uploading of dump.har file")
    print("1. Kill proxy")
    subprocess.call(["bash", "-c", "kill_proxy"])
    sleep(120)  # wait until dum.har is ready
    print("2. Wait 60 seconds")
    try:
        # print("Sandbox folder start:\n")
        # print(subprocess.check_output(['ls', '-la', './sandbox']))
        # print("Sandbox folder end:\n")
        # Open file and send contents
        print("3. Start POST request")
        files = {'file': open("./dump.har", 'rb')}
        # Generate a post request and pass the information r=
        self.log_info("Start POST Request to: " + testify_url)
        r = requests.post(testify_url, files=files, data=payload)

        print("4. Request payload data: " + str(payload))
        print("\n5. Response from Testify API:\n")
        print(r.content)

        return True
    except Exception, e:
        payload = json.dumps({'status': 'error', 'message': '' + str(e)})
        print("3. Dump.har uploading is failed. " + str(payload))

        return False

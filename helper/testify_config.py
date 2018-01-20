import json
from time import sleep

import os
from pip._vendor import requests


def _get_platform():
    platform = os.getenv('PLATFORM') or (
        'android' if os.getenv('ANDROID_HOME') else 'ios')

    if platform.lower() == 'android':
        return 'Android'
    else:
        return 'iOS'


testify_url = None
comscore_profile = "CS CBSNAPP"
levt_profile = "Video LEVT CBSS App"
heartbit_profile = "HB CBSAPP " + _get_platform()
skip_pass = "True"
appname = 'CBSAA'
buildversion = os.getenv("BUILD_VERSION")


def video_profile(video_type):
    return {
        'p_name': "{'Comscore':'" + comscore_profile + "','Omniture':'" + "OM " + _get_platform() + " CBS Ent App" + "','LEVT':'" + levt_profile + "','Heartbeat':'" + heartbit_profile + "'}",
        'skip_pass': skip_pass, 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com']",
        'appname': appname, 'platform': _get_platform(), 'buildversion': str(buildversion), 'videotype': video_type}


def sign_in_profile(omniture_profile):
    return {
        'p_name': "{'Comscore':'" + comscore_profile + "','Omniture':'" + omniture_profile + "','LEVT':'" + levt_profile + "','Heartbeat':'" + heartbit_profile + "'}",
        'skip_pass': skip_pass, 'email_list': "['bryan.gaikwad@cbsinteractive.com', 'joael.harbi@cbsinteractive.com']",
        'appname': appname, 'platform': _get_platform(), 'buildversion': str(buildversion)}


def upload_dump(payload):
    print("Start uploading of dump.har file")
    print("1. Kill proxy")
    os.subprocess.call(["bash", "-c", "kill_proxy"])
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
        r = requests.post(testify_url, files=files, data=payload)

        print("4. Request payload data: " + str(payload))
        print("\n5. Response from Testify API:\n")
        print(r.content)

        return True
    except Exception, e:
        payload = json.dumps({'status': 'error', 'message': '' + str(e)})
        print("3. Dump.har uploading is failed. " + str(payload))

        return False

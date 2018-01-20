import os


def _get_platform():
    platform = os.getenv('PLATFORM') or (
        'android' if os.getenv('ANDROID_HOME') else 'ios')

    if platform.lower() == 'android':
        return 'Android'
    else:
        return 'iOS'

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

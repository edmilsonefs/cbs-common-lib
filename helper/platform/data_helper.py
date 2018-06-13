# -*- coding: utf-8 -*-
import os
import re
PROJECT_ID = os.getenv('testlio_project_id')
BASE_API_URL = 'https://api.testlio.com'
BASE_PLATFORM_URL = 'https://platform.testlio.com'


def unify_string(phrase):
    sum = 0
    line = ''
    final_string = ''
    for c in phrase:
        sum += ord(c)
        line += str(ord(c))

    checksum = str(long(long(line) / sum))

    counter = 0
    temp_string = ''
    for c in checksum:
        counter += 1
        temp_string += str(c)
        if counter == 2:
            val = int(temp_string) if int(temp_string) >= 33 else 33 + int(temp_string)
            final_string += chr(val)
            temp_string = ''
            counter = 0

    return re.sub('[^0-9a-zA-Z]+', '', final_string)

import json


def parse_response_to_set(response):
    list_result = set()

    if len(str(response)) > 0:
        json_result = json.loads(response, encoding='utf=8')
        for level1 in json_result:
            arr_level1 = json_result[level1]
            for level2 in arr_level1:
                for level3 in level2:
                    level3['profile'] = level1
                    list_result.add(json.dumps(level3))

    return list_result

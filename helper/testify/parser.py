import json


def parse_response_to_set(response):
    json_result = json.loads(response, encoding='utf=8')
    list_result = set()
    for level1 in json_result:
        arr_level1 = json_result[level1]
        for level2 in arr_level1:
            for level3 in level2:
                list_result.add(json.dumps(level3))

    return list_result

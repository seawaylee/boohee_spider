# -*- coding: utf-8 -*-
from collections import defaultdict

from flask import json


class DataTransfer:
    def __init__(self):
        pass

    @staticmethod
    def group_by_category():
        food_details = get_food_details()
        group_map = defaultdict(list)
        for food_detail in food_details:
            food_group_name = food_detail['basic_info']['food_group_name']
            group_map[food_group_name].append(food_detail)

        total_count = 0
        for group_name, group_content in group_map.items():
            save_food_by_group(group_name, group_content)
            # print group_name, len(group_content)
            total_count += len(group_content)
        print 'total_count', total_count


def get_food_details():
    return json.loads(open('/Users/lixiwei-mac/Documents/IdeaProjects/rhinotech_spider/boohee_spider/boohee/food_detail.json').read())


def save_food_by_group(group_name, group_content):
    with open('/Users/lixiwei-mac/Documents/IdeaProjects/rhinotech_spider/boohee_spider/boohee/groups/' + group_name.encode('utf-8'), 'wb+') as f:
        f.write('[')
        for food_index, food_detail in enumerate(group_content):
            f.write(json.dumps(food_detail))
            if food_index != len(group_content) - 1:
                f.write(',\n')
                # print json.dumps(food_detail)
        f.write(']')


if __name__ == '__main__':
    DataTransfer.group_by_category()

# -*- coding: utf-8 -*-
import codecs
import csv
from collections import defaultdict

from flask import json


class DataTransfer:
    def __init__(self):
        pass

    @staticmethod
    def group_by_category():
        food_details = get_food_details()
        group_map = get_grouped_food_details(food_details)

        total_count = 0
        for group_name, group_content in group_map.items():
            save_food_by_group(group_name, group_content)
            # print group_name, len(group_content)
            total_count += len(group_content)
        print 'total_count', total_count

    @staticmethod
    def trans_json_to_csv():
        food_details = get_food_details()
        group_map = get_grouped_food_details(food_details)
        food_names = get_all_food_names(food_details)
        for group_name, group_content in group_map.items():
            if '菜' not in group_name.encode('utf-8'):
                print '================', group_name, '================'
                with open('/Users/lixiwei-mac/Documents/IdeaProjects/rhinotech_spider/boohee_spider/boohee/csv/others/' + group_name + '.csv', mode='wb+') as data_file:
                    data_file.write(codecs.BOM_UTF8)
                    csv_writer = csv.writer(data_file)
                    csv_writer.writerow(['名称', '分类', '评价', '红绿灯地址', '热量', '碳水化合物', '脂肪',
                                         '蛋白质', '纤维素', '维生素A', '维生素C', '维生素E', '胡萝卜素',
                                         '硫胺素', '核黄素', '烟酸', '胆固醇', '镁', '钙', '铁', '锌', '铜', '锰', '钾', '磷', '钠', '硒',
                                         '度量单位', '相关食物'])
                    for food_obj in group_content:
                        print food_obj['basic_info']['food_name'], food_obj['href']
                        nutrition_dict = {}
                        for nutrition_obj in food_obj['nutrition_info']:
                            nutrition_dict[nutrition_obj.keys()[0]] = nutrition_obj.values()[0]
                        col_array = [
                            food_obj['basic_info']['food_name'].encode('utf-8'),
                            food_obj['basic_info']['food_group_name'].encode('utf-8'),
                            food_obj['basic_info']['evaluation'].encode('utf-8'),
                            food_obj['basic_info']['traffic_light_img_href'].encode('utf-8'),
                            food_obj['basic_info']['calories_value'].encode('utf-8'),
                            nutrition_dict[u'碳水化合物(克)'].encode('utf-8') if nutrition_dict.has_key(u'碳水化合物(克)') else '',
                            nutrition_dict[u'脂肪(克)'].encode('utf-8') if nutrition_dict.has_key(u'脂肪(克)') else '',

                            nutrition_dict[u'蛋白质(克)'].encode('utf-8') if nutrition_dict.has_key(u'蛋白质(克)') else '',
                            nutrition_dict[u'纤维素(克)'].encode('utf-8') if nutrition_dict.has_key(u'纤维素(克)') else '',
                            nutrition_dict[u'维生素A(微克)'].encode('utf-8') if nutrition_dict.has_key(u'维生素A(微克)') else '',
                            nutrition_dict[u'维生素C(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'维生素C(毫克)') else '',
                            nutrition_dict[u'维生素E(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'维生素E(毫克)') else '',

                            nutrition_dict[u'胡萝卜素(微克)'].encode('utf-8') if nutrition_dict.has_key(u'胡萝卜素(微克)') else '',

                            nutrition_dict[u'硫胺素(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'硫胺素(毫克)') else '',
                            nutrition_dict[u'核黄素(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'核黄素(毫克)') else '',
                            nutrition_dict[u'烟酸(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'烟酸(毫克)') else '',
                            nutrition_dict[u'胆固醇(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'胆固醇(毫克)') else '',
                            nutrition_dict[u'镁(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'镁(毫克)') else '',
                            nutrition_dict[u'钙(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'钙(毫克)') else '',
                            nutrition_dict[u'铁(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'铁(毫克)') else '',
                            nutrition_dict[u'锌(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'锌(毫克)') else '',
                            nutrition_dict[u'铜(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'铜(毫克)') else '',
                            nutrition_dict[u'锰(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'锰(毫克)') else '',
                            nutrition_dict[u'钾(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'钾(毫克)') else '',
                            nutrition_dict[u'磷(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'磷(毫克)') else '',
                            nutrition_dict[u'钠(毫克)'].encode('utf-8') if nutrition_dict.has_key(u'钠(毫克)') else '',
                            nutrition_dict[u'硒(微克)'].encode('utf-8') if nutrition_dict.has_key(u'硒(微克)') else '',

                            json.dumps([k + v for item in food_obj['widget_unit_info'] for k, v in item.items()]).decode('unicode-escape').encode('utf-8'),
                            json.dumps([x for x in food_obj['relative_foods_info'] if x.encode('utf-8') in food_names]).decode('unicode-escape').encode('utf-8')

                        ]
                        csv_writer.writerow(col_array)
            else:
                print '================', group_name, '================'
                with open('/Users/lixiwei-mac/Documents/IdeaProjects/rhinotech_spider/boohee_spider/boohee/csv/dishes/' + group_name + '.csv', mode='wb+') as data_file:
                    data_file.write(codecs.BOM_UTF8)
                    csv_writer = csv.writer(data_file)
                    csv_writer.writerow(['名称', '分类', '烹饪工艺', '红绿灯地址', '热量', '碳水化合物', '脂肪',
                                         '蛋白质', '纤维素',
                                         '度量单位',
                                         '主料', '辅料', '调料', '做法',
                                         '相关食物'])

                    for food_obj in group_content:
                        print food_obj['basic_info']['food_name'], food_obj['href']
                        nutrition_dict = {}
                        for nutrition_obj in food_obj['nutrition_info']:
                            nutrition_dict[nutrition_obj.keys()[0]] = nutrition_obj.values()[0]
                        col_array = [
                            food_obj['basic_info']['food_name'].encode('utf-8'),
                            food_obj['basic_info']['food_group_name'].encode('utf-8'),
                            food_obj['basic_info']['cooking_type_detail'].encode('utf-8'),
                            food_obj['basic_info']['traffic_light_img_href'].encode('utf-8'),
                            food_obj['basic_info']['calories_value'].encode('utf-8'),
                            nutrition_dict[u'碳水化合物(克)'].encode('utf-8') if nutrition_dict.has_key(u'碳水化合物(克)') else '',
                            nutrition_dict[u'脂肪(克)'].encode('utf-8') if nutrition_dict.has_key(u'脂肪(克)') else '',

                            nutrition_dict[u'蛋白质(克)'].encode('utf-8') if nutrition_dict.has_key(u'蛋白质(克)') else '',
                            nutrition_dict[u'纤维素(克)'].encode('utf-8') if nutrition_dict.has_key(u'纤维素(克)') else '',

                            json.dumps([k + v for item in food_obj['widget_unit_info'] for k, v in item.items()]).decode('unicode-escape').encode('utf-8'),
                            json.dumps(food_obj['material_info']['major_material_info']).decode('unicode-escape').encode('utf-8'),
                            json.dumps(food_obj['material_info']['supplementary_material_info']).decode('unicode-escape').encode('utf-8'),
                            json.dumps(food_obj['material_info']['seasoning_info']).decode('unicode-escape').encode('utf-8'),
                            json.dumps(food_obj['production_method']).decode('unicode-escape').encode('utf-8'),

                            json.dumps([x for x in food_obj['relative_foods_info'] if x in food_names]).decode('unicode-escape').encode('utf-8')

                        ]
                        csv_writer.writerow(col_array)
                        # break


def get_all_food_names(food_details):
    food_names = set()
    for food in get_food_details():
        food_names.add(food['basic_info']['food_name'].encode('utf-8'))
    return food_names


def get_grouped_food_details(food_details):
    group_map = defaultdict(list)
    for food_detail in food_details:
        food_group_name = food_detail['basic_info']['food_group_name']
        group_map[food_group_name].append(food_detail)
    return group_map


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
    # DataTransfer.group_by_category()
    DataTransfer.trans_json_to_csv()

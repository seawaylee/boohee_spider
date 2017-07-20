#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import time

from flask import json

food_names = json.loads(open('food_name.json').read())
food_details = json.loads(open('food_detail_backup.json').read())


class FoodDetailSpider(scrapy.Spider):
    name = 'food_detail'
    tmp_start_urls = ['http://www.boohee.com' + food_name_obj['href'] for food_name_obj in food_names]
    start_urls = []
    total_urls = []
    already_saved_urls = []

    def __init__(self):
        for obj in food_names:
            self.total_urls.append('http://www.boohee.com' + obj['href'])
        for obj in food_details:
            self.already_saved_urls.append(obj['href'])
        self.start_urls = list(set(self.total_urls) - set(self.already_saved_urls))
        # for url in self.start_urls:
        #     print url
        # print len(self.start_urls)
        # start_urls = ['http://www.boohee.com/shiwu/hualiuniuroupian']

    def parse(self, response):
        continue_flag = True
        for obj in food_details:
            if obj['href'] == response.url:
                continue_flag = False
        if continue_flag:
            source = response.css('div.widget-source p.source::text').extract_first()
            if '用户上传' in source.encode('utf-8'):
                print "=================用户的垃圾================="
            else:
                basic_info = {}
                basic_info['calories_value'] = response.css('ul.basic-infor').xpath('//li/span/span/text()').extract_first()
                basic_info['food_name'] = response.css('h2.crumb::text').extract()[-1].split("/")[-1].strip()
                basic_info['food_group_name'] = response.xpath('//h2/a/text()').extract()[1]
                basic_info['traffic_light_img_href'] = response.css('ul.basic-infor img::attr(src)').extract_first()
                cooking_type = response.css('div.widget-food-detail div.content p b::text').extract_first()
                if cooking_type:
                    if '评价' in cooking_type.encode('utf-8'):
                        basic_info['evaluation'] = cooking_type + response.css('div.widget-food-detail div.content p::text').extract()[1]
                    else:
                        basic_info['cooking_type_detail'] = cooking_type + response.css('div.widget-food-detail div.content p::text').extract()[1]

                # nutrition infomation
                nutrition_info = []
                for nutr_dl in response.css('div.nutr-tag dl')[1:]:
                    for nutr_dd in nutr_dl.css('dd'):
                        nutr_key = nutr_dd.css('span.dt::text').extract_first()
                        if nutr_dd.css('span.stress'):
                            nutr_value = nutr_dd.css('span.stress::text').extract_first()
                        else:
                            nutr_value = nutr_dd.css('span.dd::text').extract_first()
                        # print nutr_key, nutr_value
                        nutrition_info.append({nutr_key: nutr_value})

                # widget-unit

                widget_unit_info = []
                for w_u_tr in response.css('div.widget-unit tbody tr'):
                    if w_u_tr.css('td a'):
                        w_u_name = w_u_tr.css('td a::text').extract()[0]
                        w_u_value = w_u_tr.css('td a::text').extract()[1]
                    elif w_u_tr.css('td span'):
                        w_u_name = w_u_tr.css('td span::text').extract()[0]
                        w_u_value = w_u_tr.css('td span::text').extract()[1]
                    else:
                        w_u_name = w_u_tr.css('td::text').extract()[0]
                        w_u_value = w_u_tr.css('td::text').extract()[1]
                    # print w_u_name, w_u_value
                    widget_unit_info.append({w_u_name: w_u_value})

                # widget-more
                material_info = {'major_material_info': [], 'supplementary_material_info': [], 'seasoning_info': []}
                for material_index, material_type in enumerate(response.css('div.widget-more h3::text').extract()):
                    # print material_index, material_type
                    if '做法' not in material_type.encode('utf-8'):
                        material_name_list = response.css('div.widget-more ul')[material_index].css('li a::text').extract()
                        material_unit_list = response.css('div.widget-more ul')[material_index].css('li::text').extract()
                        for sub_material_index in range(len(material_name_list)):
                            sub_material_info = material_name_list[sub_material_index] + material_unit_list[sub_material_index]
                            if material_type in [u'主料', u'原料']:
                                material_info['major_material_info'].append(sub_material_info)
                            elif material_type == u'辅料':
                                material_info['supplementary_material_info'].append(sub_material_info)
                            elif material_type == u'调料':
                                material_info['seasoning_info'].append(sub_material_info)

                production_method = response.css('div.widget-more p::text').extract()

                # widget-relative
                relative_foods_info = []
                relative_foods_info = response.css('div.widget-relative li a span::text').extract()

                # time.sleep(1)
                # print json.dumps({'source': source, 'basic_info': basic_info, 'nutrition_info': nutrition_info, 'widget_unit_info': widget_unit_info, 'material_info': material_info, 'production_method': production_method, 'relative_foods_info': relative_foods_info}).replace(" ", "")
                yield {'source': source, 'href': response.url, 'basic_info': basic_info, 'nutrition_info': nutrition_info, 'widget_unit_info': widget_unit_info, 'material_info': material_info, 'production_method': production_method, 'relative_foods_info': relative_foods_info}

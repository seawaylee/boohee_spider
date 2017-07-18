import scrapy
import time

from flask import json

file_res = json.loads(open('/Users/lixiwei-mac/Documents/IdeaProjects/rhinotech_spider/boohee_spider/boohee/food_name.json').read())
cookie = 'gwdang_brwext_share=0; from_device=default; gwdang_brwext_more_force=0; history=1479334-223%2C2365144-3%2C1462046326-3%2C12596075384-3%2C2365148-3%2C2365158-3%2C4830462-3%2C3498623-3%2C2504829-3%2C11905178-3; gwdang_permanent_id=9b26f59a3e854641cafe23c267ea728b; gwdang_brwext_is_open=0; gwdang_brwext_first=1; gwdang_brwext_position=0; gwdang_brwext_close_update=0; gwdang_brwext_close_update_hour=0; gwdang_brwext_close_install=0; gwdang_brwext_style=top; gwdang_brwext_notice=0; gwdang_brwext_fold=0; gwdang_brwext_show_tip=1; gwdang_brwext_imageAd=1; gwdang_brwext_show_popup=1; gwdang_brwext_show_ljfqrcode=1; gwdang_brwext_hide_shoptip=0; gwdang_brwext_apptg_close=0; gwdang_brwext_show_lowpri=1; gwdang_brwext_show_guessfavor=1; gwdang_brwext_show_lowpri_right=1; gwdang_brwext_show_guessfavor_right=1; gwdang_brwext_show_vips=1; gwdang_brwext_show_wishlist=1; gwdang_brwext_show_guess=1; gwdang_brwext_show_promo=1; gwdang_search_way=0'
headers = {'Cookie':cookie}

class FoodNameSpider(scrapy.Spider):
    name = 'food_name'
    base_url = 'http://www.boohee.com/food/group/%s'
    start_urls = [base_url % x for x in range(41)] * 10

    def parse(self, response):
        for food_ref in response.css('ul.food-list li h4 a::attr(href)').extract():
            group_id = response.url.split('/')[5].split("?")[0]
            food_name = response.xpath('//a[@href="%s"]/@title' % food_ref).extract_first()
            res = {'group_id': group_id, 'href': food_ref, 'food_name': food_name}
            if res not in file_res:
                yield res
        for href in response.css('a.next_page'):
            time.sleep(0.1)
            yield response.follow(href, self.parse, headers=headers)

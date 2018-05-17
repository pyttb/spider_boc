# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy
from scrapy import Selector

from creditchina_project.wdzj_items import WdzjLoaderItem,WdzjResultItem

reload(sys)
sys.setdefaultencoding('utf-8')
class Tianyancha(scrapy.Spider):
    name = "tianyancha"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.tianyancha.com']
    names=['360','智慧农业']
    default_data = {
    }
    default_headers = {

    }
    def start_requests(self):
        for name in self.names:
            yield scrapy.Request(url='https://www.tianyancha.com/search?key='+name, headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), callback=self.parse_basic_info, dont_filter=True)

    def parse_basic_info(self, response):
        basic_info = response.text
        print basic_info

    def parse_city_info(self, response):
        basic_info = response.text
        city_name = response.meta['city_name']
        neighborhoods = Selector(text=basic_info).xpath('//div[@class="leftContent"]//ul[@class="listContent"]//li[@class="clear xiaoquListItem"]').extract()
        for neighborhood in neighborhoods:
            neighborhood_url = Selector(text=neighborhood).xpath('//li[@class="clear xiaoquListItem"]/a/@href').extract()[0]

    def closed(self, reason):
        '''
        爬虫结束时退出登录状态
        :param reason:
        :return:
        '''
        if 'finished' == reason:
            logging.warning('%s', '爬虫程序执行结束，即将关闭')
        elif 'shutdown' == reason:
            logging.warning('%s', '爬虫进程被强制中断，即将关闭')
        elif 'cancelled' == reason:
            logging.warning('%s', '爬虫被引擎中断，即将关闭')
        else:
            logging.warning('%s', '爬虫被未知原因打断，即将关闭')
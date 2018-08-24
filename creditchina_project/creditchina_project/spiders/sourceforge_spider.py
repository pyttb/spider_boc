# -*- coding: utf-8 -*-
import datetime
import json
import logging
import sys
import urllib
from urlparse import urlparse

import scrapy
from scrapy import Selector

from creditchina_project.lianjia_items import LianjiaLoaderItem, LianjiaResultItem

reload(sys)
sys.setdefaultencoding('utf-8')
class SourceForge(scrapy.Spider):
    name = "sourceforge"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['sourceforge.net']
    default_data = {
    }
    default_headers = {

    }
    def start_requests(self):
        yield scrapy.Request(url='https://sourceforge.net/directory/os:windows/os:mac/os:linux/?q=windows', headers=self.default_headers,
                             body=urllib.urlencode(self.default_data), callback=self.parse_basic_info, dont_filter=True)

    def parse_basic_info(self, response):
        basic_info = response.text
        projects=Selector(text=basic_info).xpath('//ul[@class="projects"]/li[@itemprop="itemListElement"]').extract()
        for project in projects:
            url = 'https://sourceforge.net' + Selector(text=project).xpath('//li[@itemprop="itemListElement"]/div[@class="result-heading"]/div[@class="result-heading-texts"]/a/@href').extract()[0]
            title = Selector(text=project).xpath('//li[@itemprop="itemListElement"]/div[@class="result-heading"]/div[@class="result-heading-texts"]/a/h2/text()').extract()[0]
            print url,title
        has_next=Selector(text=basic_info).xpath('//ul[@class="pagination text-center"]/li[@class="pagination-next disabled"]').extract()
        if len(has_next) > 0:
            return
        next = 'https://sourceforge.net' + Selector(text=basic_info).xpath('//li[@class="pagination-next "]/a/@href').extract()[0]
        yield scrapy.Request(url=next, headers=self.default_headers, body=urllib.urlencode(self.default_data), callback=self.parse_basic_info, dont_filter=True)


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
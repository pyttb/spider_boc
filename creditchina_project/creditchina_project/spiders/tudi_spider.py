# -*- coding: utf-8 -*-
import random
import time
from datetime import datetime
import pandas as pd

import scrapy
import re
from scrapy.http import Request
from scrapy.http import FormRequest
from bs4 import BeautifulSoup

from creditchina_project.tudi_items import TudiResultItem, TudiLoaderItem
from ..settings import SPIDER_START_DATE, SPIDER_END_DATE


class TudiEndSpider(scrapy.Spider):
    name = 'tudi'

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        # 'DOWNLOADER_MIDDLEWARES' : {
        # 'creditchina_project.middlewares.RandomUserAgent': 100,
        # },
        'ITEM_PIPELINES': {
             'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        },
    }
    batch_date = datetime.now().date()
    allowed_domains = ['www.landchina.com']
    start_urls = ['http://www.landchina.com/default.aspx?tabid=263&ComName=default']

    start_date = SPIDER_START_DATE
    end_date = SPIDER_END_DATE

    def datelist(self, beginDate, endDate):
        date_l = [datetime.strftime(x, '%Y-%#m-%#d') for x in list(pd.date_range(start=beginDate, end=endDate))]
        return date_l
    def start_requests(self):
        for dt in self.datelist(self.start_date, self.end_date):
            time.sleep(random.uniform(5, 10))
            spider_date = '9f2c3acd-0256-4da2-a659-6949c4671a2a:' + str(dt) + '~' + str(dt)
            yield scrapy.FormRequest(
                url='http://www.landchina.com/default.aspx?tabid=263&ComName=default',
                formdata={'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                                                       'TAB_QuerySubmitConditionData': spider_date,
                                                       'TAB_QuerySubmitPagerData': '1'},
            meta={'spider_date':spider_date} ,callback=self.parse_page)


    def parse_page(self, response):
        spider_date=response.meta['spider_date']
        urldomain = 'http://www.landchina.com/'
        bs = BeautifulSoup(response.text, 'lxml')
        info_list = bs.select('tr[class=gridItem],tr[class=gridAlternatingItem]')
        for info in info_list:
            item = TudiLoaderItem(item=TudiResultItem(), response=response)
            item.add_value('batch_date', self.batch_date)
            item.add_value('ordnum', re.sub(r'(\d)\.',r'\1',info.find_all('td')[0].text.strip()))
            full_url=urldomain + info.a['href']
            item.add_value('totalUrl', full_url)
            yield Request(url=full_url, meta={'item': item}, callback=self.parse_item, dont_filter=True)

        nowpage = response.xpath('//td[@class="pager"][2]/input[1]/@value').extract()[0]
        nextpage = int(nowpage) + 1
        str_nextpage = str(nextpage)
        nextLink = response.xpath('//tr/td[@class="pager"][2]/a[last()-1]/@onclick').extract()
        if len(nextLink):
            yield scrapy.FormRequest(
            url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default',formdata={
                                                               'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                                                               'TAB_QuerySubmitConditionData': spider_date,
                                                               'TAB_QuerySubmitPagerData': str_nextpage
                                                           },
                callback=self.parse_page,dont_filter=True
            )

    def parse_item(self, response):
        item = response.meta['item']
        try:
            item.add_value('country', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('country', '')
        try:
            item.add_value('num', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('num', '')
        try:
            item.add_value('myname', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('myname', '')
        try:
            item.add_value('address', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('address', '')
        try:
            item.add_value('area', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('area', '')
        try:
            item.add_value('myuse', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('myuse', '')
        try:
            item.add_value('way', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('way', '')
        try:
            item.add_value('price', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('price', '')
        try:
            item.add_value('person', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('person', '')
        try:
            item.add_value('start', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('start', '')
        try:
            item.add_value('finish', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('finish', '')
        try:
            item.add_value('compact', response.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl"]/text()').extract()[0])
        except Exception as e:
            item.add_value('compact', '')
        item.add_value('table_name', 'SPIDER.TUDI_RESULT')
        yield item.load_item()

# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from scrapy.http import FormRequest
from aqsiq_project.items import *
from bs4 import BeautifulSoup
from ..settings import SPIDER_DATE


class TudiEndSpider(scrapy.Spider):
    name = 'tudi'

    custom_settings = {
        'DOWNLOAD_DELAY' : 2,
        'DOWNLOADER_MIDDLEWARES' : {
        'aqsiq_project.middlewares.RandomUserAgent': 100,
        },
        'ITEM_PIPELINES': {
            'aqsiq_project.pipelines.MysqlPipeline': 100,
        },
    }

    allowed_domains = ['www.landchina.com']
    start_urls = ['http://www.landchina.com/default.aspx?tabid=263&ComName=default']

    date = SPIDER_DATE
    spider_date = '9f2c3acd-0256-4da2-a659-6949c4671a2a:' + date

    def start_requests(self):

        yield scrapy.FormRequest(
            url='http://www.landchina.com/default.aspx?tabid=263&ComName=default',
            formdata={'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                                                       'TAB_QuerySubmitConditionData': self.spider_date,
                                                       'TAB_QuerySubmitPagerData': '1'},
            callback=self.parse_page)

    def parse_page(self, response):
        urldomain = 'http://www.landchina.com/'
        bs = BeautifulSoup(response.text, 'lxml')
        info_list = bs.select('tr[class=gridItem],tr[class=gridAlternatingItem]')

        for info in info_list:
            item = TudiResultItem()
            item['ordnum'] = re.sub(r'(\d)\.',r'\1',info.find_all('td')[0].text.strip())
            full_url=urldomain + info.a['href']
            item['totalUrl']=full_url
            print(full_url)

            yield Request(url=full_url, meta={'item': item}, callback=self.parse_item, dont_filter=True)

        nowpage = response.xpath('//td[@class="pager"][2]/input[1]/@value').extract()[0]
        print('------当前页',nowpage)
        nextpage = int(nowpage) + 1
        str_nextpage = str(nextpage)
        nextLink = response.xpath('//tr/td[@class="pager"][2]/a[last()-1]/@onclick').extract()
        if len(nextLink):
            yield scrapy.FormRequest(
            url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default',formdata={
                                                               'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                                                               'TAB_QuerySubmitConditionData': self.spider_date,
                                                               'TAB_QuerySubmitPagerData': str_nextpage
                                                           },
                callback=self.parse_page,dont_filter=True
            )

    def parse_item(self, response):
        item = response.meta['item']
        try:
            item['country'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl"]/text()').extract()[0] #extract_first()
        except Exception as e:
            item['country'] = 'None'
        try:
            item['num'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['num'] = 'None'
        try:
            item['myname'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['myname'] = 'None'
        try:
            item['address'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['address'] = 'None'
        try:
            item['area'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['area'] = 'None'
        try:
            item['myuse'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['myuse'] = 'None'
        try:
            item['way'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['way'] = 'None'
        try:
            item['price'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['price'] = 'None'
        try:
            item['person'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['person'] = 'None'
        try:
            item['start'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['start'] = 'None'
        try:
            item['finish'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['finish'] = 'None'
        try:
            item['compact'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['compact'] = 'None'
        yield item
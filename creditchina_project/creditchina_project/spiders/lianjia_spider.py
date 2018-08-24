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
class Lianjia(scrapy.Spider):
    name = "lianjia"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.lianjia.com']
    default_data = {
    }
    default_headers = {

    }
    def start_requests(self):
        yield scrapy.Request(url='https://bj.lianjia.com/', headers=self.default_headers,
                             body=urllib.urlencode(self.default_data), callback=self.parse_cities_info, dont_filter=True)

    def parse_cities_info(self, response):
        basic_info = response.text
        cities=[]
        for idx in range(0,len(Selector(text=basic_info).xpath('//div[@class="fc-main clear"]//a/@href').extract())):
            cities.append(
                {'url': Selector(text=basic_info).xpath(
                    '//div[@class="fc-main clear"]//a/@href').extract()[idx],
                 'name': Selector(text=basic_info).xpath(
                     '//div[@class="fc-main clear"]//a/text()').extract()[idx]
                 }
            )
        # cities=cities[0:2]
        allowed_cities=['https://sh.lianjia.com/']
        for city in cities:
            if city['url'] not in allowed_cities:
                continue
            yield scrapy.Request(url=city['url']+'xiaoqu/', headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), meta={'city_name':city['name']} ,callback=self.parse_district_info, dont_filter=True)

    def parse_district_info(self, response):
        url = response.url
        basic_info = response.text
        city_name = response.meta['city_name']
        districts = Selector(text=basic_info).xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for district in districts:
            parsed_uri = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            yield scrapy.Request(url=domain+district, headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), meta={'city_name':city_name} ,callback=self.parse_downtown_info, dont_filter=True)

    def parse_downtown_info(self, response):
        url = response.url
        basic_info = response.text
        city_name = response.meta['city_name']
        downtowns = Selector(text=basic_info).xpath('//div[@data-role="ershoufang"]/div[2]/a/@href').extract()
        for downtown in downtowns:
            parsed_uri = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
            yield scrapy.Request(url=domain+downtown, headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), meta={'city_name':city_name} ,callback=self.parse_page_info, dont_filter=True)

    def parse_page_info(self, response):
        url = response.url
        basic_info = response.text
        city_name = response.meta['city_name']
        pages=0
        if len(Selector(text=basic_info).xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract())>0:
            pages=json.loads(Selector(text=basic_info).xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0])['totalPage']
        for page in range(1,pages+1):
            real_url=url
            if page>1:
                real_url=real_url+'pg'+str(page)+'/'
            yield scrapy.Request(url=real_url, headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), meta={'city_name':city_name} ,callback=self.parse_item_info, dont_filter=True)

    def parse_item_info(self, response):
        basic_info = response.text
        city_name = response.meta['city_name']
        neighborhoods = Selector(text=basic_info).xpath('//div[@class="leftContent"]//ul[@class="listContent"]//li[@class="clear xiaoquListItem"]').extract()
        for neighborhood in neighborhoods:
            neighborhood_url = Selector(text=neighborhood).xpath('//li[@class="clear xiaoquListItem"]/a/@href').extract()[0]
            yield scrapy.Request(url=neighborhood_url, headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), meta={'city_name': city_name},
                                 callback=self.parse_neighborhood_info, dont_filter=True)

    def parse_neighborhood_info(self, response):
        basic_info = response.text
        city_name = response.meta['city_name']
        block_name = '>'.join(Selector(text=basic_info).xpath('//div[@class="xiaoquDetailbreadCrumbs"]/div[@class="fl l-txt"]/a/text()').extract())
        neighborhood_name=''
        if len(Selector(text=basic_info).xpath('//div[@class="xiaoquDetailHeader"]/div[@class="xiaoquDetailHeaderContent clear"]/div[@class="detailHeader fl"]/h1[@class="detailTitle"]/text()').extract())>0:
            neighborhood_name = Selector(text=basic_info).xpath('//div[@class="xiaoquDetailHeader"]/div[@class="xiaoquDetailHeaderContent clear"]/div[@class="detailHeader fl"]/h1[@class="detailTitle"]/text()').extract()[0]
        neighborhood_addr = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquDetailHeader"]/div[@class="xiaoquDetailHeaderContent clear"]/div[@class="detailHeader fl"]/div[@class="detailDesc"]/text()').extract()[0]
        neighborhood_price = ''
        if len(Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquPrice clear"]//span[@class="xiaoquUnitPrice"]/text()').extract())>0:
            neighborhood_price = Selector(text=basic_info).xpath(
                '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquPrice clear"]//span[@class="xiaoquUnitPrice"]/text()').extract()[0]
        neighborhood_year = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][1]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        neighborhood_type = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][2]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        neighborhood_estate = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][3]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        neighborhood_property = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][4]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        neighborhood_company = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][5]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        neighborhood_builds = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][6]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        neighborhood_houses = Selector(text=basic_info).xpath(
            '//div[@class="xiaoquOverview"]/div[@class="xiaoquDescribe fr"]/div[@class="xiaoquInfo"]/div[@class="xiaoquInfoItem"][7]/span[@class="xiaoquInfoContent"]/text()').extract()[0]
        item = LianjiaLoaderItem(item=LianjiaResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        item.add_value('city_name', city_name)
        item.add_value('block_name', block_name)
        item.add_value('neighborhood_name', neighborhood_name)
        item.add_value('neighborhood_addr', neighborhood_addr)
        item.add_value('neighborhood_price', neighborhood_price)
        item.add_value('neighborhood_year', neighborhood_year)
        item.add_value('neighborhood_type', neighborhood_type)
        item.add_value('neighborhood_estate', neighborhood_estate)
        item.add_value('neighborhood_property', neighborhood_property)
        item.add_value('neighborhood_company', neighborhood_company)
        item.add_value('neighborhood_builds', neighborhood_builds)
        item.add_value('neighborhood_houses', neighborhood_houses)
        item.add_value('table_name', 'spider.lianjia_result')
        yield item.load_item()

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
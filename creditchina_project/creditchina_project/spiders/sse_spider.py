# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy
from scrapy import Selector

from creditchina_project.sse_items import SseLoaderItem, SseResultItem

reload(sys)
sys.setdefaultencoding('utf-8')
class SseSpider(scrapy.Spider):
    name = "sse"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.sse.com.cn']
    default_data = {
    }
    default_headers = {

    }

    def start_requests(self):
        for url in ['http://www.sse.com.cn/disclosure/credibility/bonds/disposition/s_index.htm','http://www.sse.com.cn/disclosure/credibility/bonds/disposition/s_index_2.htm']:
            yield scrapy.Request(url=url, headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), callback=self.parse_basic_info,
                                 dont_filter=True)

    def parse_basic_info(self, response):
        contents = response.xpath('//div[@class="table_inline_wrap  tdclickable"]/table[@class="table"]/tbody//tr').extract()
        for content in contents:
            security_code = Selector(text=content).xpath('//tr/td[1]/text()').extract()[0]
            security_nick = Selector(text=content).xpath('//tr/td[2]/text()').extract()[0]
            security_url = 'http://www.sse.com.cn'+Selector(text=content).xpath('//tr/td[3]//a/@href').extract()[0]
            party_name = Selector(text=content).xpath('//tr/td[3]//a/@title').extract()[0]
            pub_date = Selector(text=content).xpath('//tr/td[4]/text()').extract()[0]
            if security_url.endswith('doc'):
                item = SseLoaderItem(item=SseResultItem(), response=response)
                item.add_value('batch_date', self.batch_date)
                item.add_value('security_code', security_code)
                item.add_value('security_nick', security_nick)
                item.add_value('pub_date', pub_date)
                item.add_value('party_name', party_name)
                item.add_value('table_name', 'spider.sse_result')
                yield item.load_item()
            else:
                yield scrapy.Request(url=security_url, headers=self.default_headers,
                                     body=urllib.urlencode(self.default_data), callback=self.parse_detail_info, meta={'security_code':security_code,'security_nick':security_nick,'pub_date':pub_date}, dont_filter=True)

    def parse_detail_info(self, response):
        security_code=response.meta['security_code']
        security_nick = response.meta['security_nick']
        pub_date = response.meta['pub_date']
        writ_no=''
        party_name=''
        pub_type=''
        if not response.xpath('//div[@class="allZoom"]//p[1]//text()').extract()[0].startswith('当事人'):
            writ_no = ''.join(response.xpath('//div[@class="allZoom"]//p[1]//text()').extract())
            party_name = response.xpath('//div[@class="allZoom"]//p[3]//text()').extract()[0]
        else:
            party_name = response.xpath('//div[@class="allZoom"]//p[2]//text()').extract()[0]
        party_name=party_name.replace('；','').replace('。','').strip()
        texts=response.xpath('//div[@class="allZoom"]//p//text()').extract()
        for text in texts:
            if text.find('本所做出如下纪律处分决定：')>0:
                pub_type = text.split('本所做出如下纪律处分决定：')[1]
        item = SseLoaderItem(item=SseResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        item.add_value('security_code', security_code)
        item.add_value('security_nick', security_nick)
        item.add_value('pub_date', pub_date)
        item.add_value('writ_no', writ_no)
        item.add_value('party_name', party_name)
        item.add_value('pub_type', pub_type)
        item.add_value('table_name', 'spider.sse_result')
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
# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy
from scrapy import Selector

from creditchina_project.csrc_items import CsrcResultItem, CsrcLoaderItem

reload(sys)
sys.setdefaultencoding('utf-8')
class CsrcSpider(scrapy.Spider):
    name = "csrc"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.csrc.gov.cn']
    default_data = {
    }
    default_headers = {
    }

    def start_requests(self):
        for page in range(0,54):
            url=''
            if page==0:
                url = 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401.htm'
            else:
                url = 'http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401_'+str(page)+'.htm'
            yield scrapy.Request(url=url, headers=self.default_headers, body=urllib.urlencode(self.default_data), callback=self.parse_basic_info, dont_filter=True)

    def parse_basic_info(self, response):
        contents = response.xpath('//div[@id="documentContainer"]/div[@class="row"]').extract()
        for content in contents:
            company_name = Selector(text=content).xpath('//div[@class="row"]/li[@class="mc"]/div/a/text()').extract()[0]
            company_url = 'http://www.csrc.gov.cn/pub/zjhpublic'+Selector(text=content).xpath('//div[@class="row"]/li[@class="mc"]/div/a/@href').extract()[0][5:]
            writ_no = Selector(text=content).xpath('//div[@class="row"]/li[@class="wh"]/text()').extract()[0]
            writ_date = Selector(text=content).xpath('//div[@class="row"]/li[@class="fbrq"]/text()').extract()[0]
            yield scrapy.Request(url=company_url, headers=self.default_headers, body=urllib.urlencode(self.default_data), meta={'company_name':company_name,'writ_no':writ_no,'writ_date':writ_date},
                                 callback=self.parse_detail_info, dont_filter=True)

    def parse_detail_info(self, response):
        company_name=response.meta['company_name']
        writ_no = response.meta['writ_no']
        writ_date = response.meta['writ_date']
        pub_content=''
        contents = response.xpath('//div[@id="ContentRegion"]/div[@class="content"]/p[@class="p0"]/span//text()').extract()
        is_pub_content=False
        for content in contents:
            if not is_pub_content and content.find('我会决定')>0:
                is_pub_content=True
                continue
            if is_pub_content:
                pub_content=pub_content+content.strip()
        item = CsrcLoaderItem(item=CsrcResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        item.add_value('company_name', company_name)
        item.add_value('writ_no', writ_no)
        item.add_value('writ_date', writ_date)
        item.add_value('pub_content', pub_content)
        item.add_value('table_name', 'spider.csrc_result')
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
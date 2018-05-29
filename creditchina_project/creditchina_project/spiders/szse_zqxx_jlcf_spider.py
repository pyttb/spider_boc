# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy
from scrapy import Selector

from creditchina_project.ssze_items import SszeZqxxJlcfResultItem, SszeLoaderItem

reload(sys)
sys.setdefaultencoding('utf-8')
class SzseZqxxJlcfSpider(scrapy.Spider):
    name = "szse_zqxx_jlcf"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.szse.cn']
    default_data = {
        'TABKEY':'tab1',
        'tab1RECORDCOUNT': 12,
        'tab1PAGENO': 1,
        'tab1PAGECOUNT': 2,
        'REPORT_ACTION': 'navigate',
        'CATALOGID': 'ZQ_JLCF',
        'AJAX': 'AJAX-TRUE',
        'ACTIONID': '7'
    }
    default_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5,zh-TW;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://www.szse.cn/main/disclosure/zqxx/jlcf/',
        'Origin': 'http://www.szse.cn',
        'Connection': 'keep-alive',
        'Host': 'www.szse.cn'
    }

    def start_requests(self):
        for page in range(1,3):
            self.default_data['tab1PAGENO']=page
            yield scrapy.Request(url='http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.4199557422175839', headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), callback=self.parse_basic_info, method='POST',
                                 dont_filter=True)

    def parse_basic_info(self, response):
        contents = response.xpath('//table[@id="REPORTID_tab1"]//tr').extract()[1:]
        for content in contents:
            company_name = Selector(text=content).xpath('//tr/td[1]/text()').extract()[0]
            writ_no = Selector(text=content).xpath('//tr/td[3]/text()').extract()[0]
            pub_type = Selector(text=content).xpath('//tr/td[4]//a/text()').extract()[0]
            writ_date = Selector(text=content).xpath('//tr/td[5]/text()').extract()[0]
            rel_bond = Selector(text=content).xpath('//tr/td[6]/text()').extract()[0]
            start = '给予'
            end = '的决定'
            pub_type = (pub_type.split(start))[1].split(end)[0]
            item = SszeLoaderItem(item=SszeZqxxJlcfResultItem(), response=response)
            item.add_value('batch_date', self.batch_date)
            item.add_value('company_name', company_name)
            item.add_value('writ_no', writ_no)
            item.add_value('pub_type', pub_type)
            item.add_value('writ_date', writ_date)
            item.add_value('rel_bond', rel_bond)
            item.add_value('table_name', 'spider.szse_zqxx_jlcf_result')
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
# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy
from scrapy import Selector

from creditchina_project.stats_items import StatsLoaderItem, StatsResultItem

reload(sys)
sys.setdefaultencoding('utf-8')
class StatsSpider(scrapy.Spider):
    name = "stats"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.stats.gov.cn']
    default_data = {
    }
    default_headers = {

    }

    def start_requests(self):
        yield scrapy.Request(url='http://www.stats.gov.cn/tjfw/sxqygs/gsxx/', headers=self.default_headers,
                             body=urllib.urlencode(self.default_data), callback=self.parse_basic_info,
                             dont_filter=True)

    def parse_basic_info(self, response):
        urls = response.xpath('//div[@class="center_list"]/ul[@class="center_list_contlist"]//li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url='http://www.stats.gov.cn/tjfw/sxqygs/gsxx'+url[1:], headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), callback=self.parse_detail_info,
                                 dont_filter=True)

    def parse_detail_info(self, response):
        pub_writ_no=''
        pub_writ_nos = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[1]//td[2]/p//span/text()').extract()
        for text in pub_writ_nos:
            pub_writ_no=pub_writ_no+text
        pub_name = ''
        pub_names = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[2]//td[2]/p//span/text()').extract()
        for text in pub_names:
            pub_name = pub_name + text
        pub_type_1 = ''
        pub_type_1s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[3]//td[2]/p//span/text()').extract()
        for text in pub_type_1s:
            pub_type_1 = pub_type_1 + text
        pub_type_2 = ''
        pub_type_2s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[4]//td[2]/p//span/text()').extract()
        for text in pub_type_2s:
            pub_type_2 = pub_type_2 + text
        pub_reason = ''
        pub_reasons = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[5]//td[2]/p//span/text()').extract()
        for text in pub_reasons:
            pub_reason = pub_reason + text
        pub_gist = ''
        pub_gists = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[6]//td[2]/p//span/text()').extract()
        for text in pub_gists:
            pub_gist = pub_gist + text
        admin_counterpart_name = ''
        admin_counterpart_names = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[7]//td[2]/p//span/text()').extract()
        for text in admin_counterpart_names:
            admin_counterpart_name = admin_counterpart_name + text
        admin_counterpart_code_1 = ''
        admin_counterpart_code_1s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[8]//td[2]/p//span/text()').extract()
        for text in admin_counterpart_code_1s:
            admin_counterpart_code_1 = admin_counterpart_code_1 + text
        admin_counterpart_code_2 = ''
        admin_counterpart_code_2s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[9]//td[2]/p//span/text()').extract()
        for text in admin_counterpart_code_2s:
            admin_counterpart_code_2 = admin_counterpart_code_2 + text
        admin_counterpart_code_3 = ''
        admin_counterpart_code_3s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[10]//td[2]/p//span/text()').extract()
        for text in admin_counterpart_code_3s:
            admin_counterpart_code_3 = admin_counterpart_code_3 + text
        admin_counterpart_code_4 = ''
        admin_counterpart_code_4s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[11]//td[2]/p//span/text()').extract()
        for text in admin_counterpart_code_4s:
            admin_counterpart_code_4 = admin_counterpart_code_4 + text
        admin_counterpart_code_5 = ''
        admin_counterpart_code_5s = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[12]//td[2]/p//span/text()').extract()
        for text in admin_counterpart_code_5s:
            admin_counterpart_code_5 = admin_counterpart_code_5 + text
        publicity_term = ''
        publicity_terms = response.xpath('//table[@class="MsoNormalTable"]/tbody//tr[15]//td[2]/p//span/text()').extract()
        for text in publicity_terms:
            publicity_term = publicity_term + text
        item = StatsLoaderItem(item=StatsResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        item.add_value('pub_writ_no', pub_writ_no)
        item.add_value('pub_name', pub_name)
        item.add_value('pub_type_1', pub_type_1)
        item.add_value('pub_type_2', pub_type_2)
        item.add_value('pub_reason', pub_reason)
        item.add_value('pub_gist', pub_gist)
        item.add_value('admin_counterpart_name', admin_counterpart_name)
        item.add_value('admin_counterpart_code_1', admin_counterpart_code_1)
        item.add_value('admin_counterpart_code_2', admin_counterpart_code_2)
        item.add_value('admin_counterpart_code_3', admin_counterpart_code_3)
        item.add_value('admin_counterpart_code_4', admin_counterpart_code_4)
        item.add_value('admin_counterpart_code_5', admin_counterpart_code_5)
        item.add_value('publicity_term', publicity_term)
        item.add_value('table_name', 'spider.stats_result')
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
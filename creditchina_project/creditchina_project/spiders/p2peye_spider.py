# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy

from creditchina_project.p2peye_items import P2peyeResultItem,P2peyeLoaderItem

reload(sys)
sys.setdefaultencoding('utf-8')
class P2peye(scrapy.Spider):
    name = "p2peye"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.p2peye.com']
    default_data = {
    }
    default_headers = {
    }
    MAX_PAGE=300
    def start_requests(self):

        for page in range(1,self.MAX_PAGE):
            yield scrapy.Request(url='http://www.p2peye.com/platformData.php?mod=issue&ajax=1&action=getPage&page='+str(page), headers=self.default_headers,
                                 body=urllib.urlencode(self.default_data), callback=self.parse_basic_info, dont_filter=True)
    def parse_basic_info(self, response):
        basic_info = response.text
        code=eval(basic_info.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['code']
        datas = eval(basic_info.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['data']
        if code=='0':
            for data in datas:
                name = data['name']
                black_time = data['black_time']
                online_time = data['online_time']
                city_name = data['city_name']
                black_type_name = data['black_type_name']
                black_url = data['black_url']
                if name!=None and name!='':
                    name=name.decode('unicode-escape')
                if black_time!=None and black_time!='':
                    black_time=black_time.decode('unicode-escape')
                if online_time!=None and online_time!='':
                    online_time=online_time.decode('unicode-escape')
                if city_name!=None and city_name!='':
                    city_name=city_name.decode('unicode-escape')
                if black_type_name!=None and black_type_name!='':
                    black_type_name=black_type_name.decode('unicode-escape')
                if black_url!=None and black_url!='':
                    black_url=black_url.decode('unicode-escape')
                    black_url=black_url.replace('\\','')
                if black_url!=None and black_url!='':
                    yield scrapy.Request(
                        url=black_url, headers=self.default_headers, body=urllib.urlencode(self.default_data),
                        meta={'name':name,'black_time':black_time,'online_time':online_time,'city_name':city_name,'black_type_name':black_type_name},
                        callback=self.parse_detail_info, dont_filter=True)
                else:
                    item = P2peyeLoaderItem(item=P2peyeResultItem(), response=response)
                    item.add_value('batch_date', self.batch_date)
                    item.add_value('name', name)
                    item.add_value('black_time', black_time)
                    item.add_value('online_time', online_time)
                    item.add_value('city_name', city_name)
                    item.add_value('black_type_name', black_type_name)
                    item.add_value('table_name', 'creditchina.p2peye_result')
                    yield item.load_item()
    def parse_detail_info(self, response):
        name=response.meta['name']
        black_time = response.meta['black_time']
        online_time = response.meta['online_time']
        city_name = response.meta['city_name']
        black_type_name = response.meta['black_type_name']
        reg_capital_info=response.xpath("//table[@class='t_table']/tr[2]/td[2]//*[text()]/text()").extract()
        reg_capital=''
        for capital in reg_capital_info:
            reg_capital=reg_capital+capital
        comp_name_info = response.xpath("//table[@class='t_table']/tr[5]/td[2]//*[text()]/text()").extract()
        comp_name = ''
        for names in comp_name_info:
            comp_name = comp_name + names
        status_info = response.xpath("//table[@class='t_table']/tr[11]/td[2]//*[text()]/text()").extract()
        status = ''
        for statu in status_info:
            status = status + statu
        item = P2peyeLoaderItem(item=P2peyeResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        item.add_value('name', name)
        item.add_value('black_time', black_time)
        item.add_value('online_time', online_time)
        item.add_value('city_name', city_name)
        item.add_value('black_type_name', black_type_name)
        item.add_value('comp_name', comp_name)
        item.add_value('reg_capital', reg_capital)
        item.add_value('status', status)
        item.add_value('table_name', 'creditchina.p2peye_result')
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
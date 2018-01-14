# -*- coding: utf-8 -*-
import urllib

import scrapy
from amacinfodisk.items import AmacInfoLoaderItem,ManagerListInfoItem,AmacinfodiskProjectItem
from bs4 import BeautifulSoup
import urllib2
import datetime
import json
import requests
import logging
import time
import urlparse

class FundmanagerlistSpider(scrapy.Spider):
    name = 'fundManagerList'
    allowed_domains = ['gs.amac.org.cn']
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html']
    # start_urls = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager"
    start_urls = ['http://gs.amac.org.cn/amac-infodisc/api/pof/manager']
    base_url= 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager'
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        'Connection': 'keep_alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Host': 'gs.amac.org.cn',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    payload = {'page': 0, 'size': 20}  # 失信加上参数
    body = {}

    def start_requests(self):
        for url in self.start_urls:
            print "url:" + url
            # yield scrapy.Request(url=url,method='POST',callback=self.parse, meta=self.payload,
            # body=json.dumps(self.payload),headers=self.headers)
            yield scrapy.Request(url=url, method='POST', headers=self.headers, body=json.dumps(self.payload),
                                     callback=self.parse_pages_loop,dont_filter=True)

    def parse_pages_loop(self, response):

        # "totalElements":22565, "totalPages":2257, "size":10
        # json转化成python dict
        js = json.loads(response.text)
        totalElements = js.get("totalElements")
        totalPages = js.get("totalPages")
        size = js.get("size")

        self.log(message='totalElements:{},totalPages:{}'.format(totalElements, totalPages), level=logging.INFO)
        # 根据页面totalPages，轮循
        if totalPages and totalElements:
            # for page in range(0, totalPages - 1):  # 页面提交-1
            for page in range(0, 10):  # 页面提交-1
                localpayload = {'page': page, 'size': size}
                page_url = "?page="+str(page)+"&size="+str(size);

                page_full_url=urlparse.urljoin(self.base_url, page_url);
                logging.info("now visting: "+page_full_url)
                yield scrapy.Request(url=page_full_url, method='POST', headers=self.headers, body=json.dumps(localpayload),
                                     callback=self.parseFundManagerList, dont_filter=True)

    def parseFundManagerList(self, response):
        # time.sleep(5)

        # rows = json.loads(response.text).get("content")
        # qry_date = datetime.datetime.now().date()
        # if rows:
        #     for row in rows:
        #         list_item = AmacInfoLoaderItem(item=ManagerListInfoItem(), response=response)
        #         list_item.add_value('qry_date', qry_date)
        #         list_item.add_value('id', row.get("id"))
        #         list_item.add_value('managerName', row.get("managerName"))
        #
        #         #尝试取得DICT键值对，后面改成统一的方式
        #         for key in row.keys():
        #             list_item.add_value(key,row.get(key))
        #
        #         item = list_item.load_item()
        #         yield item




        print(response)
        pass
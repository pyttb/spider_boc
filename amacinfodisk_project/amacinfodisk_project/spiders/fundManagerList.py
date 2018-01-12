# -*- coding: utf-8 -*-
import urllib

import scrapy
#from amacinfodisk_project.items import AmacInfoLoaderItem,ManagerListInfoItem,AmacinfodiskProjectItem
from bs4 import BeautifulSoup
import urllib2
import datetime
import json
import requests


class FundmanagerlistSpider(scrapy.Spider):
    name = 'fundManagerList'
    allowed_domains = ['gs.amac.org.cn']
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html']
    # start_urls = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager"
    start_urls = ['http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=0&size=20']
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
    payload={}
    body={}

    def start_requests(self):
        for url in self.start_urls:
            print "url:"+url
            # yield scrapy.Request(url=url,method='POST',callback=self.parse, meta=self.payload,body=json.dumps(self.payload),headers=self.headers)
            yield scrapy.FormRequest(url=url,method='POST',headers=self.headers,body=json.dumps(self.payload),callback=self.parse)



    def parse(self, response):

        print (response.text)
        pass
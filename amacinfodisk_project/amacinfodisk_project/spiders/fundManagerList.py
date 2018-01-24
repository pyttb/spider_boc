# -*- coding: utf-8 -*-
import urllib
import sys
import scrapy
from bs4 import BeautifulSoup

import datetime
import json
import requests
import logging
import time
import re
import urlparse
from amacinfodisk_project.items import AmacinfodiskProjectItem,AmacInfoLoaderItem,ManagerListInfoItem


class FundmanagerlistSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'fundManagerList'
    allowed_domains = ['gs.amac.org.cn']
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html']
    # start_urls = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager"
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/api/pof/manager']
    start_urls = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?&page=0&size=20'
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
    payload_all = [
        {'creditInfo': "isLostContactMechanism"}  # 失联机构
         ,{'creditInfo': "identification"}    #异常机构
         , {'creditInfo': "shamStatement"}     #虚假填报
         , {'creditInfo': "materRialOmission"}   #重大遗漏
         , {'creditInfo': "eightLine"}   #违反八项规定
         , {'creditInfo': "badCredit"}  # 相关主题存在不良记录
    ]
    #payload = {'creditInfo': "identification"} # 失联机构
    def start_requests(self):
        for payload in self.payload_all:
            print "url:" + self.start_urls
            yield scrapy.Request(url=self.start_urls, method='POST', headers=self.headers,
                                 body=json.dumps(payload),
                                 callback=self.parse_pages_loop,
                                 meta= {'payload':payload},dont_filter=True)

    def parse_pages_loop(self, response):
        # "totalElements":22565, "totalPages":2257, "size":10
        # json转化成python dict
        js = json.loads(response.text)
        totalPages = js.get("totalPages")
        payload = response.meta['payload']
        for page in range(0, totalPages):  # 页面提交
                # for page in range(0, 2):  # 页面提交
                page_url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=' + str(page) + '&size=20'
                logging.info("now visting: " + page_url)
                yield scrapy.Request(url=page_url, method='POST', headers=self.headers,
                                     body=json.dumps(payload),
                                     callback=self.parseFundManagerList,
                                     meta={'payload': payload},dont_filter=True)

    def parseFundManagerList(self, response):
        # time.sleep(5)
        rows = json.loads(response.text).get("content")
        payload = response.meta['payload']
        #if payload =
        if rows:
            for row in rows:
                detail_url = row.get("url")
                url_link="http://gs.amac.org.cn/amac-infodisc/res/pof/manager/"+detail_url;
                row = dict(row,**payload)
                yield scrapy.Request(url=url_link, method='GET', headers=self.headers,
                                 body=json.dumps({}),
                                 callback=self.parseFundManagerPublicInfo,
                                 meta=row,
                                 dont_filter=True)

    def parseFundManagerPublicInfo(self, response):
        shilian_jigou =""
        yichang_jigou =""
        organization_code =""
        dataSrc =""
        row = response.meta
        list_item = AmacInfoLoaderItem(item=ManagerListInfoItem(), response=response)
        for key in row.keys():
            if key in list_item.ManagerListInfoItem_columns:
                list_item.add_value(key, row.get(key))

        if re.search(u"失联机构.*\n.*", response.text):
            shilian_jigou = re.search(u"失联机构.*\n.*", response.text).group()
        if re.search(u"异常机构.*\n.*", response.text):
            yichang_jigou = re.search(u"异常机构.*\n.*", response.text).group()
        if response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]/text()"):
            organization_code = response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]/text()").extract_first('').strip()
        if response.xpath('//*[@id="complaint1"]/text()'):
            managerName= response.xpath('//*[@id="complaint1"]/text()').extract_first('').strip()
        qry_date = datetime.datetime.now().date()
        if row.get('creditInfo') == "isLostContactMechanism":
            dataSrc = "失联机构"
        elif row.get('creditInfo') == "identification":
            dataSrc = "异常机构"
        elif row.get('creditInfo') == "shamStatement":
            dataSrc = "虚假填报"
        elif row.get('creditInfo') == "materRialOmission":
            dataSrc = "重大遗漏"
        elif row.get('creditInfo') == "eightLine":
            dataSrc = "违反八项规定"
        else:
            dataSrc = "相关主题存在不良记录"

        list_item.add_value('qry_date', qry_date)
        list_item.add_value('shilian_jigou', shilian_jigou)
        list_item.add_value('yichang_jigou', yichang_jigou)
        list_item.add_value('organization_code', organization_code)
        list_item.add_value('dataSrc',dataSrc)
        item = list_item.load_item()
        yield item

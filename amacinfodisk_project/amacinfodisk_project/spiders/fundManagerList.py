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
        #{'creditInfo': "isLostContactMechanism"}  # 失联机构
         #,{'creditInfo': "identification"}    #异常机构
         #, {'creditInfo': "shamStatement"}     #虚假填报
         #,
        {'creditInfo': "materRialOmission"}   #重大遗漏
         #, {'creditInfo': "eightLine"}   #违反八项规定
         #, {'creditInfo': "badCredit"}  # 相关主题存在不良记录
    ]
    #payload = {'creditInfo': "identification"} # 失联机构
    def start_requests(self):
        #六个模块仅payload不一样，初始url一致
        for payload in self.payload_all:
            print "url:" + self.start_urls
            yield scrapy.Request(url=self.start_urls, method='POST', headers=self.headers,
                                 body=json.dumps(payload),
                                 callback=self.parse_pages_loop,
                                 meta= {'payload':payload},dont_filter=True)
    #解析当前payload对应页面，拿到json包
    def parse_pages_loop(self, response):
        # "totalElements":22565, "totalPages":2257, "size":10
        # json转化成python dict
        js = json.loads(response.text)
        totalPages = js.get("totalPages")
        payload = response.meta['payload']
        #根据json数据中页面数，循环
        for page in range(0, totalPages):  # 页面提交
                # for page in range(0, 2):  # 页面提交
                page_url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=' + str(page) + '&size=20'
                logging.info("now visting: " + page_url)
                yield scrapy.Request(url=page_url, method='POST', headers=self.headers,
                                     body=json.dumps(payload),
                                     callback=self.parseFundManagerList,
                                     meta={'payload': payload},dont_filter=True)
    #解析具体第一层界面，得到当前页公司部分信息，通过meta=row传递给下一层
    def parseFundManagerList(self, response):
        # time.sleep(5)
        rows = json.loads(response.text).get("content")
        payload = response.meta['payload']
        #if payload =
        if rows:
            for row in rows:
                detail_url = row.get("url")
                url_link="http://gs.amac.org.cn/amac-infodisc/res/pof/manager/"+detail_url;
                #url_link = "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000010425.html";
                row = dict(row,**payload)
                yield scrapy.Request(url=url_link, method='GET', headers=self.headers,
                                 body=json.dumps({}),
                                 callback=self.parseFundManagerPublicInfo,
                                 meta=row,
                                 dont_filter=True)
    #获得具体公司链接下的页面，同时拿到上一层具体公司的其他想信息，一起传入item
    def parseFundManagerPublicInfo(self, response):
        orgInfo1 =""    #失联机构
        orgInfo2 =""    #异常机构
        orgInfo3 = ""   #重大遗漏
        orgInfo4 = ""   #违反八条底线
        orgInfo5 = ""   #虚假填报
        orgInfo6 = ""   #不良诚信
        orgInfo7 = ""   #其他诚信信息
        organization_code =""
        dataSrc =""
        #拿到传入的公司信息
        row = response.meta
        list_item = AmacInfoLoaderItem(item=ManagerListInfoItem(), response=response)
        #根据ManagerListInfoItem()列名，找对应字典row中存的值
        for key in row.keys():
            if key in list_item.ManagerListInfoItem_columns:
                list_item.add_value(key, row.get(key))
        #获取诚信信息中失联机构、异常机构、组织机构代码
        if re.search(u"失联机构.*\n.*", response.text):
            orgInfo1 = re.search(u"失联机构.*\n.*", response.text).group()
        if re.search(u"异常机构.*\n.*", response.text):
            orgInfo2 = re.search(u"异常机构.*\n.*", response.text).group()
        if re.search(u"重大遗漏.*\n.*", response.text):
            orgInfo3 = re.search(u"重大遗漏.*\n.*", response.text).group()
        if re.search(u"违反八条底线.*\n.*", response.text):
            orgInfo4 = re.search(u"违反八条底线.*\n.*", response.text).group()
        if re.search(u"虚假填报.*\n.*", response.text):
            orgInfo5 = re.search(u"虚假填报.*\n.*", response.text).group()
        if re.search(u"不良诚信.*\n.*", response.text):
            orgInfo6 = re.search(u"不良诚信.*\n.*", response.text).group()
        if re.search(u"其他诚信信息.*\n.*", response.text):
            orgInfo7 = re.search(u"其他诚信信息.*\n.*", response.text).group()
            #orgInfo7 = re.match( r'(.*) 其他诚信信息 (.*?) .*', response.text).group()

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
            dataSrc = "违反八项底线"
        else:
            dataSrc = "相关主题存在不良记录"

        list_item.add_value('qry_date', qry_date)
        list_item.add_value('orgInfo1', orgInfo1)
        list_item.add_value('orgInfo2', orgInfo2)
        list_item.add_value('orgInfo3', orgInfo3)
        list_item.add_value('orgInfo4', orgInfo4)
        list_item.add_value('orgInfo5', orgInfo5)
        list_item.add_value('orgInfo6', orgInfo6)
        list_item.add_value('orgInfo7', orgInfo7)
        list_item.add_value('organization_code', organization_code)
        list_item.add_value('dataSrc',dataSrc)
        item = list_item.load_item()
        yield item

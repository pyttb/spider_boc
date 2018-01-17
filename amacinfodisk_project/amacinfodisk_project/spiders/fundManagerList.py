# -*- coding: utf-8 -*-
import urllib
import sys
import scrapy
from bs4 import BeautifulSoup
import urllib2
import datetime
import json
import requests
import logging
import time
import urlparse
import re
from amacinfodisk_project.items import AmacinfodiskProjectItem,AmacInfoLoaderItem,ManagerListInfoItem,ManagerCreditInfoItem
from bs4 import BeautifulSoup


class FundmanagerlistSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'fundManagerList'
    allowed_domains = ['gs.amac.org.cn']
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html']
    # start_urls = "http://gs.amac.org.cn/amac-infodisc/api/pof/manager"
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/api/pof/manager']
    start_urls = ['http://gs.amac.org.cn/amac-infodisc/api/pof/manager?&page=0&size=20']
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
    # payload = {'page': 0, 'size': 20, 'creditInfo':'isLostContactMechanism'}  # 失信后面需要加上参数 {"creditInfo":"isLostContactMechanism"}
    payload = {'creditInfo': 'isLostContactMechanism'}
    body = {}

    def start_requests(self):
        for url in self.start_urls:
            print "url:" + url
            # yield scrapy.Request(url=url,method='POST',callback=self.parse, meta=self.payload,
            # body=json.dumps(self.payload),headers=self.headers)
            yield scrapy.Request(url=url, method='POST', headers=self.headers,
                                 body=json.dumps(self.payload),
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
            for page in range(0, totalPages):  # 页面提交
            # for page in range(0, 2):  # 页面提交
                localpayload = {'page': page, 'size': size}
                localpayload = dict(localpayload,**self.payload)
                page_url = "?page="+str(page)+"&size="+str(size);

                page_full_url=urlparse.urljoin(self.base_url, page_url);
                logging.info("now visting: "+page_full_url)
                yield scrapy.Request(url=page_full_url, method='POST', headers=self.headers,
                                     body=json.dumps(localpayload),
                                     callback=self.parseFundManagerList, dont_filter=True)

    def parseFundManagerList(self, response):
        # time.sleep(5)

        rows = json.loads(response.text).get("content")
        qry_date = datetime.datetime.now().date()
        if rows:
            for row in rows:
                list_item = AmacInfoLoaderItem(item=ManagerListInfoItem(), response=response)
                list_item.add_value('qry_date', qry_date)
                # list_item.add_value('id', row.get("id"))
                # list_item.add_value('managerName', row.get("managerName"))
                # list_item.add_value('artificialPersonName', row.get("artificialPersonName"))
                # list_item.add_value('registerNo', row.get("registerNo"))
                # list_item.add_value('establishDate', row.get("establishDate"))
                # list_item.add_value('managerHasProduct', row.get("managerHasProduct"))
                # list_item.add_value('url', row.get("url"))
                # list_item.add_value('registerDate', row.get("registerDate"))
                # list_item.add_value('registerAddress', row.get("registerAddress"))
                # list_item.add_value('registerProvince', row.get("registerProvince"))
                # list_item.add_value('registerCity', row.get("registerCity"))
                # list_item.add_value('regAdrAgg', row.get("regAdrAgg"))
                # list_item.add_value('primaryInvestType', row.get("primaryInvestType"))

                #尝试取得DICT键值对，后面改成统一的方式
                for key in row.keys():
                    if key in list_item.ManagerListInfoItem_columns:
                        list_item.add_value(key,row.get(key))

                item = list_item.load_item()
                yield item

                detail_url = row.get("url")
                if detail_url:
                    # url_link = urlparse.urljoin(self.base_url,"/",detail_url);
                    url_link="http://gs.amac.org.cn/amac-infodisc/res/pof/manager/"+detail_url;
                    yield scrapy.Request(url=url_link, method='GET', headers=self.headers,
                                     body=json.dumps({}),
                                     callback=self.parseFundManagerPublicInfo, dont_filter=True)


    def parseFundManagerPublicInfo(self, response):


        #/html/body/div/div[2]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td
        # "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/101000000138.html"

        # soup.prettify()

        #selector="body > div > div.g-body > div > table > tbody > tr:nth-child(6) > td.td-content"
        #xpath="/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]"
        #soup=BeautifulSoup(response.text,'lxml')
        #soup.find_all('td', attrs={'class': 'td-content', 'colspan': '3'})

        # response.xpath("/html/body/div/div[2]/div/table/tbody/tr[1]/td[2]/table/tr[1]/td/text()").extract_first('').strip()
        # response.xpath("/html/body/div/div[2]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td/text()")
        # response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]/text()")
        # response.xpath("/html/body/div/div[2]/div/table/tbody/tr[1]/td[2]/table/tr[1]/td/text()").extract_regex(u'失联机构').strip()
        # response.xpath("/html/body/div/div[2]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/span/text()")

        shilianString="";
        yichangString="";
        organization_code="";
        managerName="";

        if re.search(u"失联机构.*\n.*", response.text):
            shilianString = re.search(u"失联机构.*\n.*", response.text).group()
            shilianString = shilianString.replace("\s",'')
            shilianString = shilianString.replace("</span>&nbsp;",'')
            shilianString = shilianString.replace("\n", '')
            shilianString = shilianString.replace("\t", '')
            shilianString = shilianString.replace("<a.*/a>", '')    #去掉链接字符串
        if re.search(u"异常机构.*\n.*", response.text):
            yichangString = re.search(u"异常机构.*\n.*", response.text).group()
            yichangString = yichangString.replace("\s",'')
            yichangString = yichangString.replace("</span>&nbsp;",'')
            yichangString = yichangString.replace("\n", '')
            yichangString = yichangString.replace("\t", '')

        # response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]")
        # organization_code = response.xpath('//div[@class="m-manager-list m-list-details"]/table/tbody/tr[6]/td[2]/text()').extract_first('').strip()
        if response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]/text()"):
            organization_code = response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]/text()").extract_first('').strip()

        if response.xpath('//*[@id="complaint1"]/text()'):
            managerName= response.xpath('//*[@id="complaint1"]/text()').extract_first('').strip()
            managerName = managerName.replace("&nbsp", '')
            managerName = managerName.replace("\s", '')
            managerName = managerName.replace(" ", '')

        qry_date = datetime.datetime.now().date()
        list_item = AmacInfoLoaderItem(item=ManagerCreditInfoItem(), response=response)
        list_item.add_value('qry_date', qry_date)
        list_item.add_value('managerName', managerName)
        list_item.add_value('shilian_jigou', shilianString)
        list_item.add_value('yichang_jigou', yichangString)
        list_item.add_value('organization_code', organization_code)

        item = list_item.load_item()
        yield item
# -*- coding: utf-8 -*-
import scrapy


class FundmanagerlistSpider(scrapy.Spider):
    name = 'fundManagerList'
    allowed_domains = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html']
    start_urls = ['http://http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy
from amacinfodisk_project.items import AmacInfoLoaderItem,ManagerListInfoItem,AmacinfodiskProjectItem

class FundmanagerlistSpider(scrapy.Spider):
    name = 'fundManagerList'
    allowed_domains = ['gs.amac.org.cn']
    start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/manager/managerList.html']


    def parse(self, response):

        print(response)




        pass

# -*- coding: utf-8 -*-
import random
import time
from datetime import datetime
import pandas as pd

import scrapy
import re
from scrapy.http import Request
from scrapy.http import FormRequest
from bs4 import BeautifulSoup

from urlparse import urljoin

from creditchina_project.overseas_investment_items import OverseasInvestLoaderItem, OverseasInvestResultItem
from hyperlink.test.test_decoded_url import BASIC_URL


# from ..settings import TABLE_NAME

# from creditchina_project.utils.dbutils import queryAll, execute

TABLE_NAME = 'spider.tudi_result'

class TudiEndSpider(scrapy.Spider):
    name = 'overseas_investment'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,

        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        },
    }
    
    start_urls = ['http://femhzs.mofcom.gov.cn/fecpmvc/pages/fem/CorpJWList.html']
    
    
    def start_requests(self):
        
        full_url = 'http://femhzs.mofcom.gov.cn/fecpmvc/pages/fem/CorpJWList.html'
        
        yield Request(url=full_url, callback=self.parse_page, dont_filter=True)
        
    def parse_page(self, response):
        
        basic_url = 'http://femhzs.mofcom.gov.cn/'
        bs = BeautifulSoup(response.text, 'html.parser')
        page = bs.find('em', {'class': 'm-page-total-num'}).text
        print("page:")
        print(page)
        tr_list = bs.select('tr[id*="foreach"]')
        for tr in tr_list:
            item = OverseasInvestLoaderItem(item=OverseasInvestResultItem(), response=response)
            
            td_list =  tr.find_all("td")
            
            item.add_value('table_name', 'spider.rh_overseas_investment_list')
            i = 0
            for td in td_list:
                tdText = td.text
                tdText = tdText.replace("\t",'').replace(" ",'')
#                 print(tdText)
                
                if i == 0 :
                    item.add_value('company', tdText)
                elif i == 1:
                    item.add_value('investor', tdText)
                else:
                    item.add_value('country', tdText)
                    
                i += 1
            yield item.load_item()
                
        try:
            nextPage = bs.find('a',{'class':'last pagenxt'})
            nextLink = nextPage.attrs['href'].decode('utf-8')
#             print(nextLink)
            next_url = urljoin(basic_url, nextLink)
            yield Request(url=next_url, callback=self.parse_page, dont_filter=True)  
        except Exception as e:
            print(e)
            print("end page!!")
        
             
        
      
  
           
            
            
            
            
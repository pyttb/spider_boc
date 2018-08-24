# -*- coding: utf-8 -*-
import scrapy
import urlparse
import datetime
import logging

class NewsBankofchinaSpider(scrapy.Spider):
    name = 'news_bankofchina'
    # allowed_domains = ['www.boc.cn']
    start_urls = ['http://www.boc.cn/aboutboc/bi1/']
    base_url='http://www.boc.cn/aboutboc/bi1/'
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'runasone_project.pipelines.ExcelPipeline': 100,     #保存到EXCEL表格
            'runasone_project.pipelines.RunasoneDB2Pipeline': 100,  # 保存到数据库
        }
    }
    def parse(self, response):
        #1、找到所有的面标签，循环调用
        qry_date = datetime.datetime.now().date()
        all_pages_count = response.xpath('/html/body/div/div[5]/div/div/p/span/text()').extract_first()
        for i in range(0, int(all_pages_count.encode('utf8')) -1):
            if i==0:
                extend_url =  "index.html"
            else:
                extend_url = "index_"+str(i)+".html"
            try:
                url = urlparse.urljoin(self.base_url,extend_url );
                self.log(message="visting=====" + url, level=logging.INFO)
                yield scrapy.Request(url=url,callback=self.get_page_brief)
            except(Exception ) as e:
                self.log(message="exception....."+extend_url, level=logging.INFO)

    def get_page_brief(self,response):
        # 2、找到所有的新闻链接
        ul_lists = response.xpath('//ul[@class="list"]')

        detail_url=ul_lists[0].css('::attr("href")').extract_first('').strip().replace('\r\n', '').replace('\t', '')

        if detail_url is not None:
            url = urlparse.urljoin(self.base_url, detail_url);
            self.log(message="visting=====" + url, level=logging.INFO)
            yield scrapy.Request(url=url,
                meta={'details_url': url},
                callback=self.get_page_detail)


        ###################################BEAUTIFUL SOUP REWRITE###################################




    #3、点开所有的新闻
    def get_page_detail(self,response):
        if response:
            content_essay = response.xpath('/html/body/div/div[5]/div[1]/div[2]/p[1]/text()').extract_first();
            if content_essay is not None:
                print content_essay


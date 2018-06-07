# -*- coding: utf-8 -*-
import scrapy,re,logging,datetime
from aqsiq_project.items import AqsiqResultItem

class AqsiqSpiderSpider(scrapy.Spider):
    name = 'aqsiq'

    custom_settings = {
        'ITEM_PIPELINES': {
            'aqsiq_project.pipelines.MysqlPipeline': 100,
        }
    }

    batch_date = datetime.datetime.now().date()

    allowed_domains = ['www.aqsiq.gov.cn']
    start_urls = ['http://www.aqsiq.gov.cn/zjsj/jssj/jssj8/index.htm']
    page = 1

    def parse(self, response):
        print('---------',self.page)
        list_url = response.xpath('//a[@class="quicklink"]/@href').extract()
        base_url = 'http://www.aqsiq.gov.cn/zjsj/jssj/jssj8'
        for a in list_url:
            deatil_url = base_url + a[1:]
            print(deatil_url)
            yield scrapy.Request(url = deatil_url, callback = self.parse_item, dont_filter = True)

        allPage = re.findall(r'var countPage = (\d)//',response.text)
        allPage = int(allPage[0])
        if self.page < allPage:
            pageUrl = base_url + '/index_%s.htm'%self.page
            yield scrapy.Request(url = pageUrl, callback=self.parse, dont_filter = True)
            self.page += 1

    def parse_item(self, response):
        infos = response.xpath('//div[@class="TRS_Editor"]/table/tbody/tr')

        for info in infos[1:-1]:
            item = AqsiqResultItem()
            item['batch_date']=self.batch_date
            item['comp_name']=info.xpath('./td[2]/font/text()').extract_first()
            item['place']=info.xpath('./td[3]/font/text()').extract_first()
            item['product_name']=info.xpath('./td[4]/font/text()').extract_first()
            item['spec_type']=info.xpath('./td[5]/font/text()').extract_first()
            item['produce_date']=info.xpath('./td[6]/font/text()').extract_first()
            item['desq_pro']=info.xpath('./td[7]/font/text()').extract_first()
            item['insp_agency']=info.xpath('./td[8]/font/text()').extract_first()
            item['release_date']=response.xpath('//div[@class="xj2"]/text()').extract_first()
            yield item

    def closed(self, reason):
        if 'finished' == reason:
            logging.warning('%s', '爬虫程序执行结束，即将关闭')
        elif 'shutdown' == reason:
            logging.warning('%s', '爬虫进程被强制中断，即将关闭')
        elif 'cancelled' == reason:
            logging.warning('%s', '爬虫被引擎中断，即将关闭')
        else:
            logging.warning('%s', '爬虫被未知原因打断，即将关闭')
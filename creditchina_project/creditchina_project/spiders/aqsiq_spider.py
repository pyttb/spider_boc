# -*- coding: utf-8 -*-
import scrapy,re,logging,datetime
from creditchina_project.aqsiq_items import AqsiqResultItem, AqsiqLoaderItem


class AqsiqSpiderSpider(scrapy.Spider):
    name = 'aqsiq'

    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }

    batch_date = datetime.datetime.now().date()

    allowed_domains = ['www.aqsiq.gov.cn']
    start_urls = ['http://www.aqsiq.gov.cn/zjsj/jssj/jssj8/index.htm']
    page = 1

    def parse(self, response):
        list_url = response.xpath('//a[@class="quicklink"]/@href').extract()
        base_url = 'http://www.aqsiq.gov.cn/zjsj/jssj/jssj8'
        for a in list_url:
            deatil_url = base_url + a[1:]
            yield scrapy.Request(url = deatil_url, callback = self.parse_item, dont_filter = True)

        allPage = re.findall(r'var countPage = (\d)//',response.text)
        allPage = int(allPage[0])
        if self.page < allPage:
            pageUrl = base_url + '/index_%s.htm'%self.page
            yield scrapy.Request(url = pageUrl, callback=self.parse, dont_filter = True)
            self.page += 1

    def parse_item(self, response):
        infos = response.xpath('//div[@class="TRS_Editor"]/table/tbody/tr')
        if len(infos)==0:
            return
        keys=infos[0].xpath('./td/font/text()').extract()
        alt_title=response.xpath('//td[@class="border"]/div[@class="sj_h"]/h1/text()').extract_first()
        product_name=''
        for info in infos[1:-1]:
            values=[]
            tds=info.xpath('./td')
            for td in tds:
                value=''.join(td.xpath('./font//text()').extract())
                values.append(value)
            item = AqsiqLoaderItem(item=AqsiqResultItem(), response=response)
            item.add_value('batch_date', self.batch_date)
            for idx in range(1,len(keys)):
                if keys[idx].find('企业名称')>=0:
                    item.add_value('comp_name', values[idx])
                if keys[idx].find('所在地')>=0 or keys[idx].find('所在省')>=0:
                    item.add_value('place', values[idx])
                if keys[idx].find('产品名称')>=0:
                    product_name=values[idx]
                if keys[idx].find('规格')>=0:
                    item.add_value('spec_type', values[idx])
                if keys[idx].find('日期')>=0:
                    item.add_value('produce_date', values[idx])
                # if keys[idx].find('结果')>=0:
                #     item.add_value('insp_res', values[idx])
                if keys[idx].find('不合格')>=0:
                    item.add_value('disq_con', values[idx])
                if keys[idx].find('承检机构')>=0:
                    item.add_value('insp_agency', values[idx])
            if product_name=='':
                product_name=(alt_title.split('批')[1]).split('产品')[0]
            item.add_value('product_name', product_name)
            item.add_value('insp_res', '不合格')
            item.add_value('release_date', response.xpath('//div[@class="xj2"]/text()').extract_first())
            item.add_value('table_name', 'spider.AQSIQ_RESULT')
            yield item.load_item()

    def closed(self, reason):
        if 'finished' == reason:
            logging.warning('%s', '爬虫程序执行结束，即将关闭')
        elif 'shutdown' == reason:
            logging.warning('%s', '爬虫进程被强制中断，即将关闭')
        elif 'cancelled' == reason:
            logging.warning('%s', '爬虫被引擎中断，即将关闭')
        else:
            logging.warning('%s', '爬虫被未知原因打断，即将关闭')

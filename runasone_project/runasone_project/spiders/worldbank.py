# -*- coding: utf-8 -*-
import scrapy
import datetime
import re, logging
from runasone_project.worldbank_items import SizeOfTheEconomyItem, WorldbankLoaderItem


class WorldbankSpider(scrapy.Spider):
    name = 'worldbank'
    allowed_domains = ['http://wdi.worldbank.org']
    start_urls = ['http://wdi.worldbank.org/table/WV.1']
    custom_settings = {
        'ITEM_PIPELINES': {
            # 'runasone_project.pipelines.ExcelPipeline': 100,     #保存到EXCEL表格
            'runasone_project.pipelines.RunasoneDB2Pipeline': 100,  # 保存到数据库
        }
    }

    batch_date = datetime.datetime.now().date()

    def parse(self, response):
        # yield scrapy.Request(url='http://wdi.worldbank.org/AjaxDownload/FileDownloadHandler.ashx?filename=WV.1_Size_of_the_economy.xls&filetype=excel', callback=self.parse_item, dont_filter=True)
        # yield scrapy.Request(
        #     url='http://wdi.worldbank.org/table/WV.1',
        #     callback=self.parse, dont_filter=True)

        # 方法一：保存到本地html
        # print(response.text)

        # 方法二：解析到xls
        year = response.xpath('//*[@id="fixedTable"]/tr[4]/th[2]/div/text()').extract_first()
        rows = response.xpath('//*[@id="scrollTable"]/tbody/tr')
        for row in rows:
            if row.xpath('./td/div/a/text()') != None:
                item = WorldbankLoaderItem(item=SizeOfTheEconomyItem(), response=response)
                item.add_value('batch_date', self.batch_date)
                item.add_value('year', year)
                item.add_value('country', row.xpath('./td/div/a/text()').extract_first())
                item.add_value('population', row.xpath('./td[2]/div/text()').extract_first())
                item.add_value('surface_area', row.xpath('./td[3]/div/text()').extract_first())
                item.add_value('population_density', row.xpath('./td[4]/div/text()').extract_first())
                item.add_value('GNI_1', row.xpath('./td[5]/div/text()').extract_first())
                item.add_value('GNI_2', row.xpath('./td[6]/div/text()').extract_first())
                item.add_value('purchasing_1', row.xpath('./td[7]/div/text()').extract_first())
                item.add_value('purchasing_2', row.xpath('./td[8]/div/text()').extract_first())
                item.add_value('GDP_1', row.xpath('./td[9]/div/text()').extract_first())
                item.add_value('GDP_2', row.xpath('./td[10]/div/text()').extract_first())
                item.add_value('table_name', 'spider.WORLDBANK_ECONOMIC_RESULT')

                logging.info("pasing row is ok,now pipeline......")
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

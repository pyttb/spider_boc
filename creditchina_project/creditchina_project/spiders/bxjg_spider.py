# -*- coding: utf-8 -*-
import scrapy,re,datetime,logging
from aqsiq_project.items import *

class BxjgSpider(scrapy.Spider):
    name = 'bxjg'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'aqsiq_project.middlewares.RandomUserAgent': 100,
        },
        'ITEM_PIPELINES': {
            'aqsiq_project.pipelines.MysqlPipeline': 100
        }
    }
    batch_date = datetime.datetime.now().date()

    allowed_domains = ['bxjg.circ.gov.cn']
    start_urls = ['http://bxjg.circ.gov.cn/web/site0/tab5240/',
                  'http://bxjg.circ.gov.cn/web/site0/tab5241/']

    def parse(self, response):
        if 'tab5240' in response.url:
            list_url = response.xpath('//span[@id="lan1"]/a/@href').extract()
            for a in list_url:
                deatil_url = 'http://bxjg.circ.gov.cn' + a
                yield scrapy.Request(url= deatil_url, callback= self.parse_item)

            nextPage = response.xpath('//td[@valign="bottom"]/a[last()-2]/@href').extract_first()
            if nextPage != None:
                pageUrl = 'http://bxjg.circ.gov.cn' + nextPage
                yield scrapy.Request(url=pageUrl, callback=self.parse, dont_filter=True)

        else:
            list_url = response.xpath('//span[@id="lan1"]/a/@href').extract()
            for a in list_url:
                deatil_url = 'http://bxjg.circ.gov.cn' + a
                print(deatil_url)
                yield scrapy.Request(url= deatil_url, callback= self.parse_item_bureau)

            nextPage = response.xpath('//td[@valign="bottom"]/a[last()-2]/@href').extract_first()
            if nextPage != None:
                pageUrl = 'http://bxjg.circ.gov.cn' + nextPage
                print(11111,pageUrl)
                yield scrapy.Request(url=pageUrl, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        item = BxjgResultItem()
        item['batch_date'] = self.batch_date
        infos = response.xpath('//table[@id="tab_content"]/tbody')
        data = response.xpath('//span[@id="zoom"]')
        info = data.xpath('string(.)').extract_first()
        r = re.compile(r'<[^>]+>', re.S)

        comp_name = re.findall('当事人：(.*?)\n', info, re.DOTALL) or re.findall('当事人：(.*?)&nbsp;', info, re.DOTALL)
        if len(comp_name) > 1:
            item['comp_name'] = comp_name[0]
            item['mine_name'] = comp_name[1]
        elif len(comp_name) == 1:
            item['comp_name'] = comp_name[0]
            item['mine_name'] = ''
        else:
            item['mine_name'] = ''
            item['comp_name'] = ''

        item['abode'] = infos.re_first('所：(.*)\n</p>') or infos.re_first('址：(.*)\n</p>')

        repres = infos.re_first('法定代表人：(.*)\n</p>')
        if repres == None:
            item['repres'] = repres
        elif '</span>' in repres:
            item['repres'] = r.sub('', repres)
        else:
            item['repres'] = repres

        item['id_number'] = infos.re_first('身份证号：(.*)\n</p>')

        duty = re.findall('职务：(.*?)\r\n', info, re.DOTALL)
        if len(duty) > 0:
            item['duty'] = duty[0]
        else:
            item['duty'] = ''

        item['refer_num'] = infos.re_first('<!--TitleStart-->(.*)<!--TitleEnd-->')

        reles_date = infos.re_first('发布时间：(.*?)分享到')
        item['reles_date'] = reles_date.replace('\xa0','')

        pun_con = re.findall('综上，我会决定作出如下处罚：(.*)<p style="text-indent:2em;">\r\n\t&nbsp;',response.text,re.DOTALL)
        if pun_con != []:
            pun_con = pun_con[0].replace('\r', '').replace('\n', '').replace('\t', '')
            item['pun_con'] = r.sub('', pun_con)
        yield item


    def parse_item_bureau(self, response):
        item = BxjgResultBureauItem()
        item['batch_date'] = self.batch_date
        print(response.url)
        infos = response.xpath('//table[@id="tab_content"]/tbody')
        data = response.xpath('//span[@id="zoom"]')
        info = data.xpath('string(.)').extract_first()

        comp_name = re.findall('当事人：(.*?)\r\n',info,re.DOTALL)
        if len(comp_name) > 1:
            item['comp_name'] = comp_name[0]
            item['mine_name'] = comp_name[1]
        elif len(comp_name) == 1:
            item['comp_name'] = ''
            item['mine_name'] = comp_name[0]
        else:
            item['mine_name'] = ''
            item['comp_name'] = ''

        abode = re.findall('址：(.*?)\r\n',info,re.DOTALL) or re.findall('所：(.*?)\r\n',info,re.DOTALL)
        if len(abode) > 0:
            item['abode'] = abode[0]
        else:
            item['abode'] = ''

        repres = re.findall('法定代表人：(.*?)\r\n',info,re.DOTALL)
        print(repres)
        if len(repres) > 0:
            item['repres'] = repres[0]
        else:
            item['repres'] = ''

        id_number = re.findall('（身份证号：(.*?)）',info,re.DOTALL) or re.findall('身份证号：(.*?)\r\n',info,re.DOTALL)
        if len(id_number) > 0:
            item['id_number'] = id_number[0]
        else:
            item['id_number'] = ''

        duty = re.findall('职务：(.*?)\r\n',info,re.DOTALL)
        if len(duty) > 0:
            item['duty'] = duty[0]
        else:
            item['duty'] = ''
        item['refer_num'] = infos.re_first('<!--TitleStart-->(.*)<!--TitleEnd-->')

        reles_date = infos.re_first('发布时间：(.*?)分享到')
        item['reles_date'] = reles_date.replace('\xa0', '')

        pun_con = re.findall('我局决定作出如下处罚：(.*)2018年',info,re.DOTALL)
        if pun_con == []:
            item['pun_con'] = ''
        else:
            item['pun_con'] = pun_con[0].replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0','')

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



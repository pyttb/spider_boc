# -*- coding: utf-8 -*-
import scrapy,re,datetime,logging

from creditchina_project.bxjg_bureau_items import BxjgBureauResultItem, BxjgBureauLoaderItem
from creditchina_project.bxjg_items import BxjgResultItem, BxjgLoaderItem


class BxjgSpider(scrapy.Spider):
    name = 'bxjg'

    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
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
                yield scrapy.Request(url= deatil_url, callback= self.parse_item_bureau)

            nextPage = response.xpath('//td[@valign="bottom"]/a[last()-2]/@href').extract_first()
            if nextPage != None:
                pageUrl = 'http://bxjg.circ.gov.cn' + nextPage
                yield scrapy.Request(url=pageUrl, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        item = BxjgLoaderItem(item=BxjgResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        infos = response.xpath('//table[@id="tab_content"]/tbody')
        data = response.xpath('//span[@id="zoom"]')
        info = data.xpath('string(.)').extract_first()
        r = re.compile(r'<[^>]+>', re.S)

        comp_name = re.findall(u'当事人：(.*?)\n', info, re.DOTALL) or re.findall(u'当事人：(.*?)&nbsp;', info, re.DOTALL)
        if len(comp_name) > 1:
            item.add_value('comp_name', comp_name[0])
            item.add_value('mine_name', comp_name[1])
        elif len(comp_name) == 1:
            item.add_value('comp_name', comp_name[0])
            item.add_value('mine_name', '')
        else:
            item.add_value('comp_name', '')
            item.add_value('mine_name', '')
        item.add_value('abode', infos.re_first(u'所：(.*)\n</p>') or infos.re_first(u'址：(.*)\n</p>'))

        repres = infos.re_first(u'法定代表人：(.*)\n</p>')
        if repres == None:
            item.add_value('repres', repres)
        elif '</span>' in repres:
            item.add_value('repres', r.sub('', repres))
        else:
            item.add_value('repres', repres)
        item.add_value('id_number', infos.re_first(u'身份证号：(.*)\n</p>'))

        duty = re.findall(u'职务：(.*?)\r\n', info, re.DOTALL)
        if len(duty) > 0:
            item.add_value('duty', duty[0])
        else:
            item.add_value('duty', '')
        item.add_value('refer_num', infos.re_first(u'<!--TitleStart-->(.*)<!--TitleEnd-->'))
        reles_date = infos.re_first(u'发布时间：(.*?)分享到')
        item.add_value('reles_date', reles_date)
        pun_con = re.findall(u'综上，我会决定作出如下处罚：(.*)<p style="text-indent:2em;">\r\n\t&nbsp;',response.text,re.DOTALL)
        if pun_con != []:
            pun_con = pun_con[0].replace('\r', '').replace('\n', '').replace('\t', '')
            item.add_value('pun_con', r.sub('', pun_con))
        item.add_value('table_name', 'SPIDER.BXJG_RESULT')
        yield item.load_item()


    def parse_item_bureau(self, response):
        item = BxjgBureauLoaderItem(item=BxjgBureauResultItem(), response=response)
        item.add_value('batch_date', self.batch_date)
        infos = response.xpath('//table[@id="tab_content"]/tbody')
        data = response.xpath('//span[@id="zoom"]')
        info = data.xpath('string(.)').extract_first()

        comp_name = re.findall(u'当事人：(.*?)\r\n',info,re.DOTALL)
        if len(comp_name) > 1:
            item.add_value('comp_name', comp_name[0])
            item.add_value('mine_name', comp_name[1])
        elif len(comp_name) == 1:
            item.add_value('comp_name', '')
            item.add_value('mine_name', comp_name[0])
        else:
            item.add_value('comp_name', '')
            item.add_value('mine_name', '')

        abode = re.findall(u'址：(.*?)\r\n',info,re.DOTALL) or re.findall(u'所：(.*?)\r\n',info,re.DOTALL)
        if len(abode) > 0:
            item.add_value('abode', abode[0])
        else:
            item.add_value('abode', '')

        repres = re.findall(u'法定代表人：(.*?)\r\n',info,re.DOTALL)
        if len(repres) > 0:
            item.add_value('repres', repres[0])
        else:
            item.add_value('repres', '')

        id_number = re.findall(u'（身份证号：(.*?)）',info,re.DOTALL) or re.findall(u'身份证号：(.*?)\r\n',info,re.DOTALL)
        if len(id_number) > 0:
            item.add_value('id_number', id_number[0])
        else:
            item.add_value('id_number', '')

        duty = re.findall(u'职务：(.*?)\r\n',info,re.DOTALL)
        if len(duty) > 0:
            item.add_value('duty', duty[0])
        else:
            item.add_value('duty', '')
        item.add_value('refer_num', infos.re_first(u'<!--TitleStart-->(.*)<!--TitleEnd-->'))
        reles_date = infos.re_first(u'发布时间：(.*?)分享到')
        item.add_value('reles_date', reles_date)
        pun_con = re.findall(u'我局决定作出如下处罚：(.*)2018年',info,re.DOTALL)
        if pun_con == []:
            item.add_value('pun_con', '')
        else:
            item.add_value('pun_con', pun_con[0].replace('\r', '').replace('\n', '').replace('\t', ''))
        item.add_value('table_name', 'SPIDER.BXJG_BUREAU_RESULT')
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



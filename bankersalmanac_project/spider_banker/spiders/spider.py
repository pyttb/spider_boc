# -*- coding: utf-8 -*-

import scrapy
import re
import xlrd
import os
import sys
try:
    from urllib import parse as urlparse
except:
    import urlparse
from spider_banker.items import BankerListInfoItem, BankLoaderItem, BankDetailsInfoItem, BankCreditInfoItem, BankSsiItem
import logging
import datetime
from bs4 import BeautifulSoup
import bs4


class SpiderSpider(scrapy.Spider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'banker'
    allowed_domains = ['www.bankersalmanac.com']
    start_urls = []

    path = os.path.abspath(os.path.dirname(__file__))
    data = xlrd.open_workbook(path + '/bankers_cust_list.xlsx')
    sheet = data.sheet_by_index(0)
    sheet.col_values(0, 1)
    codes = sheet.col_values(0)
    list_url = 'https://www.bankersalmanac.com/private/qsresults.aspx?searchtype=swift&swfcode='
    for i in range(0, len(codes)-2):
        start_urls.append(list_url + codes[i+1])

    def start_requests(self):
        '''
        进入查询页面
        :return:
        '''
        # 模块测试：
        # qry_date = datetime.datetime.now().date()
        # yield scrapy.Request(
        #     url='file:///Users/jiachengyu/Downloads/temp/Bankersalmanac.com-AustraliaandNewZealandBankingGroupLimited-FullDetails.htm',
        #     meta={'qry_date': qry_date, 'bank_swift': 'ANCDEFGH'},
        #     callback=self.parse_details
        # )

        # 程序入口：
        return [scrapy.Request(
            url="https://www.bankersalmanac.com/private/seaban.aspx?menu=search",
            callback=self.start_login
        )]

    def start_login(self, response):
        '''
        开始登录
        :param response:
        :return:
        '''
        #bocom122 bocom1

        match_obj = re.match('.*name="ReturnUrl" value="(.*?)"', response.text, re.DOTALL)
        return_url = ''
        if match_obj:
            return_url = match_obj.group(1)
        return [scrapy.FormRequest(
            url="https://www.bankersalmanac.com/securityCheck.ashx?redir=",
            formdata={'ReturnUrl': return_url, 'Username': 'bocom1', 'Password': 'Happy2017', 'x': '14', 'y': '10'},
            callback=self.check_status
        )]

    def check_status(self, response):
        '''
        检测登录状态
        :param response:
        :return:
        '''
        if 'already logged in' in response.text:
            self.log(message='登录失败，用户已登录', level=logging.INFO)
        elif 'Invalid Username Or Password' in response.text:
            self.log(message='登录失败，用户或密码错误', level=logging.INFO)
        elif 'Bankersalmanac.com - Log-in to Bankersalmanac.com' in response.text:
            self.log(message='登录失败，重新登录', level=logging.ERROR)
        elif 'Bankersalmanac.com - Institution Search' in response.text:
            self.log(message='登录成功', level=logging.INFO)
            for url in self.start_urls:
                self.log(message=url, level=logging.INFO)
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            self.log(message='登录失败，状态未知', level=logging.ERROR)

    def parse(self, response):
        '''
        解析列表信息
        :param response:
        :return:
        '''
        title = response.xpath('//title/text()').extract_first('').strip()
        if response.status == 200 and 'Institution Search results for SWIFT/BIC' in title:
            # 获取当前日期
            qry_date = datetime.datetime.now().date()
            # 获取查询条件中的swift
            match_obj = re.match('Institution Search results for SWIFT/BIC (.*)', title)
            swift = ''
            if match_obj:
                swift = match_obj.group(1)
            # 解析列表中信息
            divs1 = response.xpath('//div[@class="ResultsInner IBANShow"]')
            # 解析隐藏列表中信息
            divs2 = response.xpath('//div[@class="ResultsInner IBANHide"]')
            divs = []
            if divs1:
                for div in divs1:
                    divs.append(div)
            if divs2:
                for div in divs2:
                    divs.append(div)
            if divs:
                for div in divs:
                    list_item = BankLoaderItem(item=BankerListInfoItem(), response=response)
                    bank_name = div.xpath('.//th/b/a/text()').extract_first('').strip()
                    if not bank_name:
                        bank_name = div.xpath('.//th/a/text()').extract_first('').strip()
                    list_item.add_value('qry_date', qry_date)
                    list_item.add_value('bank_name', bank_name)
                    list_item.add_value('bank_type', div.xpath('.//table/tr[2]/td[2]/text()').extract_first('').strip())
                    list_item.add_value('bank_location', div.xpath('.//table/tr[3]/td[2]/a/text()').extract_first('').strip())
                    list_item.add_value('bank_country', div.xpath('.//table/tr[4]/td[2]/a/text()').extract_first('').strip())
                    list_item.add_value('bank_swift', div.xpath('.//table/tr[5]/td[2]/text()').extract_first('').strip())
                    list_item.add_value('swift', swift)
                    item = list_item.load_item()
                    yield item
            # 获取机构详情页面的URL，并添加到爬取队列中
            as_tag = response.xpath('//a[@tabindex="1"]')
            for a_tag in as_tag:
                if a_tag:
                    url = a_tag.css('::attr("href")').extract_first('').strip().replace('\r\n', '').replace('\t', '')
                    url_link = urlparse.urljoin(response.url, url)
                    yield scrapy.Request(
                        url=url_link,
                        meta={'details_url': url_link, 'qry_date': qry_date},
                        callback=self.get_full_details)
                else:
                    print('a标签为空')
            # 判断是否需要翻页
            next_page = response.xpath('//a[@tabindex="2"]')
            if next_page:
                self.log(message='下一页', level=logging.INFO)
                url = next_page[0].css('::attr("href")').extract_first('').strip().replace('\r\n', '').replace('\t', '')
                yield scrapy.Request(url=urlparse.urljoin(response.url, url), callback=self.parse)
            else:
                self.log(message='不需要翻页', level=logging.INFO)
        else:
            print('根据SWIFT查询列表信息失败')

    def get_full_details(self, response):
        '''
        获取full details详情页面
        :param response:
        :return:
        '''
        qry_date = response.meta.get('qry_date', '')
        # 获取详情页面对应的机构代码
        details_url = response.meta.get('details_url', '')
        bank_swift = re.match('.*swift=(.*?)#focus', details_url).group(1)

        flag = True
        as_tag = response.xpath('//a[@tabindex="1"]')
        for a_tag in as_tag:
            if 'Full Details' == a_tag.xpath('./text()').extract_first(''):
                flag = False
                url = a_tag.css('::attr("href")').extract_first('').strip().replace('\r\n', '').replace('\t', '')
                url_link = urlparse.urljoin(response.url, url)
                yield scrapy.Request(
                    url=url_link,
                    meta={'qry_date': qry_date, 'bank_swift': bank_swift},
                    callback=self.parse_details)
        if flag:
            yield scrapy.Request(
                url=details_url,
                meta={'qry_date': qry_date, 'bank_swift': bank_swift},
                callback=self.parse_details)

    def parse_details(self, response):
        '''
        解析详细信息
        :param response:
        :return:
        '''
        qry_date = response.meta.get('qry_date', '')
        bank_swift = response.meta.get('bank_swift', '')

        info_item = BankLoaderItem(item=BankDetailsInfoItem(), response=response)

        info_item.add_value('qry_date', qry_date)
        info_item.add_value('bank_swift', bank_swift)

        # mainaddress printsection
        head_obj = response.xpath('//div[@class="mainaddress printsection"]')
        if head_obj:
            for detail in head_obj.xpath('.//div[@class="ContactDetails"]'):
                if 'Head Office' in detail.xpath('./strong/text()').extract_first(''):
                    for tr in detail.xpath('./table/tr'):
                        if 'Website' in tr.xpath('./td[1]/text()').extract_first(''):
                            bank_website = tr.xpath('./td[2]/text()').extract_first('')
                            if not bank_website:
                                bank_website = tr.xpath('./td[2]/a/text()').extract_first('')
                            info_item.add_value('bank_website', bank_website)
                if 'Postal Address' in detail.xpath('./strong/text()').extract_first(''):
                    postal_address = detail.xpath('./address/text()').extract()
                    info_item.add_value('postal_address', postal_address)

        # StatusSection printsection
        if response.xpath('//tr[@class="ranks"]'):
            info_item.add_xpath('world_rank', '//tr[@class="ranks"]/td[2]/a[1]/text()')
            info_item.add_xpath('country_rank', '//tr[@class="ranks"]/td[2]/a[2]/text()')
        if response.xpath('//tr[@class="ownertype"]'):
            info_item.add_xpath('owner_ship', '//tr[@class="ownertype"]/td[2]/text()')

        # history printsection
        if response.xpath('//div[@class="history printsection"]'):
            info_item.add_xpath('history', '//div[@class="history printsection"]/div/div/p/text()')
        item = info_item.load_item()
        yield item

        # creditrating printsection
        credit_div = response.xpath('//div[@class="creditrating printsection"]')
        if credit_div:
            for div in credit_div:
                for tr in div.xpath('.//table/tr'):
                    if tr.xpath('./td[1]/a/text()'):
                        credit_item = BankLoaderItem(item=BankCreditInfoItem(), response=response)
                        credit_name = tr.xpath('./td[1]/a/text()').extract_first('').strip()
                        long_term = tr.xpath('./td[2]/text()').extract_first('').strip()
                        short_term = tr.xpath('./td[3]/text()').extract_first('').strip()

                        credit_item.add_value('qry_date', qry_date)
                        credit_item.add_value('bank_swift', bank_swift)
                        credit_item.add_value('credit_name', credit_name)
                        credit_item.add_value('long_term', long_term)
                        credit_item.add_value('short_term', short_term)
                        item = credit_item.load_item()
                        yield item

        # # SSI printsection
        ssi_obj = response.xpath('//div[@class="SSI printsection"]')
        if ssi_obj:
            for tr in ssi_obj.xpath('.//table/tr'):
                ssi_item = BankLoaderItem(item=BankSsiItem(), response=response)
                currency = tr.xpath('./td[1]/text()').extract_first('').strip()
                bank = tr.xpath('./td[2]/a/text()').extract_first('').strip() + \
                       tr.xpath('./td[2]/text()').extract_first('').strip()
                swift_bic = tr.xpath('./td[3]/text()').extract_first('').strip()
                account_no = tr.xpath('./td[4]/text()').extract_first('').strip()
                ssikeycolumn_cp = tr.xpath('./td[5]/text()').extract_first('').strip()
                ssikeycolumn_fx = tr.xpath('./td[6]/text()').extract_first('').strip()
                ssikeycolumn_mm = tr.xpath('./td[7]/text()').extract_first('').strip()
                other = tr.xpath('./td[8]/text()').extract_first('').strip()

                ssi_item.add_value('qry_date', qry_date)
                ssi_item.add_value('bank_swift', bank_swift)
                ssi_item.add_value('currency', currency)
                ssi_item.add_value('bank', bank)
                ssi_item.add_value('swift_bic', swift_bic)
                ssi_item.add_value('account_no', account_no)
                ssi_item.add_value('ssikeycolumn_cp', ssikeycolumn_cp)
                ssi_item.add_value('ssikeycolumn_fx', ssikeycolumn_fx)
                ssi_item.add_value('ssikeycolumn_mm', ssikeycolumn_mm)
                ssi_item.add_value('other', other)
                item = ssi_item.load_item()
                yield item

        # Personnel
        soup = BeautifulSoup(response.text, 'lxml')
        person_obj = soup.find('div', 'personnel printsection')
        if person_obj:
            div_tag = person_obj.find('div', 'DetailsSectionInner')
            if div_tag and isinstance(div_tag, bs4.element.Tag):
            # for div_tag in person_obj.find_all('div', 'DetailsSectionInner'):
                if div_tag.find('p') and isinstance(div_tag.find('p'), bs4.element.Tag):
                    mark_info = div_tag.find('p').string.strip()
                    next_tag = div_tag.find('p').next_sibling
                elif div_tag.find('h5') and isinstance(div_tag.find('h5'), bs4.element.Tag):
                    next_tag = div_tag.find('h5')
                elif div_tag.find('Group1') and isinstance(div_tag.find('Group1'), bs4.element.Tag):
                    next_tag = div_tag.find('Group1')
                dept_name = ''
                while(True):
                    if 'h5' == next_tag.name:
                        dept_name = next_tag.string.strip()
                    if 'Group1' in next_tag.attrs['class'] or 'Group2' in next_tag.attrs['class']:
                        for num in xrange(0, len(next_tag.find_all('h6'))):
                            department = next_tag.find_all('h6')[num].string.strip()
                            pernm = next_tag.find_all('strong')[num].string.strip()
                            if 'span' == next_tag.find_all('strong')[num].next_sibling.name:
                                pernm = pernm + ' ' + next_tag.find_all('strong')[num].next_sibling.string.strip()
                            if 'br' == next_tag.find_all('strong')[num].next_sibling.name:
                                pernm = pernm + ' ' + next_tag.find_all('strong')[num].next_sibling.next_sibling.string.strip()
                            if 'table' == next_tag.find_all('strong')[num].next_sibling.name:
                                table_tag = next_tag.find_all('strong')[num].next_sibling
                                for tr in table_tag.find_all('tr'):
                                    if 'tel' == tr.attrs['class']:
                                        tel = tr.find_all('td')[1].string.strip()
                                        if not tel:
                                            tel = tr.find('td').string.strip()
                                    elif 'email' == tr.attrs['class']:
                                        email = tr.find('a').string.strip()
                                    else:
                                        ot = tr.find('a').string.strip()
                                        if not ot:
                                            ot = tr.find('td').string.strip()
                    next_tag = next_tag.next_sibling
                    if 'FloatWithIn' in next_tag.attrs['class']:
                        break
                    else:
                        continue

        # person_obj = response.xpath('//div[@class="personnel printsection"]')
        # if person_obj:
        #     for num in xrange(0, len(person_obj.xpath('.//div[@class="DetailsSectionInner"]'))):
        #         if person_obj.xpath('.//div[@class="DetailsSectionInner"]/h5'):
        #             dept_name  = person_obj.xpath('.//div[@class="DetailsSectionInner"]/h5')[num].xpath('./text()').extract_first('').strip()
        #         if person_obj.xpath('.//div[@class="Group1"]') or person_obj.xpath('.//div[@class="Group2"]'):
        #             if person_obj.xpath('.//div[@class="Group1"]'):
        #                 group = person_obj.xpath('.//div[@class="Group1"]')[num]
        #             else:
        #                 group = person_obj.xpath('.//div[@class="Group2"]')[num]
        #             for i in xrange(0, len(group.xpath('./h6'))):
        #                 department = group.xpath('./h6')[i].xpath('./text()').extract()
        #                 pernm = group.xpath('./strong')[i].xpath('./text()').extract()
        #                 if group.xpath('./table/tbody'):
        #                     for tr in group.xpath('./table/tbody/tr'):
        #                         title = tr.xpath('./td[1]/text()').extract_first('').strip()
        #                         value = tr.xpath('./td[2]/text()').extract_first('').strip()
        #                         if not value:
        #                             value = tr.xpath('./td[2]/a/text()').extract_first('').strip()

    def close(spider, reason):
        '''
        爬虫结束时退出登录状态
        :param reason:
        :return:
        '''
        if 'finished' == reason:
            print('爬虫程序执行结束，即将关闭')
        elif 'shutdown' == reason:
            print('爬虫进程被强制中断，即将关闭')
        elif 'cancelled' == reason:
            print('爬虫被引擎中断，即将关闭')
        else:
            print('爬虫被未知原因打断，即将关闭')
        # scrapy.Request(url="https://www.bankersalmanac.com/upplogout.aspx")
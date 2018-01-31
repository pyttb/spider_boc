# -*- coding: utf-8 -*-
import os
import random
import urllib
import time
import datetime
import scrapy
import sys
import xlrd

from creditchina_project.items import CreditchinaLoaderItem, PubPermissionsNameItem, RecordParamRedItem, RecordParamAttentionItem, DishonestyBlacklistItem, SeriousRevenueLawlessCustListItem, PurchasingBadnessRecordItem

reload(sys)
sys.setdefaultencoding('utf-8')
class CreditChinaSpider(scrapy.Spider):
    name = "creditchina"
    allowed_domains = ['www.creditchina.gov.cn']
    creditchina_cust_path = os.path.abspath(os.path.dirname(__file__))
    creditchina_cust_data = xlrd.open_workbook(creditchina_cust_path + '/creditchina.xlsx')
    creditchina_cust_sheet = creditchina_cust_data.sheet_by_index(0)
    creditchina_cust_sheet.col_values(0, 1)
    creditchina_cust_list = creditchina_cust_sheet.col_values(0, start_rowx=1)
    total_len=len(creditchina_cust_list)
    def start_requests(self):
        current_len=0
        for creditchina_cust in self.creditchina_cust_list:
            current_len=current_len+1
            msg= 'Current search cust is '+creditchina_cust+' ('+str(current_len)+'/'+str(self.total_len)+') '
            self.logger.warning('%s', msg)
            time.sleep(random.uniform(3,5))
            default_data = {
                'keyword': '%s' % creditchina_cust,
                'searchtype': '0',
                'objectType': '2',
                'areas': '',
                'creditType': '',
                'dataType': '1',
                'areaCode': '',
                'templateId': '',
                'exact': '0',
                'page': '1',
                'pageSize': '10'
            }
            default_headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
                'Proxy-Connection': 'keep-alive',
                'RA-Sid': 's_858_r2x9ak474125_270',
                'RA-Ver': '3.3.0',
                'Cookie': 'Hm_lvt_0076fef7e919d8d7b24383dc8f1c852a=1515074986,1515113646; browseHistory=%5B%7B%22name%22%3A%22%E6%B9%96%E5%8C%97%E7%B3%96%E6%9F%9C%E9%A3%9F%E5%93%81%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22fXt3cnl5bTZqUXk%3D%5Cn%22%7D%2C%7B%22name%22%3A%22a%22%2C%22encryStr%22%3A%22cTFqS0F3dzFtZ2Y%3D%5Cn%22%7D%2C%7B%22name%22%3A%22a%22%2C%22encryStr%22%3A%22MnkwOXYseWk7ZnQ%3D%5Cn%22%7D%2C%7B%22name%22%3A%22a%22%2C%22encryStr%22%3A%22MnkwUWcsdHtzZHQ%3D%5Cn%22%7D%2C%7B%22name%22%3A%22%E6%B5%99%E6%B1%9F%E4%BC%81%E6%88%90%E6%9C%BA%E6%A2%B0%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22Mm15Zixva3dubns%3D%5Cn%22%7D%2C%7B%22name%22%3A%22%E6%B5%99%E6%B1%9F%E4%BC%81%E6%88%90%E6%9C%BA%E6%A2%B0%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22cXAxZix1bztubjA%3D%5Cn%22%7D%2C%7B%22name%22%3A%22%E5%AE%89%E5%BE%BD%E9%AB%98%E5%B1%B1%E8%8D%AF%E4%B8%9A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22ejFncFsscTI0eVE%3D%5Cn%22%7D%5D; Hm_lpvt_0076fef7e919d8d7b24383dc8f1c852a=1515155482',
                'Host': 'www.creditchina.gov.cn',
                'Origin': 'http://www.creditchina.gov.cn',
                'Referer': 'http://www.creditchina.gov.cn/api/credit_info_search',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36HH=20Runtime=kecekldmfbcpjfmnnijdjhcggpcnkpbhALICDN/ DOL/HELLO_GWF_s_858_r2x9ak474125_270',
                'X-Requested-With': 'XMLHttpRequest',
            }
            default_data = urllib.urlencode(default_data)
            yield scrapy.Request(url='http://www.creditchina.gov.cn/api/credit_info_search?keyword='+creditchina_cust+'&templateId=&page=1&pageSize=10', headers=default_headers, body=default_data, callback=self.parse_basic_info, meta={'cust':creditchina_cust}, dont_filter = True)

    def parse_basic_info(self, response):
        basic_info = response.text
        if eval(basic_info.replace('null', 'None').replace('false', 'None')).get('msg'):
            msg = eval(basic_info.replace('null', 'None').replace('false', 'None'))
            self.logger.warning('%s', msg)
            status=eval(basic_info.replace('null', 'None').replace('false', 'None'))['msg']
            if status=='访问受限':
                self.logger.warning('%s', '访问受限，睡眠30秒')
                time.sleep(random.uniform(30, 60))
        cust=response.meta['cust']
        total_page_count=eval(basic_info.replace('null', 'None').replace('false', 'None'))['data']['totalPageCount']
        for page in range(1, total_page_count + 1):
            detail_url = 'http://www.creditchina.gov.cn/api/credit_info_search?keyword=' + cust + '&templateId=&page=' + str(page) + '&pageSize=10'
            data = {
                'keyword': '%s' % cust,
                'searchtype': '0',
                'objectType': '2',
                'areas': '',
                'creditType': '',
                'dataType': '1',
                'areaCode': '',
                'templateId': '',
                'exact': '0',
                'page': '%s' % page,
                'pageSize': '10'
            }
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
                'Proxy-Connection': 'keep-alive',
                'RA-Sid': 's_858_r2x9ak474125_270',
                'RA-Ver': '3.3.0',
                'Cookie': 'Hm_lvt_0076fef7e919d8d7b24383dc8f1c852a=1515074986,1515113646; browseHistory=%5B%7B%22name%22%3A%22%E6%B9%96%E5%8C%97%E7%B3%96%E6%9F%9C%E9%A3%9F%E5%93%81%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22fXt3cnl5bTZqUXk%3D%5Cn%22%7D%2C%7B%22name%22%3A%22a%22%2C%22encryStr%22%3A%22cTFqS0F3dzFtZ2Y%3D%5Cn%22%7D%2C%7B%22name%22%3A%22a%22%2C%22encryStr%22%3A%22MnkwOXYseWk7ZnQ%3D%5Cn%22%7D%2C%7B%22name%22%3A%22a%22%2C%22encryStr%22%3A%22MnkwUWcsdHtzZHQ%3D%5Cn%22%7D%2C%7B%22name%22%3A%22%E6%B5%99%E6%B1%9F%E4%BC%81%E6%88%90%E6%9C%BA%E6%A2%B0%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22Mm15Zixva3dubns%3D%5Cn%22%7D%2C%7B%22name%22%3A%22%E6%B5%99%E6%B1%9F%E4%BC%81%E6%88%90%E6%9C%BA%E6%A2%B0%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22cXAxZix1bztubjA%3D%5Cn%22%7D%2C%7B%22name%22%3A%22%E5%AE%89%E5%BE%BD%E9%AB%98%E5%B1%B1%E8%8D%AF%E4%B8%9A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22encryStr%22%3A%22ejFncFsscTI0eVE%3D%5Cn%22%7D%5D; Hm_lpvt_0076fef7e919d8d7b24383dc8f1c852a=1515155482',
                'Host': 'www.creditchina.gov.cn',
                'Origin': 'http://www.creditchina.gov.cn',
                'Referer': 'http://www.creditchina.gov.cn/api/credit_info_search',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36HH=20Runtime=kecekldmfbcpjfmnnijdjhcggpcnkpbhALICDN/ DOL/HELLO_GWF_s_858_r2x9ak474125_270',
                'X-Requested-With': 'XMLHttpRequest',
            }
            data = urllib.urlencode(data)
            yield scrapy.Request(url=detail_url, headers=headers, body=data, callback=self.parse_detail_info, meta={'cust': cust}, dont_filter = True)
    def parse_detail_info(self, response):
        detail_info = response.text
        cust = response.meta['cust']
        if eval(detail_info.replace('null', 'None').replace('false', 'None').replace('true', 'None')).get('msg'):
            self.logger.warning('%s',  cust + ' occurred err!')
            self.logger.warning('%s', eval(detail_info.replace('null', 'None').replace('false', 'None').replace('true', 'None')))
        results = eval(detail_info.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['data']['results']
        credit_info_detail_url = "http://www.creditchina.gov.cn/api/credit_info_detail?"
        pub_permissions_name_url = 'http://www.creditchina.gov.cn/api/pub_permissions_name?'
        pub_penalty_name_url = 'http://www.creditchina.gov.cn/api/pub_penalty_name?'
        record_param_url = 'http://www.creditchina.gov.cn/api/record_param?'
        credit_info_detail_list = []
        pub_permissions_name_list = []
        pub_penalty_name_list = []
        record_param_list_2 = []
        record_param_list_4 = []
        record_param_list_8 = []
        hasResults=False
        for result in results:
            if result['name'] != cust:
                continue
            hasResults=True
            # summary
            credit_info_detail_url_append = {'encryStr': result['encryStr'].replace('\n', '')}
            credit_info_detail_url_append = urllib.urlencode(credit_info_detail_url_append)
            credit_info_detail_list.append(credit_info_detail_url + credit_info_detail_url_append)
            credit_info_detail_list = list(set(credit_info_detail_list))
            # pub_permissions
            pub_permissions_name_url_append = {'name': cust, 'page': 1, 'pageSize': 50}
            pub_permissions_name_url_append = urllib.urlencode(pub_permissions_name_url_append)
            pub_permissions_name_list.append(pub_permissions_name_url + pub_permissions_name_url_append)
            pub_permissions_name_list = list(set(pub_permissions_name_list))
            # pub_penalty
            pub_penalty_name_url_append = {'name': cust, 'page': 1, 'pageSize': 50}
            pub_penalty_name_url_append = urllib.urlencode(pub_penalty_name_url_append)
            pub_penalty_name_list.append(pub_penalty_name_url + pub_penalty_name_url_append)
            pub_penalty_name_list = list(set(pub_penalty_name_list))
            # creditType=2 red,creditType=4 attention,creditType=8 black
            record_param_url_append_2 = {'encryStr': result['encryStr'].replace('\n', ''), 'creditType': 2,
                                         'dataSource': 0, 'pageNum': 1, 'pageSize': 50}
            record_param_url_append_2 = urllib.urlencode(record_param_url_append_2)
            record_param_list_2.append(record_param_url + record_param_url_append_2)
            record_param_list_2 = list(set(record_param_list_2))
            record_param_url_append_4 = {'encryStr': result['encryStr'].replace('\n', ''), 'creditType': 4,
                                         'dataSource': 0, 'pageNum': 1, 'pageSize': 50}
            record_param_url_append_4 = urllib.urlencode(record_param_url_append_4)
            record_param_list_4.append(record_param_url + record_param_url_append_4)
            record_param_list_4 = list(set(record_param_list_4))
            record_param_url_append_8 = {'encryStr': result['encryStr'].replace('\n', ''), 'creditType': 8,
                                         'dataSource': 0, 'pageNum': 1, 'pageSize': 50}
            record_param_url_append_8 = urllib.urlencode(record_param_url_append_8)
            record_param_list_8.append(record_param_url + record_param_url_append_8)
            record_param_list_8 = list(set(record_param_list_8))
        if hasResults==False:
            self.logger.warning('%s', cust + ' no results!')
        if pub_permissions_name_list != []:
            for url in pub_permissions_name_list:
                time.sleep(random.uniform(1, 3))
                yield scrapy.Request(url=url, callback=self.parse_pub_permissions_name,meta={'cust': cust}, dont_filter = True)
        if record_param_list_2 != []:
            for url in record_param_list_2:
                time.sleep(random.uniform(1, 3))
                yield scrapy.Request(url=url, callback=self.parse_record_param_url_append_2,meta={'cust': cust}, dont_filter = True)
        if record_param_list_4 != []:
            for url in record_param_list_4:
                time.sleep(random.uniform(1, 3))
                yield scrapy.Request(url=url, callback=self.parse_record_param_url_append_4,meta={'cust': cust}, dont_filter = True)
        if record_param_list_8 != []:
            for url in record_param_list_8:
                time.sleep(random.uniform(1, 3))
                yield scrapy.Request(url=url, callback=self.parse_record_param_url_append_8,meta={'cust': cust}, dont_filter = True)
    def parse_pub_permissions_name(self, response):
        batch_date = datetime.datetime.now().date()
        cust = response.meta['cust']
        resp=response.text
        if eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')).get('msg'):
            self.logger.warning('%s', cust + ' occurred err!')
            self.logger.warning('%s', eval(
                resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')))
        results = eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['result']['results']
        if results!=None and len(results)>0:
            for result in results:
                item = CreditchinaLoaderItem(item=PubPermissionsNameItem(), response=response)
                item.add_value('batch_date', batch_date)
                item.add_value('cust_name', cust)
                item.add_value('adm_license_writ_no', result['xkWsh'])
                item.add_value('audit_type', result['xkSplb'])
                item.add_value('legal_person', result['xkFr'])
                item.add_value('content', result['xkNr'])
                item.add_value('permit_validity', result['xkYxq'])
                item.add_value('permit_decision_date', result['xkJdrq'])
                item.add_value('permit_issue_date', result['xkJzq'])
                item.add_value('local_code', result['xkDfbm'])
                item.add_value('permit_org', result['xkXzjg'])
                item.add_value('data_update_date', result['xkSjc'])
                item.add_value('table_name', 'pub_permissions_name')
                yield item.load_item()
        else:
            item = CreditchinaLoaderItem(item=PubPermissionsNameItem(), response=response)
            item.add_value('batch_date', batch_date)
            item.add_value('cust_name', cust)
            item.add_value('adm_license_writ_no', '')
            item.add_value('audit_type', '')
            item.add_value('legal_person', '')
            item.add_value('content', '')
            item.add_value('permit_validity', '')
            item.add_value('permit_decision_date', '')
            item.add_value('permit_issue_date', '')
            item.add_value('local_code', '')
            item.add_value('permit_org', '')
            item.add_value('data_update_date', '')
            item.add_value('table_name', 'pub_permissions_name')
            yield item.load_item()
    #red
    def parse_record_param_url_append_2(self, response):
        batch_date = datetime.datetime.now().date()
        cust = response.meta['cust']
        resp=response.text
        results=None
        if eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')).get('msg'):
            self.logger.warning('%s', cust + ' occurred err!')
            self.logger.warning('%s', eval(
                resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')))
        else:
            results = eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['result']
        if results!=None and len(results)>0:
            for result in results:
                if result['数据类别'] == 'A级纳税人':
                    item = CreditchinaLoaderItem(item=RecordParamRedItem(), response=response)
                    item.add_value('batch_date', batch_date)
                    item.add_value('cust_name', cust)
                    item.add_value('data_source', result['数据来源'])
                    item.add_value('no', result['序号'])
                    item.add_value('taxpayer_name', result['纳税人名称'])
                    item.add_value('rating_year', result['评价年度'])
                    item.add_value('data_update_date', result['最新更新日期'])
                    item.add_value('table_name', 'cust_red_list')
                    yield item.load_item()
                else:
                    self.logger.warning('parse_record_param_url_append_2 has a new type: %s', result['数据类别'])
                    item = CreditchinaLoaderItem(item=RecordParamRedItem(), response=response)
                    item.add_value('batch_date', batch_date)
                    item.add_value('cust_name', cust)
                    item.add_value('data_source', '')
                    item.add_value('no', '')
                    item.add_value('taxpayer_name', '')
                    item.add_value('rating_year', '')
                    item.add_value('data_update_date', '')
                    item.add_value('table_name', 'cust_red_list')
                    yield item.load_item()
        else:
            item = CreditchinaLoaderItem(item=RecordParamRedItem(), response=response)
            item.add_value('batch_date', batch_date)
            item.add_value('cust_name', cust)
            item.add_value('data_source', '')
            item.add_value('no', '')
            item.add_value('taxpayer_name', '')
            item.add_value('rating_year', '')
            item.add_value('data_update_date', '')
            item.add_value('table_name', 'cust_red_list')
            yield item.load_item()

    def parse_record_param_url_append_4(self, response):
        batch_date = datetime.datetime.now().date()
        cust = response.meta['cust']
        resp=response.text
        if eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')).get('msg'):
            self.logger.warning('%s', cust + ' occurred err!')
            self.logger.warning('%s', eval(
                resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')))
        results = eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['result']
        if results!=None and len(results)>0:
            for result in results:
                if result['数据类别'] == '异常名录':
                    item = CreditchinaLoaderItem(item=RecordParamAttentionItem(), response=response)
                    item.add_value('batch_date', batch_date)
                    item.add_value('cust_name', cust)
                    item.add_value('data_source', result['数据来源'])
                    item.add_value('comp_name', result['企业名称'])
                    item.add_value('reg_no', result['注册号'])
                    item.add_value('legal_person', result['法定代表人'])
                    item.add_value('exception_reason_type', result['列入经营异常名录原因类型名称'])
                    item.add_value('set_date', result['设立日期'])
                    item.add_value('org_name', result['列入决定机关名称'])
                    item.add_value('data_update_date', result['最新更新日期'])
                    item.add_value('table_name', 'cust_attention_list')
                    yield item.load_item()
                else:
                    self.logger.warning('parse_record_param_url_append_4 has a new type: %s', result['数据类别'])
                    item = CreditchinaLoaderItem(item=RecordParamAttentionItem(), response=response)
                    item.add_value('batch_date', batch_date)
                    item.add_value('cust_name', cust)
                    item.add_value('data_source', '')
                    item.add_value('comp_name', '')
                    item.add_value('reg_no', '')
                    item.add_value('legal_person', '')
                    item.add_value('exception_reason_type', '')
                    item.add_value('set_date', '')
                    item.add_value('org_name', '')
                    item.add_value('data_update_date', '')
                    item.add_value('table_name', 'cust_attention_list')
                    yield item.load_item()
        else:
            item = CreditchinaLoaderItem(item=RecordParamAttentionItem(), response=response)
            item.add_value('batch_date', batch_date)
            item.add_value('cust_name', cust)
            item.add_value('data_source', '')
            item.add_value('comp_name', '')
            item.add_value('reg_no', '')
            item.add_value('legal_person', '')
            item.add_value('exception_reason_type', '')
            item.add_value('set_date', '')
            item.add_value('org_name', '')
            item.add_value('data_update_date', '')
            item.add_value('table_name', 'cust_attention_list')
            yield item.load_item()

    def parse_record_param_url_append_8(self, response):
        batch_date = datetime.datetime.now().date()
        cust = response.meta['cust']
        resp=response.text
        if eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')).get('msg'):
            self.logger.warning('%s', cust + ' occurred err!')
            self.logger.warning('%s', eval(
                resp.replace('null', 'None').replace('false', 'None').replace('true', 'None')))
        results = eval(resp.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['result']
        if results!=None and len(results)>0:
            for result in results:
                if result['数据类别'] == '失信黑名单-法人':
                    item_DishonestyBlacklist = CreditchinaLoaderItem(item=DishonestyBlacklistItem(), response=response)
                    item_DishonestyBlacklist.add_value('batch_date', batch_date)
                    item_DishonestyBlacklist.add_value('cust_name', cust)
                    item_DishonestyBlacklist.add_value('data_source', result['数据来源'])
                    item_DishonestyBlacklist.add_value('case_no', result['案号'])
                    item_DishonestyBlacklist.add_value('dishonesty_cust_name', result['失信被执行人名称'])
                    item_DishonestyBlacklist.add_value('legal_person', result['企业法人姓名'])
                    item_DishonestyBlacklist.add_value('exec_court', result['执行法院'])
                    item_DishonestyBlacklist.add_value('area_name', result['地域名称'])
                    item_DishonestyBlacklist.add_value('exec_gist_no', result['执行依据文号'])
                    item_DishonestyBlacklist.add_value('exec_gist_org', result['作出执行依据单位'])
                    item_DishonestyBlacklist.add_value('writ_content', result['法律生效文书确定的义务'])
                    item_DishonestyBlacklist.add_value('performance_status', result['被执行人的履行情况'])
                    item_DishonestyBlacklist.add_value('dishonesty_cust_specific_status', result['失信被执行人具体情形'])
                    item_DishonestyBlacklist.add_value('issue_date', result['发布时间'])
                    item_DishonestyBlacklist.add_value('register_date', result['立案时间'])
                    item_DishonestyBlacklist.add_value('performanced_part', result['已履行部分'])
                    item_DishonestyBlacklist.add_value('unperformanced_part', result['未履行部分'])
                    item_DishonestyBlacklist.add_value('data_update_date', result['最新更新日期'])
                    item_DishonestyBlacklist.add_value('table_name', 'dishonesty_blacklist')
                    yield item_DishonestyBlacklist.load_item()
                else:
                    item_DishonestyBlacklist = CreditchinaLoaderItem(item=DishonestyBlacklistItem(), response=response)
                    item_DishonestyBlacklist.add_value('batch_date', batch_date)
                    item_DishonestyBlacklist.add_value('cust_name', cust)
                    item_DishonestyBlacklist.add_value('data_source', '')
                    item_DishonestyBlacklist.add_value('case_no', '')
                    item_DishonestyBlacklist.add_value('dishonesty_cust_name', '')
                    item_DishonestyBlacklist.add_value('legal_person', '')
                    item_DishonestyBlacklist.add_value('exec_court', '')
                    item_DishonestyBlacklist.add_value('area_name', '')
                    item_DishonestyBlacklist.add_value('exec_gist_no', '')
                    item_DishonestyBlacklist.add_value('exec_gist_org', '')
                    item_DishonestyBlacklist.add_value('writ_content', '')
                    item_DishonestyBlacklist.add_value('performance_status', '')
                    item_DishonestyBlacklist.add_value('dishonesty_cust_specific_status', '')
                    item_DishonestyBlacklist.add_value('issue_date', '')
                    item_DishonestyBlacklist.add_value('register_date', '')
                    item_DishonestyBlacklist.add_value('performanced_part', '')
                    item_DishonestyBlacklist.add_value('unperformanced_part', '')
                    item_DishonestyBlacklist.add_value('data_update_date', '')
                    item_DishonestyBlacklist.add_value('table_name', 'dishonesty_blacklist')
                    yield item_DishonestyBlacklist.load_item()
                if result['数据类别'] == '重大税收违法案件当事人名单':
                    item_SeriousRevenueLawlessCustList = CreditchinaLoaderItem(item=SeriousRevenueLawlessCustListItem(),response=response)
                    item_SeriousRevenueLawlessCustList.add_value('batch_date', batch_date)
                    item_SeriousRevenueLawlessCustList.add_value('cust_name', cust)
                    item_SeriousRevenueLawlessCustList.add_value('data_source', result['数据来源'])
                    item_SeriousRevenueLawlessCustList.add_value('taxer_name', result['纳税人名称'])
                    item_SeriousRevenueLawlessCustList.add_value('taxer_id', result['纳税人识别码'])
                    item_SeriousRevenueLawlessCustList.add_value('org_code', result['组织机构代码'])
                    item_SeriousRevenueLawlessCustList.add_value('register_addr', result['注册地址'])
                    item_SeriousRevenueLawlessCustList.add_value('legal_person_name', result['法定代表人或者负责人姓名'])
                    item_SeriousRevenueLawlessCustList.add_value('financing_person_name', result['负有直接责任的财务负责人姓名'])
                    item_SeriousRevenueLawlessCustList.add_value('intermediary_info', result['负有直接责任的中介机构信息及其从业人员信息'])
                    item_SeriousRevenueLawlessCustList.add_value('case_nature', result['案件性质'])
                    item_SeriousRevenueLawlessCustList.add_value('lawless_fact', result['主要违法事实'])
                    item_SeriousRevenueLawlessCustList.add_value('punish_status', result['相关法律依据及税务处理处罚情况'])
                    item_SeriousRevenueLawlessCustList.add_value('case_report_date', result['案件上报期'])
                    item_SeriousRevenueLawlessCustList.add_value('data_update_date', result['最新更新日期'])
                    item_SeriousRevenueLawlessCustList.add_value('table_name', 'serious_revenue_lawless_cust_list')
                    yield item_SeriousRevenueLawlessCustList.load_item()
                else:
                    item_SeriousRevenueLawlessCustList = CreditchinaLoaderItem(item=SeriousRevenueLawlessCustListItem(),response=response)
                    item_SeriousRevenueLawlessCustList.add_value('batch_date', batch_date)
                    item_SeriousRevenueLawlessCustList.add_value('cust_name', cust)
                    item_SeriousRevenueLawlessCustList.add_value('data_source', '')
                    item_SeriousRevenueLawlessCustList.add_value('taxer_name', '')
                    item_SeriousRevenueLawlessCustList.add_value('taxer_id', '')
                    item_SeriousRevenueLawlessCustList.add_value('org_code', '')
                    item_SeriousRevenueLawlessCustList.add_value('register_addr', '')
                    item_SeriousRevenueLawlessCustList.add_value('legal_person_name', '')
                    item_SeriousRevenueLawlessCustList.add_value('financing_person_name', '')
                    item_SeriousRevenueLawlessCustList.add_value('intermediary_info', '')
                    item_SeriousRevenueLawlessCustList.add_value('case_nature', '')
                    item_SeriousRevenueLawlessCustList.add_value('lawless_fact', '')
                    item_SeriousRevenueLawlessCustList.add_value('punish_status', '')
                    item_SeriousRevenueLawlessCustList.add_value('case_report_date', '')
                    item_SeriousRevenueLawlessCustList.add_value('data_update_date', '')
                    item_SeriousRevenueLawlessCustList.add_value('table_name', 'serious_revenue_lawless_cust_list')
                    yield item_SeriousRevenueLawlessCustList.load_item()
                if result['数据类别'] == '财政部采购不良记录数据':
                    item_PurchasingBadnessRecord = CreditchinaLoaderItem(item=PurchasingBadnessRecordItem(),response=response)
                    item_PurchasingBadnessRecord.add_value('batch_date', batch_date)
                    item_PurchasingBadnessRecord.add_value('cust_name', cust)
                    item_PurchasingBadnessRecord.add_value('data_source', result['数据来源'])
                    item_PurchasingBadnessRecord.add_value('supplier_name', result['供应商或代理机构名称'])
                    item_PurchasingBadnessRecord.add_value('supplier_addr', result['地址'])
                    item_PurchasingBadnessRecord.add_value('lawless_status', result['不良行为的具体情形'])
                    item_PurchasingBadnessRecord.add_value('punish_result', result['处罚结果'])
                    item_PurchasingBadnessRecord.add_value('punish_gist', result['处罚依据'])
                    item_PurchasingBadnessRecord.add_value('punish_date', result['处罚（记录）日期'])
                    item_PurchasingBadnessRecord.add_value('exec_org', result['执法（记录）单位'])
                    item_PurchasingBadnessRecord.add_value('punish_end_date', result['处罚结束时间'])
                    item_PurchasingBadnessRecord.add_value('data_update_date', result['最新更新日期'])
                    item_PurchasingBadnessRecord.add_value('table_name', 'purchasing_badness_record')
                    yield item_PurchasingBadnessRecord.load_item()
                else:
                    item_PurchasingBadnessRecord = CreditchinaLoaderItem(item=PurchasingBadnessRecordItem(),response=response)
                    item_PurchasingBadnessRecord.add_value('batch_date', batch_date)
                    item_PurchasingBadnessRecord.add_value('cust_name', cust)
                    item_PurchasingBadnessRecord.add_value('data_source', '')
                    item_PurchasingBadnessRecord.add_value('supplier_name', '')
                    item_PurchasingBadnessRecord.add_value('supplier_addr', '')
                    item_PurchasingBadnessRecord.add_value('lawless_status', '')
                    item_PurchasingBadnessRecord.add_value('punish_result', '')
                    item_PurchasingBadnessRecord.add_value('punish_gist', '')
                    item_PurchasingBadnessRecord.add_value('punish_date', '')
                    item_PurchasingBadnessRecord.add_value('exec_org', '')
                    item_PurchasingBadnessRecord.add_value('punish_end_date', '')
                    item_PurchasingBadnessRecord.add_value('data_update_date', '')
                    item_PurchasingBadnessRecord.add_value('table_name', 'purchasing_badness_record')
                    yield item_PurchasingBadnessRecord.load_item()
                if result['数据类别'] != '财政部采购不良记录数据' and result['数据类别'] != '重大税收违法案件当事人名单' and result['数据类别'] != '失信黑名单-法人':
                    self.logger.warning('parse_record_param_url_append_8 has a new type: %s', result['数据类别'])
        else:
            item_DishonestyBlacklist = CreditchinaLoaderItem(item=DishonestyBlacklistItem(), response=response)
            item_DishonestyBlacklist.add_value('batch_date', batch_date)
            item_DishonestyBlacklist.add_value('cust_name', cust)
            item_DishonestyBlacklist.add_value('data_source', '')
            item_DishonestyBlacklist.add_value('case_no', '')
            item_DishonestyBlacklist.add_value('dishonesty_cust_name', '')
            item_DishonestyBlacklist.add_value('legal_person', '')
            item_DishonestyBlacklist.add_value('exec_court', '')
            item_DishonestyBlacklist.add_value('area_name', '')
            item_DishonestyBlacklist.add_value('exec_gist_no', '')
            item_DishonestyBlacklist.add_value('exec_gist_org', '')
            item_DishonestyBlacklist.add_value('writ_content', '')
            item_DishonestyBlacklist.add_value('performance_status', '')
            item_DishonestyBlacklist.add_value('dishonesty_cust_specific_status', '')
            item_DishonestyBlacklist.add_value('issue_date', '')
            item_DishonestyBlacklist.add_value('register_date', '')
            item_DishonestyBlacklist.add_value('performanced_part', '')
            item_DishonestyBlacklist.add_value('unperformanced_part', '')
            item_DishonestyBlacklist.add_value('data_update_date', '')
            item_DishonestyBlacklist.add_value('table_name', 'dishonesty_blacklist')
            yield item_DishonestyBlacklist.load_item()

            item_SeriousRevenueLawlessCustList = CreditchinaLoaderItem(item=SeriousRevenueLawlessCustListItem(),response=response)
            item_SeriousRevenueLawlessCustList.add_value('batch_date', batch_date)
            item_SeriousRevenueLawlessCustList.add_value('cust_name', cust)
            item_SeriousRevenueLawlessCustList.add_value('data_source', '')
            item_SeriousRevenueLawlessCustList.add_value('taxer_name', '')
            item_SeriousRevenueLawlessCustList.add_value('taxer_id', '')
            item_SeriousRevenueLawlessCustList.add_value('org_code', '')
            item_SeriousRevenueLawlessCustList.add_value('register_addr', '')
            item_SeriousRevenueLawlessCustList.add_value('legal_person_name', '')
            item_SeriousRevenueLawlessCustList.add_value('financing_person_name', '')
            item_SeriousRevenueLawlessCustList.add_value('intermediary_info', '')
            item_SeriousRevenueLawlessCustList.add_value('case_nature', '')
            item_SeriousRevenueLawlessCustList.add_value('lawless_fact', '')
            item_SeriousRevenueLawlessCustList.add_value('punish_status', '')
            item_SeriousRevenueLawlessCustList.add_value('case_report_date', '')
            item_SeriousRevenueLawlessCustList.add_value('data_update_date', '')
            item_SeriousRevenueLawlessCustList.add_value('table_name', 'serious_revenue_lawless_cust_list')
            yield item_SeriousRevenueLawlessCustList.load_item()

            item_PurchasingBadnessRecord = CreditchinaLoaderItem(item=PurchasingBadnessRecordItem(), response=response)
            item_PurchasingBadnessRecord.add_value('batch_date', batch_date)
            item_PurchasingBadnessRecord.add_value('cust_name', cust)
            item_PurchasingBadnessRecord.add_value('data_source', '')
            item_PurchasingBadnessRecord.add_value('supplier_name', '')
            item_PurchasingBadnessRecord.add_value('supplier_addr', '')
            item_PurchasingBadnessRecord.add_value('lawless_status', '')
            item_PurchasingBadnessRecord.add_value('punish_result', '')
            item_PurchasingBadnessRecord.add_value('punish_gist', '')
            item_PurchasingBadnessRecord.add_value('punish_date', '')
            item_PurchasingBadnessRecord.add_value('exec_org', '')
            item_PurchasingBadnessRecord.add_value('punish_end_date', '')
            item_PurchasingBadnessRecord.add_value('data_update_date', '')
            item_PurchasingBadnessRecord.add_value('table_name', 'purchasing_badness_record')
            yield item_PurchasingBadnessRecord.load_item()
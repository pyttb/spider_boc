# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import urllib

import scrapy

from creditchina_project.wdzj_items import WdzjLoaderItem,WdzjResultItem

reload(sys)
sys.setdefaultencoding('utf-8')
class Wdzj(scrapy.Spider):
    name = "wdzj"
    custom_settings = {
        'ITEM_PIPELINES': {
            'creditchina_project.pipelines.CreditchinaProjectDB2Pipeline': 100,
        }
    }
    batch_date = datetime.datetime.now().date()
    allowed_domains = ['www.wdzj.com']

    def start_requests(self):
        default_data = {
        }
        default_headers = {
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
            'Cookie': 'gr_user_id=dc16a530-c757-444a-b072-1150e3c34a69; __jsluid=b87efca3caa2675cfa46396b9a4010f7; pc_login=1; route=a57086c2d51d5c9496accda7a8d9ea91; pass_refer=https%3A%2F%2Fshuju.wdzj.com%2Fproblem-1.html; gr_session_id_1931ea22324b4036a653ff1d3a0b4693=181ff69c-d535-41da-8099-27b004aaf909; gr_cs1_181ff69c-d535-41da-8099-27b004aaf909=user_id%3A1468416; UM_distinctid=16203dbb3d2199-0b2c27c02bcb97-3f3c5906-144000-16203dbb3d34e1; _ga=GA1.2.1897436897.1520483153; _gid=GA1.2.1178677747.1520483153; _gat=1; _pk_ref.1.b30f=%5B%22%22%2C%22%22%2C1520483153%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.1.b30f=48874f764c7f544e.1520471469.2.1520483153.1520483153.; _pk_ses.1.b30f=*; Hm_lvt_9e837711961994d9830dcd3f4b45f0b3=1520471469; Hm_lpvt_9e837711961994d9830dcd3f4b45f0b3=1520483153; WDZJptlbs=1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Host': 'passport.wdzj.com'
        }
        yield scrapy.Request(url='https://passport.wdzj.com/userInterface/login?t=1520478724292&callback=jQuery1102021446813330409986_1520478553360&username=18201828126&password=wdzj154553&auto_login=1&_=1520478553364', headers=default_headers,
                             body=urllib.urlencode(default_data), callback=self.start_login, dont_filter=True)

    def start_login(self, response):
        yield scrapy.Request(url='https://shuju.wdzj.com/problem-list-all.html?year=', headers={},
                             body=urllib.urlencode({}), callback=self.parse_basic_info, dont_filter=True)

    def parse_basic_info(self, response):
        basic_info = response.text
        problemList=eval(basic_info.replace('null', 'None').replace('false', 'None').replace('true', 'None'))['problemList']
        for problem in problemList:
            item = WdzjResultItem(item=WdzjResultItem(), response=response)
            item.add_value('batch_date', self.batch_date)
            item.add_value('platName', problem['platName'])
            item.add_value('problemTime', problem['problemTime'])
            item.add_value('onlineTime', problem['onlineTime'])
            item.add_value('regCapital', problem['regCapital'])
            item.add_value('area', problem['area'])
            item.add_value('type', problem['type'])
            item.add_value('table_name', 'creditchina.wdzj_result')
            yield item.load_item()

    def closed(self, reason):
        '''
        爬虫结束时退出登录状态
        :param reason:
        :return:
        '''
        if 'finished' == reason:
            logging.warning('%s', '爬虫程序执行结束，即将关闭')
        elif 'shutdown' == reason:
            logging.warning('%s', '爬虫进程被强制中断，即将关闭')
        elif 'cancelled' == reason:
            logging.warning('%s', '爬虫被引擎中断，即将关闭')
        else:
            logging.warning('%s', '爬虫被未知原因打断，即将关闭')
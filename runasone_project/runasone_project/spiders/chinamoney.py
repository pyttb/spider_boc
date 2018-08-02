# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import urlparse
import urllib
import time
import datetime
from runasone_project.chinamoney_items import ChinaMoneyLoaderItem,CM_MarketTradeItem,CM_TY_TERM_TRADEITEM,CM_HG_TERM_TRADEITEM

class ChinamoneySpider(scrapy.Spider):
    name = 'chinamoney'
    allowed_domains = ['http://www.chinamoney.com.cn/fe/Channel/19152']
    # start_urls = ['http://www.chinamoney.com.cn/fe/Channel/19152/']
    base_url="http://www.chinamoney.com.cn/fe/Channel/19152/"
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
        'Proxy-Connection': 'keep-alive',
        'RA-Sid': 's_858_r2x9ak474125_270',
        'RA-Ver': '3.3.0',
        'Cookie': 'JSESSIONID=PnHqcObwGEptN4Hk76NlxWovxsQejjqZV2GbhHq0GTndARC89SJk!-1269514697; _ulta_id.CM-Prod.e9dc=c2d0914c7eb31844; _ulta_ses.CM-Prod.e9dc=f27d6c24b1d75709; ADMINCONSOLESESSION=ZJjrgEw51OpU-d_zaAiWSDWi10gx5Yy2YYd_G7RZPdX4_pugzUIj!1426237228; ZP_CAL=%27fdow%27%3Anull%2C%27history%27%3A%222018/07/11/22/20%22%2C%27sortOrder%27%3A%22asc%22%2C%27hsize%27%3A9',
        'Host': 'www.chinamoney.com.cn',
        'Cache-Control':'max-age=0',
        'Content-Type':'application/x-www-form-urlencoded',
        'Origin': 'http://www.chinamoney.com.cn',
        'Referer': 'http://www.chinamoney.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36HH=20Runtime=kecekldmfbcpjfmnnijdjhcggpcnkpbhALICDN/ DOL/HELLO_GWF_s_858_r2x9ak474125_270',
        'X-Requested-With': 'XMLHttpRequest',
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'runasone_project.pipelines.RunasoneDB2Pipeline': 100,  # 保存到数据库
        }
    }
    default_data=''

    def start_requests(self):

        #日期循环爬取,开始结束日期
        begin = datetime.date(2018, 1, 1)
        end = datetime.date(2018, 8, 2)
        # begin = datetime.date(2018, 3, 15)
        # end = datetime.date(2018, 3, 15)
        for i in range((end - begin).days + 1):
            searchday = begin + datetime.timedelta(days=i)
            self.default_data = {'searchDate': str(searchday)}
            default_data = urllib.urlencode(self.default_data)

            # 同业拆借日报     API
            CreditLendDailySearch_URL = urlparse.urljoin(self.base_url, '/fe-c/CreditLendDailySearchAction.do')
            yield scrapy.Request(
                url=CreditLendDailySearch_URL,
                meta={'searchDate': str(searchday),'query_block':'同业拆借日报'},
                body=default_data,
                headers=self.default_headers,
                method="POST",
                callback=self.get_MoneyReportDaily_details)

            #质押式回购日报    API
            PledgeRepoDailySearch_URL=urlparse.urljoin(self.base_url, '/fe-c/PledgeRepoDailySearchAction.do')
            yield scrapy.Request(
                url=PledgeRepoDailySearch_URL,
                meta={'searchDate': str(searchday),'query_block':'质押式回购日报'},
                body=default_data,
                headers=self.default_headers,
                method="POST",
                callback=self.get_MoneyReportDaily_details)

    def get_MoneyReportDaily_details(self, response):

        fo = open("test.html", "w")
        fo.write(response.text)

        #使用BeautifulSoup解析获取两张表格信息
        #市场成交情况
        soup = BeautifulSoup(response.text, 'lxml')
        #查询日期
        c0 = response.meta['searchDate']
        c1 = response.meta['query_block']

        #抽取：第一张表的第二行
        if c1=='同业拆借日报':
            t0 = soup.find_all(class_=" market-new-text")[0]  #同业
        elif c1=='质押式回购日报':
            t0 = soup.find_all(class_=" market-new-text")[1]  #回购

        if t0 and len(t0.find_all('tr')) > 1:
            tr1 = t0.find_all('tr')[1]  #同业/回购 一样
            if tr1:
                c2 = '市场成交情况'
                marketTradeItem = ChinaMoneyLoaderItem(item=CM_MarketTradeItem(), response=response)
                marketTradeItem.add_value('c0', c0);
                marketTradeItem.add_value('c1', c1);
                marketTradeItem.add_value('c2', c2);
                marketTradeItem.add_value('c3', tr1.find_all('td')[0].text); 
                marketTradeItem.add_value('c4', tr1.find_all('td')[1].text)
                marketTradeItem.add_value('c5', tr1.find_all('td')[2].text)
                marketTradeItem.add_value('c6', tr1.find_all('td')[3].text)
                marketTradeItem.add_value('c7', tr1.find_all('td')[4].text)
                marketTradeItem.add_value('c8', tr1.find_all('td')[5].text)
                marketTradeItem.add_value('c9', tr1.find_all('td')[6].text)
                marketTradeItem.add_value('c10', self.get_current_timestamp());
                marketTradeItem.add_value('table_name', 'SPIDER.CM_MARKETTRADEITEM')
                yield marketTradeItem.load_item()

        # 各期限品种成交情况
        c2 = '各期限品种成交情况'
        if c1=='同业拆借日报':
            t1 = soup.find_all(class_=" market-new-text")[1]  # 同业
            if t1 and t1.find_all('tr'):
                for tr in t1.find_all('tr'):
                    # 判断是否产品码开头
                    if tr.find('td') and tr.find_all('td')[0].text.encode("utf-8").isalnum():
                        termTradeTradeItem = ChinaMoneyLoaderItem(item=CM_TY_TERM_TRADEITEM(), response=response)
                        termTradeTradeItem.add_value('c0', c0);
                        termTradeTradeItem.add_value('c1', c1);
                        termTradeTradeItem.add_value('c2', c2);
                        termTradeTradeItem.add_value('c3', tr.find_all('td')[0].text);
                        termTradeTradeItem.add_value('c4', tr.find_all('td')[1].text);
                        termTradeTradeItem.add_value('c5', tr.find_all('td')[2].text);
                        termTradeTradeItem.add_value('c6', tr.find_all('td')[3].text);
                        termTradeTradeItem.add_value('c7', tr.find_all('td')[4].text);
                        termTradeTradeItem.add_value('c8', tr.find_all('td')[5].text);
                        termTradeTradeItem.add_value('c9', tr.find_all('td')[6].text);
                        termTradeTradeItem.add_value('c10', tr.find_all('td')[7].text);
                        termTradeTradeItem.add_value('c11', tr.find_all('td')[8].text);
                        termTradeTradeItem.add_value('c12', self.get_current_timestamp());
                        termTradeTradeItem.add_value('table_name', 'SPIDER.CM_TY_TERM_TRADEITEM')
                        yield termTradeTradeItem.load_item()

        elif c1=='质押式回购日报':
            t1 = soup.find_all(class_=" market-new-text")[2]  #回购
            if t1 and t1.find_all('tr'):
                for tr in t1.find_all('tr'):
                    # 判断是否产品码开头
                    if tr.find('td') and tr.find_all('td')[0].text.encode("utf-8").isalnum():
                        termTradeTradeItem = ChinaMoneyLoaderItem(item=CM_HG_TERM_TRADEITEM(), response=response)
                        termTradeTradeItem.add_value('c0', c0);
                        termTradeTradeItem.add_value('c1', c1);
                        termTradeTradeItem.add_value('c2', c2);
                        termTradeTradeItem.add_value('c3', tr.find_all('td')[0].text);
                        termTradeTradeItem.add_value('c4', tr.find_all('td')[1].text);
                        termTradeTradeItem.add_value('c5', tr.find_all('td')[2].text);
                        termTradeTradeItem.add_value('c6', tr.find_all('td')[3].text);
                        termTradeTradeItem.add_value('c7', tr.find_all('td')[4].text);
                        termTradeTradeItem.add_value('c8', tr.find_all('td')[5].text);
                        termTradeTradeItem.add_value('c9', tr.find_all('td')[6].text);
                        termTradeTradeItem.add_value('c10', tr.find_all('td')[7].text);
                        termTradeTradeItem.add_value('c11', tr.find_all('td')[8].text);
                        termTradeTradeItem.add_value('c12', tr.find_all('td')[9].text);
                        termTradeTradeItem.add_value('c13', self.get_current_timestamp());
                        termTradeTradeItem.add_value('table_name', 'SPIDER.CM_HG_TERM_TRADEITEM')
                        yield termTradeTradeItem.load_item()




    def get_current_timestamp(self):
        timestamp = time.time()
        timestruct = time.localtime(timestamp)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
        return timestamp
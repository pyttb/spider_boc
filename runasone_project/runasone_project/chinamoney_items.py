# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join




class ChinaMoneyLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()



#市场成交情况
class CM_MarketTradeItem(scrapy.Item):
    c0 = scrapy.Field()
    c1 = scrapy.Field()
    c2 = scrapy.Field()
    c3 = scrapy.Field()
    c4 = scrapy.Field()
    c5 = scrapy.Field()
    c6 = scrapy.Field()
    c7 = scrapy.Field()
    c8 = scrapy.Field()
    c9 = scrapy.Field()
    c10 = scrapy.Field()
    table_name = scrapy.Field()

#同业拆借-各期限品种成交情况
class CM_TY_TERM_TRADEITEM(scrapy.Item):
    c0 = scrapy.Field()
    c1 = scrapy.Field()
    c2 = scrapy.Field()
    c3 = scrapy.Field()
    c4 = scrapy.Field()
    c5 = scrapy.Field()
    c6 = scrapy.Field()
    c7 = scrapy.Field()
    c8 = scrapy.Field()
    c9 = scrapy.Field()
    c10 = scrapy.Field()
    c11 = scrapy.Field()
    c12 = scrapy.Field()
    table_name = scrapy.Field()

#质押式回购-各期限品种成交情况
class CM_HG_TERM_TRADEITEM(scrapy.Item):
    c0 = scrapy.Field()
    c1 = scrapy.Field()
    c2 = scrapy.Field()
    c3 = scrapy.Field()
    c4 = scrapy.Field()
    c5 = scrapy.Field()
    c6 = scrapy.Field()
    c7 = scrapy.Field()
    c8 = scrapy.Field()
    c9 = scrapy.Field()
    c10 = scrapy.Field()
    c11 = scrapy.Field()
    c12 = scrapy.Field()
    c13 = scrapy.Field()
    table_name = scrapy.Field()
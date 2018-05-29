# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def delete_space(value):
    '''
    删除字符串中的所有空格
    :param value:
    :return:
    '''
    return str(value).replace(' ', '').strip()


def delete_plus(value):
    '''
    删除字符串中的"+"
    :param value:
    :return:
    '''
    return str(value).replace('+', '').strip()


def date_parse(value):
    '''
    转换为日期类型
    :param value:
    :return:
    '''
    try:
        value = value.replace('·', '').replace('/', '').strip()
        value = datetime.datetime.strptime(value, '%Y%m%d').date()
    except Exception as e:
        value = datetime.datetime.now().date()
    return str(value)


def return_value(value):
    '''
    保持原来的数值不变
    :param value:
    :return:
    '''
    return str(value).strip()


def get_value(value):
    '''
    通过正则表达式获取特定值
    :param value:
    :return:
    '''
    value = str(value).strip()
    obj = re.match('.*\[(.*?)\].*', value)
    if obj:
        return obj.group(1)
    else:
        return value
class StatsLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()

class StatsResultItem(scrapy.Item):
    batch_date = scrapy.Field()
    pub_writ_no = scrapy.Field()
    pub_name = scrapy.Field()
    pub_type_1 = scrapy.Field()
    pub_type_2 = scrapy.Field()
    pub_reason = scrapy.Field()
    pub_gist = scrapy.Field()
    admin_counterpart_name = scrapy.Field()
    admin_counterpart_code_1 = scrapy.Field()
    admin_counterpart_code_2 = scrapy.Field()
    admin_counterpart_code_3 = scrapy.Field()
    admin_counterpart_code_4 = scrapy.Field()
    admin_counterpart_code_5 = scrapy.Field()
    publicity_term = scrapy.Field()
    table_name = scrapy.Field()
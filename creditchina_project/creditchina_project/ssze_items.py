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
class SszeLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()

class SszeZqxxJlcfResultItem(scrapy.Item):
    batch_date = scrapy.Field()
    company_name = scrapy.Field()
    writ_no = scrapy.Field()
    pub_type = scrapy.Field()
    writ_date = scrapy.Field()
    rel_bond = scrapy.Field()
    table_name = scrapy.Field()

class SzseCxdaCfcfjlResultItem(scrapy.Item):
    batch_date = scrapy.Field()
    company_code = scrapy.Field()
    company_nick = scrapy.Field()
    pub_date = scrapy.Field()
    pub_type = scrapy.Field()
    counterpart_name = scrapy.Field()
    title = scrapy.Field()
    table_name = scrapy.Field()

class SszeZqxxJlcfDetailResultItem(scrapy.Item):
    batch_date = scrapy.Field()
    inter_name = scrapy.Field()
    inter_type = scrapy.Field()
    pub_date = scrapy.Field()
    pub_type = scrapy.Field()
    ref_company_code = scrapy.Field()
    ref_company_nick = scrapy.Field()
    counterpart_name = scrapy.Field()
    title = scrapy.Field()
    table_name = scrapy.Field()
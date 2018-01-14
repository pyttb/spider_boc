# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
import datetime
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import time

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


def date_parse_from_digital(value):
    '''
    转换为日期类型
    :param value:
    :return:
    '''
    try:
        value = time.strftime("%Y-%m-%d", time.localtime(float(value)/1000))
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


class AmacInfoLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()


class ManagerListInfoItem(scrapy.Item):
    '''
    保存ManagerListInfo信息
    '''
    qry_date = scrapy.Field(input_processor=MapCompose(date_parse))
    id=scrapy.Field()
    managerName=scrapy.Field()
    artificialPersonName=scrapy.Field()
    registerNo=scrapy.Field()
    establishDate=scrapy.Field(input_processor=MapCompose(date_parse_from_digital))
    managerHasProduct=scrapy.Field()
    url=scrapy.Field()
    registerDate=scrapy.Field(input_processor=MapCompose(date_parse_from_digital))
    registerAddress=scrapy.Field()
    registerProvince=scrapy.Field()
    registerCity=scrapy.Field()
    regAdrAgg=scrapy.Field()
    primaryInvestType=scrapy.Field()



class AmacinfodiskProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

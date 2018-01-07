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


class BankLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()


class BankSsiItem(scrapy.Item):
    '''
    保存SSI信息
    '''
    qry_date = scrapy.Field(
        input_processor=MapCompose(date_parse)
    )
    bank_swift = scrapy.Field(
        input_processor=MapCompose(delete_plus)
    )
    currency = scrapy.Field()
    bank = scrapy.Field()
    swift_bic = scrapy.Field()
    account_no = scrapy.Field()
    ssikeycolumn_cp = scrapy.Field()
    ssikeycolumn_fx = scrapy.Field()
    ssikeycolumn_mm = scrapy.Field()
    other = scrapy.Field()


class BankCreditInfoItem(scrapy.Item):
    '''
    保存征信评级信息
    '''
    qry_date = scrapy.Field(
        input_processor=MapCompose(date_parse)
    )
    bank_swift = scrapy.Field(
        input_processor=MapCompose(delete_plus)
    )
    credit_name = scrapy.Field()
    long_term = scrapy.Field()
    short_term = scrapy.Field()


class BankerListInfoItem(scrapy.Item):
    '''
    保存查询列表中的信息
    '''
    qry_date = scrapy.Field(
        input_processor=MapCompose(date_parse)
    )
    swift = scrapy.Field()
    bank_name = scrapy.Field()
    bank_type = scrapy.Field()
    bank_location = scrapy.Field()
    bank_country = scrapy.Field()
    bank_swift = scrapy.Field(
        input_processor=MapCompose(delete_space)
    )


class BankDetailsInfoItem(scrapy.Item):
    '''
    保存机构的详细信息
    '''
    qry_date = scrapy.Field(
        input_processor=MapCompose(date_parse)
    )
    bank_swift = scrapy.Field(
        input_processor=MapCompose(delete_plus)
    )
    bank_website = scrapy.Field()
    postal_address = scrapy.Field(
        # output_processor=MapCompose(return_value)
        output_processor=Join('')
    )
    world_rank = scrapy.Field(
        input_processor=MapCompose(get_value)
    )
    country_rank = scrapy.Field(
        input_processor=MapCompose(get_value)
    )
    owner_ship = scrapy.Field()
    history = scrapy.Field()


class SpiderBankerItem(scrapy.Item):
    pass
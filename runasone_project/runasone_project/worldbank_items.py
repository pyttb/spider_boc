# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class WorldbankLoaderItem(ItemLoader):
    '''
    自定义ITEM，取每个字段数组的第一个值
    '''
    default_output_processor = TakeFirst()

class SizeOfTheEconomyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    batch_date = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    population = scrapy.Field()
    surface_area = scrapy.Field()
    population_density = scrapy.Field()
    GNI_1 = scrapy.Field()
    GNI_2 = scrapy.Field()
    purchasing_1= scrapy.Field()
    purchasing_2= scrapy.Field()
    GDP_1 = scrapy.Field()
    GDP_2 = scrapy.Field()
    table_name = scrapy.Field()

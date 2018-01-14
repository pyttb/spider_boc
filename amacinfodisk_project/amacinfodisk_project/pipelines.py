# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import redis

class AmacinfodiskProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class AmacinfodiskTwistedPipeline(object):
    '''
        调用twisted，将信息异步入库，降低对爬虫爬取速度的影响
        '''

    def __init__(self, dbpool, conn):
        self.dbpool = dbpool
        self.conn = conn

    @classmethod
    def from_settings(cls, settings):
        '''
        读取配置文件中的数据库配置
        :param settings:
        :return:
        '''
        dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        conn = redis.StrictRedis(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            db=settings['REDIS_DB']
        )
        return cls(dbpool, conn)

    def process_item(self,item,spider):
        '''
        处理ITEM
        :param item:
        :param spider:
        :return:
        '''
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        '''
        添加error操作
        :param failure:
        :return:
        '''
        print(failure)

    def do_insert(self, cursor, item):
        '''
        添加详细信息
        :param cursor:
        :param item:
        :return:
        '''
        insert = 'insert into amac.manager_list_info('

        value = 'values('
        keys = item.keys()
        for i in xrange(0, len(keys)):
            if i == (len(keys) - 1):
                insert = insert + keys[i] + ')'
                value = value + '\"' + str(item[keys[i]]).replace("\"", "\'") + '\")'
            else:
                insert = insert + keys[i] + ','
                value = value + '\"' + str(item[keys[i]]).replace("\"", "\'") + '\",'
        sql = insert + value
        print(sql)
        cursor.execute(sql)

        # 添加机构代码到已爬清单中,应该要加上时间戳？
        self.conn.sadd('amac_query_record', item['id'])






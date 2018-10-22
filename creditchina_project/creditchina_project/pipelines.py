# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import sys

from twisted.enterprise import adbapi
import redis
import logging
import ibm_db_dbi
import ibm_db

reload(sys)
sys.setdefaultencoding('utf-8')
class CreditchinaProjectDB2Pipeline(object):
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
            'ibm_db_dbi',
            dsn='DATABASE='+settings['DB2_DBNAME']+';HOSTNAME='+settings['DB2_HOST']+';UID='+settings['DB2_USER']+';PWD='+settings['DB2_PASSWORD']+';PORT='+str(settings['DB2_PORT']),
            conn_options={'SQL_ATTR_AUTOCOMMIT':ibm_db_dbi.SQL_AUTOCOMMIT_ON}
        )
        conn = redis.StrictRedis(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            db=settings['REDIS_DB']
        )
        return cls(dbpool, conn)

    def process_item(self, item, spider):
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
        logging.info('%s', failure)

    def do_insert(self, cursor, item):
        '''
        添加详细信息
        :param cursor:
        :param item:
        :return:
        '''
        insert = 'insert into ' + item['table_name'] + ' ('
        values = 'values('
        keys = item.keys()
        params = []
        if 'table_name' in item:
            keys.remove('table_name')
        for i in xrange(0, len(keys)):
            if i == (len(keys) - 1):
                insert = insert + keys[i] + ')'
                # values = values + '\'' + str(item[keys[i]]).replace("\'", "\"") + '\')'
                values = values + '?)'
            else:
                insert = insert + keys[i] + ','
                # values = values + '\'' + str(item[keys[i]]).replace("\'", "\"") + '\','
                values = values + '?,'
            key = keys[i]
            value = item[keys[i]]
            # logging.info('value is %s, containsChinese is %s.', value, self.containsChinese(value))
            # logging.info('variable is %s, type is %s, length is %s.', value, type(value), sys.getsizeof(value))
            if self.containsChinese(value):
                params.append(str(value).replace("\'", "\"").decode('utf-8', "replace"))
            else:
                params.append(str(value).replace("\'", "\""))
        sql = insert + values
        logging.info('sql is %s, params is %s.', sql, params)
        cursor.execute(sql, params)

    def containsChinese(self, value):
        if isinstance(value, unicode):
            return len(re.findall(ur'[\u4e00-\u9fff]+', value)) > 0
        else:
            return len(re.findall(ur'[\u4e00-\u9fff]+', str(value).decode('utf8'))) > 0
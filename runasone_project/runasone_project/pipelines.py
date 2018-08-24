# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import redis
import logging
import ibm_db_dbi
import ibm_db
import xlwt

class RunasoneProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class RunasoneDB2Pipeline(object):
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
            conn_options={'SQL_ATTR_AUTOCOMMIT':ibm_db.SQL_AUTOCOMMIT_ON}
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
        value = 'values('
        keys = item.keys()
        if 'table_name' in item:
            keys.remove('table_name')
        for i in xrange(0, len(keys)):
            if i == (len(keys) - 1):
                insert = insert + keys[i] + ')'
                value = value + '\'' + str(item[keys[i]]).replace("\'", "\"") + '\')'
            else:
                insert = insert + keys[i] + ','
                value = value + '\'' + str(item[keys[i]]).replace("\'", "\"") + '\','
        sql = insert + value
        logging.info('%s', sql)
        try:
            cursor.execute(sql)
        except Exception,e:
            print e.message
            print "INSERT 执行异常："+sql


# 1. 创建pipeline类继承object
class ExcelPipeline(object):
    # 2 . 重写初始化函数, 做准备工作
    def __init__(self):
         self.workbook = xlwt.Workbook(encoding='utf-8')
         self.sheet = self.workbook.add_sheet('WV.1')
         self.sheet.write(0, 0, 'WV.1  World Development Indicators: Size of the economy ')
         self.count = 1
    # 3. 实现process_item函数, 做写入操作
    def process_item(self, item, spider):
        keys = item.keys()
        for key in keys:
            if key=='batch_date': columnTh=0;
            elif key=='year': columnTh=1;
            elif key=='country': columnTh=2;
            elif key=='population': columnTh=3;
            elif key=='surface_area': columnTh=4;
            elif key=='population_density': columnTh=5;
            elif key=='GNI_1': columnTh=6;
            elif key=='GNI_2': columnTh=7;
            elif key=='purchasing_1': columnTh=8;
            elif key=='purchasing_2': columnTh=9;
            elif key=='GDP_1': columnTh=10;
            elif key=='GDP_2': columnTh=11;
            self.sheet.write(self.count, columnTh, str(item[key]))
        self.count += 1

        # for i in xrange(0, len(keys)):
        #     self.sheet.write(self.count, i, str(item[keys[i]]))
        # self.count += 1

        # for i in range(len(item)):
        #     self.sheet.write(self.count, i, item)
        #     self.count += 1
        #     return item

        # for index in item:
        #     self.sheet.write(self.count, index, index)
        # self.sheet.write(self.count, 0, item['batch_date'])
        # self.sheet.write(self.count, 1, item['population'])
        # self.sheet.write(self.count, 2, item['surface_area'])
        # self.sheet.write(self.count, 3, item['population_density'])
        # self.sheet.write(self.count, 4, item['GNI_1'])
        # self.sheet.write(self.count, 5, item['GNI_2'])
        # self.sheet.write(self.count, 6, item['purchasing_1'])
        # self.sheet.write(self.count, 7, item['purchasing_2'])
        # self.sheet.write(self.count, 8, item['GDP_1'])
        # self.sheet.write(self.count, 9, item['GDP_2'])

    # 4. 实现close_spider, 做关闭操作
    def close_spider(self, spider):
          self.workbook.save('SizeOfTheEconomy.xls')
# -*- coding: utf-8 -*-
# import random
import time
from datetime import datetime,date,timedelta

import scrapy
from scrapy.http import Request
from scrapy import cmdline

import logging

from creditchina_project.utils.deleteDbutils import queryAll, execute
from cmd_exqute import exqute_cmd

import base64
# from ..settings import DAT_FILE_PATH,DATA_FILE_PATH,DAT_DATA

from creditchina_project.downloadpdf_items import DownLoadPdfLoaderItem,DownLoadPdfResultItem

import os
from statsmodels.genmod.tests.test_gee import pdf


# 获取当前日期
nowtime = [datetime.now().date().strftime('%Y%m%d')]
# currentTime = [datetime.now().date().strftime('%Y-%m-%d')]
# 
# nowtime = [(date.today() + timedelta(days = -1)).strftime("%Y%m%d")]
currentTime = [(date.today() + timedelta(days = -1)).strftime("%Y-%m-%d")]

# local
# DAT_FILE_PATH = '/home/pd/download/pdf.dat'
# DATA_FILE_PATH = '/home/pd/download/lobs'
# DAT_DATA = 'new.dat'

# prd
DAT_FILE_PATH = '/usr/share/download/pdf.dat'
DATA_FILE_PATH = '/usr/share/download/lobs'
DAT_DATA = 'new.dat'

# nowtime = ["20190212"]
# currentTime = ["2019-02-12"]

 
#存文件路径
filepath = DAT_FILE_PATH
datapath = DATA_FILE_PATH + "/" + DAT_DATA
file_dir = os.path.split(filepath)[0]

# 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
if not os.path.isdir(file_dir):
    print file_dir
    os.makedirs(file_dir)
if not os.path.isdir(DATA_FILE_PATH):
    print file_dir
    os.makedirs(DATA_FILE_PATH)
    
data_sum = [0]

all_length = [0]
    
class TudiEndSpider(scrapy.Spider):
    name = 'download_pdf'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
    }
    
   
    
    def start_requests(self):

        '''
           1.获取out表中的当天日期的数据，如果无数据，走2，如果有数据，走3
           2.获取in表中的数据，跑批，跑批成功，doc_id=''，file_name='名称+时间戳',跑批失败，doc_id='fail'，filename=''
           3.获取in表中跑批失败的数据，如果有数据，再次跑批，之后先delete,再insert数据，如果跑批失败，返回不管
        '''
        logging.info("now time:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
#         print("now time:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
        
        if os.path.exists(filepath):
            os.remove(filepath)
            
        if os.path.exists(datapath):
            os.remove(datapath)
            
        # 获取当前日期        
#         data_sum[0] = 0
    
#         print("yestoday:" + nowtime[0])
        # 1.获取out表数据
        get_out_sql = "select SOURCE_CODE,CODE,ID from spider.RH_GOVT_CONTRACT_OUT where BATCHDATE = '" + nowtime[0] + "'"
        out_list = queryAll(get_out_sql)
        
        query_sql = "select FILE_CONTENT,SOURCE_CODE,ANN_CODE_DIS,CODE,ID,BATCHDATE from spider.RH_GOVT_CONTRACT_IN where UPDATE_TIME = '" +  currentTime[0] + "'"
#         print "query_sql:" + query_sql
        logging.info("query_sql:" + query_sql)
#         print("query_sql:" + query_sql)
        cur_list = queryAll(query_sql)
        
#         print "get_out_sql:" + get_out_sql
        logging.info("get_out_sql:" + get_out_sql)
#         print(len(out_list))
        logging.info("out: " + str(len(out_list)))
#         print(len(cur_list))
        logging.info("in: " + str(len(cur_list)))
        
        
        if len(out_list) != 0 and len(out_list) != len(cur_list):
            delete_sql = "delete from spider.RH_GOVT_CONTRACT_OUT where BATCHDATE = '" + nowtime[0] + "'"
            logging.info(delete_sql)
            execute(delete_sql)
#             print(delete_sql)
            logging.info("all pao count(out) != count(in)")
            
            out_list = []
#             print(len(out_list))
            logging.info("out_list len:" + str(len(out_list)))
            
        #2.out表中无数据
        if out_list== None or len(out_list) == 0 :
            # self.insert_out_sql()
#             query_sql = "select FILE_CONTENT,SOURCE_CODE,ANN_CODE_DIS,CODE,ID,BATCHDATE from spider.RH_GOVT_CONTRACT_IN where UPDATE_TIME = '" +  currentTime[0] + "'"
#             print "query_sql:" + query_sql
#             cur_list = queryAll(query_sql)
#             print(cur_list)
            all_count = len(cur_list)
            if all_count == 0:
#                 print '无下放数据'
                logging.info('无下放数据')
            
            else:
                # 循环获取pdf文件
                for cu in list(cur_list):
                    # pdf文件所在url
#                     print(cu)
                    logging.info(cu)
                    file_content = cu[0]
                    if None == file_content:
                        file_content = "fail"
                    
                    source_code = cu[1]
                    ann_code_dis = cu[2]
                    code = cu[3]
                    id = cu[4]
                    batchdate = cu[5]
                    
                    if None == source_code:
                        source_code = "fail"
                    
                    if None == ann_code_dis:
                        ann_code_dis = "fail"
                        
                    if None == code:
                        code = "fail"
                        
                    if None == id:
                        id = "fail"
                    
                    item = DownLoadPdfLoaderItem(item=DownLoadPdfResultItem())
                    item.add_value('file_content', file_content)
                    item.add_value('source_code', source_code)
                    item.add_value('ann_code_dis', ann_code_dis)
                    item.add_value('code', code)
                    item.add_value('id', id)
                    item.add_value('batchdate',nowtime[0])
                    item.add_value('all_count',all_count)
                    
                    try:
                        pdf_content = yield Request(file_content, meta={'item': item},callback=self.parse_pdf, errback=self.error_back,
                                                    dont_filter=True)
                    except Exception as e:
#                         print("url is error")
                        logging.info("insert url is error")
#                         print(e)
                        logging.info(e)
                        item.add_value('filedate','fail')
                        item.add_value('doc_id','fail')
                        item.add_value('file_name','fail')
                        
                        self.write_dat(item.load_item())
        
                        summ = data_sum[0]
                        summ = summ + 1
                        data_sum[0] = summ
                        if all_count == summ and summ != 0:
                            exqute_cmd()
                            data_sum[0] = 0
#                         elif summ % 5 == 0 and summ != 0:
#                             print("sum % 5 == 0")
#                             exqute_cmd()
                        
                    
        # 3.out表中有数据
        else:
            fail_sql = "select FILE_CONTENT,SOURCE_CODE,ANN_CODE_DIS,CODE,ID,BATCHDATE from spider.RH_GOVT_CONTRACT_OUT where BATCHDATE =  '" + nowtime[0] + "'and DOC_ID = 'fail'"
            cur_list = queryAll(fail_sql)
            
            all_count = len(cur_list)
            if all_count == 0:
                print '数据已跑完'

            else:
                for cu in list(cur_list):
                    file_content = cu[0]
                    if None == file_content:
                        file_content = "fail"
                    logging.info(file_content)
#                     print(file_content)
                        
                    source_code = cu[1]
                    ann_code_dis = cu[2]
                    code = cu[3]
                    id = cu[4]
                    batchdate = cu[5]
                    
                    if None == source_code:
                        source_code = "fail"
                    
                    if None == ann_code_dis:
                        ann_code_dis = "fail"
                        
                    if None == code:
                        code = "fail"
                        
                    if None == id:
                        id = "fail"
                
                    item = DownLoadPdfLoaderItem(item=DownLoadPdfResultItem())
                    item.add_value('file_content', file_content)
                    item.add_value('source_code', source_code)
                    item.add_value('ann_code_dis', ann_code_dis)
                    item.add_value('code', code)
                    item.add_value('id', id)
                    item.add_value('batchdate',nowtime[0])
                    item.add_value('all_count',all_count)
                
                    try:
                        pdf_content = yield Request(file_content, meta={'item': item},callback=self.parse_update, errback=self.error_update,
                                                dont_filter=True)
                    
                    except Exception as e:
#                         print("url is error")
                        logging.info("update url is error")
#                         print(e)
                        logging.info(e)
                        item.add_value('filedate','fail')
                        item.add_value('doc_id','fail')
                        item.add_value('file_name','fail')
                        
#                         self.write_dat(item.load_item())
        
                        summ = data_sum[0]
                        summ = summ + 1
                        data_sum[0] = summ
                        if all_count == summ and summ != 0:
                            exqute_cmd()
                            data_sum[0] = 0
#                         elif summ % 5 == 0 and summ != 0:
#                             print("sum % 5 == 0")
#                             exqute_cmd()
            
        

    def write_dat(self, item):
        
        datstr = ''
        source_code = item['source_code']
        if "fail" != source_code:
            datstr = datstr + source_code
        datstr = datstr + ','
        
        ann_code_dis = item['ann_code_dis']
        if "fail" != ann_code_dis:
            datstr = datstr + ann_code_dis
        datstr = datstr + ','
        
        code = item['code']
        if "fail" != code:
            datstr = datstr + code
        datstr = datstr + ','
        
        id= item['id']
        if "fail" != id:
            datstr = datstr + id
        datstr = datstr + ','
        
        file_content = item['file_content']
        if "fail" != file_content:
            datstr = datstr + file_content
        datstr = datstr + ','
        
        doc_id = item['doc_id']
        if "fail" == doc_id:
           datstr =  datstr + doc_id
        datstr = datstr + ','
        
        file_name = item['file_name']
        
        if "fail" != file_name:
            datstr =  datstr + file_name
        datstr = datstr + ','
        
        filedate = item['filedate']
        if "fail" != filedate:
#             datstr =  datstr + filedate
            datstr = datstr + DAT_DATA + "." + str(all_length[0]) + "." + str(len(filedate)) + "/"
            with open(datapath, 'ab') as f:
                f.write(filedate)
#                 f.write("\n")
                f.close()
                
            all_length[0] = all_length[0] + len(filedate)
#             with open(DATA_FILE_PATH+"/" + file_name + ".txt", 'wb') as f:
#                 f.write(filedate)
#                 f.close()
        else:
            datstr = datstr + DAT_DATA + "." + str(all_length[0]) + ".0/"
            
                
        datstr = datstr + ',' +  item['batchdate'] + "\n"
        

        # 打开文件，不存在则新建后打开,追加数据
        fp = open(filepath, 'a')
        # 写入数据
        fp.write(datstr)
        # 关闭文件
        fp.close()

        return

    #请求成功
    def parse_pdf(self, response):
        
        item = response.meta['item']
        pdf = base64.b64encode(response.body)
#         pdf = response.body
#         ann_code_dis = item.load_item()['ann_code_dis']
        all_count = item.load_item()['all_count']
        
        timechuo = str(int(time.time() * 1000))
        filename = ""
        try:
            
            filenames = response.headers.getlist('Content-Disposition')[0].split('.')
            ls = len(filenames)
            if ls >= 1:
                 filename = filenames[ls - 1]
        except Exception as e:
            print(e)
            
        filename = timechuo + "." + filename
        
        
        if 'ss7K/dPQzvOjrMfrvOyy6cr9vt3F5NbDoaM=' == pdf:
            item.add_value('filedate','fail')
            item.add_value('doc_id','fail')
            item.add_value('file_name','fail')
        else:
            item.add_value('filedate',pdf)
            item.add_value('doc_id','succ')
            item.add_value('file_name',filename)
        
        
        self.write_dat(item.load_item())
        
        summ = data_sum[0]
        summ = summ + 1
        data_sum[0] = summ
        if all_count == summ and summ != 0:
#             print("over    ")
            logging.info("over    ")
            exqute_cmd()
            data_sum[0] = 0
#             print("now time:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
#             logging.info("now time:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
#         elif summ % 5 == 0 and summ != 0:
#             print("sum % 5 == 0")
#             exqute_cmd()
            

    def error_back(self, response):
        
        from scrapy.spidermiddlewares.httperror import HttpError
        if isinstance(response.value,HttpError):
            response = response.value.response
        item = response.request.meta['item']
        
        all_count = item.load_item()['all_count']
        item.add_value('filedate','fail')
        item.add_value('doc_id','fail')
        item.add_value('file_name','fail')
        
        self.write_dat(item.load_item())
        
        summ = data_sum[0]
        summ = summ + 1
        data_sum[0] = summ
        if all_count == summ and summ != 0:
            exqute_cmd()
            data_sum[0] = 0
#         elif summ % 5 == 0 and summ != 0:
#             print("sum % 5 == 0")
#             exqute_cmd()
            
#         print 'fail: code=' + code + ",source_code="+ source_code + ",id=" + id
#         logging.info('fail')

    #请求成功
    def parse_update(self, response):
        item = response.meta['item']
        pdf = base64.b64encode(response.body)
        
        if 'ss7K/dPQzvOjrMfrvOyy6cr9vt3F5NbDoaM=' == pdf:
#             print 'url is error'
            logging.info('url is error')
        else:
#             ann_code_dis = item.load_item()['ann_code_dis']
            all_count = item.load_item()['all_count']
            code = item.load_item()['code']
            source_code = item.load_item()['source_code']
            id = item.load_item()['id']
            batchdate = item.load_item()['batchdate']
            
            timechuo = str(int(time.time() * 1000))
            filename = "fail"
            try:
                
                filenames = response.headers.getlist('Content-Disposition')[0].split('.')
                ls = len(filenames)
                if ls >= 1:
                     filename = filenames[ls - 1]
            except Exception as e:
                print(e)
            
            filename = timechuo + "." + filename
            
            
            item.add_value('filedate',pdf)
            item.add_value('doc_id','succ')
            item.add_value('file_name',filename)
             
            
            self.write_dat(item.load_item())
            
            delete_sql = "delete from spider.RH_GOVT_CONTRACT_OUT where BATCHDATE='" + batchdate + "' and CODE='" + code + "' and ID='" + id + "' and SOURCE_CODE='" + source_code + "'"
            logging.info(delete_sql)
            execute(delete_sql)
        
        
        summ = data_sum[0]
        summ = summ + 1
        data_sum[0] = summ
        if all_count == summ and summ != 0:
            exqute_cmd()
            data_sum[0] = 0
#         elif summ % 5 == 0 and summ != 0:
#             print("sum % 5 == 0")
#             exqute_cmd()
            
    def error_update(self, response):
        from scrapy.spidermiddlewares.httperror import HttpError
        if isinstance(response.value,HttpError):
            response = response.value.response
        item = response.request.meta['item']
        
        all_count = item.load_item()['all_count']
        code = item.load_item()['code']
        source_code = item.load_item()['source_code']
        id = item.load_item()['id']
        
      
        summ = data_sum[0]
        summ = summ + 1
        data_sum[0] = summ
        if all_count == summ and summ != 0:
            exqute_cmd()
            data_sum[0] = 0
#         elif summ % 5 == 0 and summ != 0:
#             print("sum % 5 == 0")
#             exqute_cmd()
#         print 'fail: code=' + code + ",source_code="+ source_code + ",id=" + id
        logging.info('fail')





#     def start_requests(self):

        # 获取输入表中所有数据get db sql data
#         query_sql = 'select FILE_CONTENT,SOURCE_CODE,ANN_CODE_DIS,CODE,ID,BATCHDATE from spider.RH_GOVT_CONTRACT_IN'
#         cust_list = queryAll(query_sql)

    #     #判断是否存在数据
    #     if len(cust_list) == 0:
    #         return
    #
    #     #循环获取pdf文件
    #     for cu in list(cust_list):
    #         #pdf文件所在url
    #         file_content = cu[0]
    #         print(file_content)
    #         source_code = cu[1]
    #         ana_code_dis = cu[2]
    #         code = cu[3]
    #         id = cu[4]
    #         batchdate = cu[5]
    #
    #         item = DownLoadPdfLoaderItem(item=DownLoadPdfResultItem())
    #         item.add_value('file_content', file_content)
    #         item.add_value('source_code', source_code)
    #         item.add_value('ana_code_dis', ana_code_dis)
    #         item.add_value('code', code)
    #         item.add_value('id', id)
    #         item.add_value('batchdate', batchdate)
    #
    #
    #         # yield Request(url=full_url, meta={'url': full_url}, callback=self.parse_item, errback=self.error_back, dont_filter=True)
    #         # pdf_content = yield Request(file_content,meta={'item': item},callback = self.parse_pdf)
    #         # print('+++++++++++++++++++++++++++++')
    #         # print(pdf_content)
    #         # pdf = base64.b64encode(pdf_content.body)
    #         # table_name = 'spider.RH_GOVT_CONTRACT_OUT'
    #         #pdf文件名称
    #         file_name = datetime.now().date().strftime('%Y%m%d%H%M%S')
    #         # self.save(file_content,source_code,ana_code_dis,code,id,file_name,pdf,batchdate,table_name,pdf_content)
    #
    #
    # def parse_pdf(self, response):
    #     item = response.meta['item']
    #
    #     pdf = base64.b64encode(response.body)
    #     item.add_value('filedate', pdf)
    #     print pdf
    #
    #     file_name = datetime.now().date().strftime('%Y%m%d%H%M%S')
    #     item.add_value('file_name', file_name)
    #
    #     item.add_value('table_name', 'spider.RH_GOVT_CONTRACT_OUT')
    #     return item.load_item()
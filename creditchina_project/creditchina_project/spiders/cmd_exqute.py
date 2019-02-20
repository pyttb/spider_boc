# -*- coding: utf-8 -*-
import commands
import os
import logging
# from ..settings import DAT_FILE_PATH,DATA_FILE_PATH,DAT_DATA


# local
# DAT_FILE_PATH = '/home/pd/download/pdf.dat'
# DATA_FILE_PATH = '/home/pd/download/lobs'
# DAT_DATA = 'new.dat'

# prd
DAT_FILE_PATH = '/usr/share/download/pdf.dat'
DATA_FILE_PATH = '/usr/share/download/lobs'
DAT_DATA = 'new.dat'


def exqute_cmd():
    #print(commands.getstatusoutput('db2 connect to iass;db2 "import from /home/pd/Desktop/pdf.dat of del insert into spider.RH_COVT_CONTRACT_OUT"'))
    # print(commands.getstatusoutput('db2 connect to iass;db2 "load from pdf.dat of del messages tmp.out insert into spider.RH_COVT_CONTRACT_OUT NONRECOVERABLE"'))
#     db2_sql = 'db2 connect to iass;db2 "load from '+ DAT_FILE_PATH +' of del messages tmp.out insert into spider.RH_COVT_CONTRACT_OUT NONRECOVERABLE"'
    db2_sql = 'db2 connect to iass;db2 "load from '+ DAT_FILE_PATH +' of del lobs from ' + DATA_FILE_PATH +  ' messages tmp.out insert into spider.RH_GOVT_CONTRACT_OUT NONRECOVERABLE"'
    file_path_sql = 'rm '+ DAT_FILE_PATH
    data_path_sql = 'rm ' + DATA_FILE_PATH + '/' + DAT_DATA
    # 判断文件是否存在，存在删除
    if os.path.exists(DAT_FILE_PATH) and os.path.exists(DATA_FILE_PATH + '/' + DAT_DATA):
        try:
            logging.info(commands.getstatusoutput(db2_sql))
#             print(db2_sql)
#             print(data_path_sql)
            logging.info(commands.getstatusoutput(file_path_sql))
            logging.info(commands.getstatusoutput(data_path_sql))
            logging.info("++++++++++++++end++++++++++++++")
        except Exception as e:
            print(e)

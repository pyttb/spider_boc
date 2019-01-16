# -*- coding: utf-8 -*-

# from scrapy.cmdline import execute
import sys
import os
import time
import logging
reload(sys)
sys.setdefaultencoding('utf-8')

while True:
    sleeptime = 3600
    print(sleeptime)
    logging.info("++++++++++++++cycle+++++++++++++++")
    logging.info("now time:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy', 'crawl', 'download_pdf'])
    nowtime_hour = int(time.strftime("%H"))
    nowtime_minite = int(time.strftime("%M"))
    print("nowtime:" + time.strftime("%Y-%m-%d %H:%M:%S"))
    if nowtime_hour > 8:
        print("now time > 8:30,stop cycle")
        time.sleep(sleeptime)
    elif nowtime_hour == 8 and nowtime_minite > 30 :
        print("now time > 8:30,stop cycle")
        time.sleep(sleeptime)
    else:
        os.system("scrapy crawl download_pdf")
    try: 
        with open("log.txt", 'rb+') as f:
            read_dataa = f.read()
            if len(read_dataa) > 1024*1024*2:
                print("truncate")
                f.seek(0)
                f.truncate()
            f.close()
    except Exception as e:
        print(e)
        

    logging.info("++++++++++++++end++++++++++++++")
    time.sleep(sleeptime) 
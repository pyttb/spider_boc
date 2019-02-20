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
#     sleeptime = 30
    print(sleeptime)
    logging.info("++++++++++++++cycle+++++++++++++++")
    logging.info("now time:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try: 
        print("is need remove log")
        with open("log.txt", 'rb+') as f:
            read_dataa = f.read()
            print(len(read_dataa))
            if len(read_dataa) > 1024*10:
                print("truncate")
                f.seek(0)
                f.truncate()
                print("remove log success")
            f.close()
            print("log excute")
    except Exception as e:
        print("remove log error")
        print(e)
    
#     execute(['scrapy', 'crawl', 'download_pdf'])
    nowtime_hour = int(time.strftime("%H"))
    nowtime_minite = int(time.strftime("%M"))
    print("nowtime:" + time.strftime("%Y-%m-%d %H:%M:%S"))
#     if nowtime_hour > 8:
    if nowtime_hour > 4:
        print("now time > 4:00,stop cycle")
    elif nowtime_hour == 4 and nowtime_minite > 30:
        print("now time > 4:30,stop cycle")
    else:
        os.system("scrapy crawl download_pdf")
        
    time.sleep(sleeptime)
    
       
    
# -*- coding: utf-8 -*-
import datetime
import time
import os
import sys
from WindPy import w
from dbutils import insertOne, insertMany, execute

# 加入MYSQL连接，测试使用MSYQLDB


reload(sys)
sys.setdefaultencoding('utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
yesterdayDt = datetime.date.today() - datetime.timedelta(1)
yesterday = str(yesterdayDt).replace('-', '')
w.start()

# 全部股票
# wind_stocks_all=w.wset("sectorconstituent","date=2019-01-02;sectorid=a001010100000000")


print ("===================== SPIDERMAN,HERE WE GO =====================")
print ("yesterdayDt:"+str(yesterdayDt))
print ("yesterday:"+yesterday)

print ("========清理当天已取股票数据========")
execute("delete from spider.WIND_STOCK_IASSUSER_INFO where datadt=" + yesterday, None)


print ("========取出全部股票代码,sectorid=1000013859000000========")
wind_stocks_all = w.wset("sectorconstituent", "date="+str(yesterdayDt)+";sectorid=a001010100000000")

wind_codes_all = wind_stocks_all.Data[1]
total_cnt = len(wind_codes_all)
print("总笔数："+str(total_cnt))

# wind_codes_all = ["000000.IB", "000001.IB"]
columns = "datadt,windcode,comp_name,sec_name,mkt,share_pledgeda_pct,share_pledgeda_pct_largestholder,pct_chg_3m,susp_days"
queryparams1 = "windcode,comp_name,sec_name,mkt,share_pledgeda_pct,share_pledgeda_pct_largestholder,pct_chg_3m,susp_days"
queryparams2 = "tradeDate="+yesterday+";cycle=D"

# 每次读取1000笔调用wind接口
MaxNum = 1000
print("总轮次：" + str(total_cnt/MaxNum + 1))
results = []
TimeOutError = []

while (len(wind_codes_all)!=0):
    wind_codes_1000 = ''
    current_cnt = 1
    for i in range(0, min(MaxNum, len(wind_codes_all))):
        wind_codes_1000 = wind_codes_1000 + wind_stocks_all.Data[1][0] + ","
        wind_codes_all.pop(0)
    try:
        datas = w.wss(wind_codes_1000, queryparams1, queryparams2)
        print ("当前时间:" + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
               + "  当前轮数:" + str(current_cnt)
               + "  现在处理股票:" + wind_codes_1000 )
        for i in range(0, len(datas.Data[0])):
            result = []
            result.append(yesterday)
            for j in range(0, len(datas.Data)):
                result.append(datas.Data[j][i])
            results.append(result)
        current_cnt = current_cnt + 1

    except TimeOutError as e:
        print('错误内容:', e)
#   finally:

    # print sql，暂时无法入库，没有DB2环境了
print ("INSERT INTO SPIDER.WIND_STOCK_IASSUSER_INFO ( " + columns + ") VALUES (? , ?, ?, ?, ? ,?, ?,?,?)", result)
insertMany("INSERT INTO SPIDER.WIND_STOCK_IASSUSER_INFO ( " + columns + ") VALUES (? , ?, ?, ?, ? ,?, ?,?,?)", results)

#drop table spider.WIND_STOCK_IASSUSER_INFO;
#create table spider.WIND_STOCK_IASSUSER_INFO(
#    datadt varchar(10),
#    windcode  varchar(20),
#    comp_name varchar(255),
#    sec_name varchar(255),
#    mkt varchar(255),
#    share_pledgeda_pct decimal(8,4),
#    share_pledgeda_pct_largestholder decimal(8,4),
#    pct_chg_3m decimal(20,16) ,
#    susp_days integer
#);
#
#comment on table spider.WIND_STOCK_IASSUSER_INFO is 'wind股票信息';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.datadt is '数据日期';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.windcode  is 'wind代码';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.comp_name is '公司中文名称';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.sec_name is '股票简称';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.mkt is '上市板';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.share_pledgeda_pct is '质押比例';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.share_pledgeda_pct_largestholder is '大股东累计质押数占持股数比例';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.pct_chg_3m is '近3月涨跌幅';
#comment on column spider.WIND_STOCK_IASSUSER_INFO.susp_days is '连续停牌天数';
# -*- coding: utf-8 -*-
import datetime
import os
import sys
from WindPy import w
from dbutils import insertOne, insertMany

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
# 全部债券

print ("===================== SPIDERMAN,HERE WE GO =====================")
print ("yesterdayDt:"+str(yesterdayDt))
print ("yesterday:"+yesterday)
print ("========取出全部债券代码,sectorid=1000013859000000========")
# wind_stocks_all=w.wset("sectorconstituentonstituent","date="+str(yesterdayDt)+";sectorid=1000013859000000")
wind_stocks_all=w.wset("sectorconstituent","date=2019-01-02;sectorid=a001010100000000")

print(wind_stocks_all)
wind_codes_all=wind_stocks_all.Data[1]

# wind_codes_all = ["000000.IB", "000001.IB"]
columns = "datadt,windcode,latestissurercreditrating,ratingoutlooks,latestissurercreditratingdate,rate_lateissuerchng,latestissurercreditratingtype"
queryparams = "windcode,latestissurercreditrating,ratingoutlooks,latestissurercreditratingdate,rate_lateissuerchng,latestissurercreditratingtype"

print ("========一次性取出数据，即可使用二维数据取数========")

datas = w.wss(wind_codes_all, queryparams)
# for i in range(0, 5): #测试使用5支债券即可
results = []
for i in range(0, len(wind_codes_all)):
    print ("现在处理债券:"+wind_codes_all[i]);
    # datas = w.wss(wind_codes_all[i], queryparams)
    result = []
    result.append(yesterday)
    # result.append(wind_codes_all[i])
    for j in range(0, len(datas.Data)):
        #result.append(datas.Data[j])
        result.append(datas.Data[j][i])
    results.append(result)

    # print sql，暂时无法入库，没有DB2环境了
    print ("INSERT INTO SPIDER.WIND_BOND_IASSUSER_INFO ( " + columns + ") VALUES (? , ?, ?, ?, ? ,?, ?)", results)

# insertMany(
#     "INSERT INTO SPIDER.WIND_BOND_IASSUSER_INFO ( "+columns+") "
#     "VALUES (? , ?, ?, ?, ? ,?, ?)"
#     , results
# )

# create table spider.WIND_BOND_IASSUSER_INFO(
#     datadt varchar(10),
#     windcode  varchar(20),
#     latestissurercreditrating  varchar(255),
#     ratingoutlooks  varchar(255),
#     latestissurercreditratingdate  varchar(255),
#     rate_lateissuerchng  varchar(255),
#     latestissurercreditratingtype  varchar(255)
# );

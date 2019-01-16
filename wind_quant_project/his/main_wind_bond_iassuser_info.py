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
# 全部债券

print ("===================== SPIDERMAN,HERE WE GO =====================")
print ("yesterdayDt:"+str(yesterdayDt))
print ("yesterday:"+yesterday)

print ("========清理当天已取债券数据========")
execute("delete from spider.WIND_BOND_IASSUSER_INFO where datadt=" + yesterday, None)

print ("========取出全部债券代码,sectorid=1000013859000000========")
wind_stocks_all=w.wset("sectorconstituent", "date="+str(yesterdayDt)+";sectorid=1000013859000000")

wind_codes_all = wind_stocks_all.Data[1]
total_cnt = len(wind_codes_all)
print("总笔数："+str(total_cnt))

# 每次读取1000笔调用wind接口
MaxNum = 1000
print("总轮次：" + str(total_cnt/MaxNum + 1))
results = []
TimeOutError = []

columns = "datadt,windcode,comp_name,latestissurercreditrating,ratingoutlooks,latestissurercreditratingdate,rate_lateissuerchng,latestissurercreditratingtype,deducteddebttoassets2"
queryparams = "windcode,comp_name,latestissurercreditrating,ratingoutlooks,latestissurercreditratingdate,rate_lateissuerchng,latestissurercreditratingtype,deducteddebttoassets2"

while (len(wind_codes_all)!=0):
    wind_codes_1000 = ''
    current_cnt = 1
    for i in range(0, min(MaxNum, len(wind_codes_all))):
        wind_codes_1000 = wind_codes_1000 + wind_stocks_all.Data[1][0] + ","
        wind_codes_all.pop(0)
    try:
        datas = w.wss(wind_codes_1000, queryparams)
        print ("当前时间:" + time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
               + "  当前轮数:" + str(current_cnt)
               + "  现在处理债券:" + wind_codes_1000 )
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

print("INSERT INTO SPIDER.WIND_BOND_IASSUSER_INFO ( " + columns + ") VALUES (? , ?, ?, ?, ? ,?, ? ,?,?)", results)
insertMany("INSERT INTO SPIDER.WIND_BOND_IASSUSER_INFO ( " + columns + ") VALUES (? , ?, ?, ?, ? ,?, ? ,?,?)", results)

# create table spider.WIND_BOND_IASSUSER_INFO(
#     datadt varchar(10),
#     windcode  varchar(20),
#     comp_name varchar(255),
#     latestissurercreditrating  varchar(255),
#     ratingoutlooks  varchar(255),
#     latestissurercreditratingdate  varchar(255),
#     rate_lateissuerchng  varchar(255),
#     latestissurercreditratingtype  varchar(255),
#     deducteddebttoassets2 varchar(255)
# );
# COMMENT ON TABLE spider.WIND_BOND_IASSUSER_INFO IS 'WIND债券信息';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.datadt IS '数据日期';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.windcode IS 'wind代码';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.comp_name IS '公司名称';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.latestissurercreditrating IS '发行人最新评级';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.ratingoutlooks IS '发行人最新评级展望';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.latestissurercreditratingdate IS '发行人最新评级日期';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.rate_lateissuerchng IS '发行人最新评级变动方向';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.latestissurercreditratingtype IS '发行人最新最低评级';
# COMMENT ON COLUMN spider.WIND_BOND_IASSUSER_INFO.deducteddebttoassets2 IS '剔除预收款项后的资产负债率';
# -*- coding: utf-8 -*-
from WindPy import w
from datetime import *
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame

reload(sys)
sys.setdefaultencoding('utf-8')

# 现在的日期
dt=datetime.now()

# 利用wset从Wind得到所有股票的代码
# wsetdata=w.wset('SectorConstituent','date=20160116;sectorId=a001010100000000;field=wind_code')
# wsetdata=w.wset("sharestructure","enddate=2018-02-28;sectorid=a002010100000000")

w.start()

w1=w.wsd("600000.SH","high","2012-05-09",datetime.today(),"Period=W")
w2=w.tquery(1,logonid=1,showfields='securitycode,Profit,securityBalance ')

print w1
print w2

# print wsetdata
# print wsetdata
# if wsetdata:
#     for j in range(0,len(wsetdata.Data[0])):
#         # 利用wss提取股票的成立时间
#         wssdata=w.wss(str(wsetdata.Data[0][j]),'ipo_date')
#         # 通过wsd来提取时间序列数据，比如取开高低收成交量，成交额数据
#         data=w.wsd(str(wsetdata.Data[0][j]), "open,high,low,close,volume,amt", wssdata.Data[0][0], dt, "Fill=Previous")
#         # 得到其中一只股票从IPO到现在的时间序列数据并存储在DataFrame中
#         df = DataFrame(data.Data, columns=data.Times, index=data.Fields).T
#         # 再讲DataFrame中的数据存储在CSV文件中，以后就可以通过read_csv直接读取CSV文件
#         df.to_csv(str(wsetdata.Data[0][j])+'.csv')
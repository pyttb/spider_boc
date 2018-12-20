# -*- coding: utf-8 -*-
import datetime
import os
import sys
from WindPy import w
from dbutils import insertOne, insertMany

reload(sys)
sys.setdefaultencoding('utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
yesterday = datetime.date.today() - datetime.timedelta(1)
yesterday = str(yesterday).replace('-', '')
w.start()
# ids = ['872725.OC,872726.OC']
ids = "000001.SZ,000002.SZ,000004.SZ,872747.OC,872751.OC".split(',')
MAXNUM = 100
while len(ids) > 0:
    tempids = ''
    current = len(ids)
    for idx in range(0, min(MAXNUM, current)):
        tempids = tempids + ids.pop(0) + ','
    if len(tempids) > 0:
        tempids = tempids[0:-1]
    results = []
    datas = w.wss(
        tempids,
        "comp_name,comp_name_eng,compprename,briefing,founddate,registernumber,regcapital,chairman,holder_controller,holder_pct,holder_name,wgsd_sales_oper,industry_CSRC12,industry_gics,industry_gicscode,indexcode_wind,employee,ceo,province,city,address,office,zipcode,phone,fax,email,website,discloser,auditor,stmnote_audit_cpa,clo",
        "tradeDate=" + yesterday + ";unit=1;order=1;rptDate=20161231;rptType=1;currencyType=;industryType=1;zoneType=1")
    for i in range(0, len(datas.Data[0])):
        result = []
        result.append(yesterday)
        for j in range(0, len(datas.Data)):
            result.append(datas.Data[j][i])
        results.append(result)
    insertMany(
        "INSERT INTO SPIDER.WIND_OC_RESULT (TRADE_DATE, COMP_NAME, COMP_NAME_ENG, COMPPRENAME, BRIEFING, FOUNDDATE, REGISTERNUMBER, REGCAPITAL, CHAIRMAN, HOLDER_CONTROLLER, HOLDER_PCT, HOLDER_NAME, WGSD_SALES_OPER, INDUSTRY_CSRC12, INDUSTRY_GICS, INDUSTRY_GICSCODE, INDEXCODE_WIND, EMPLOYEE, CEO, PROVINCE, CITY, ADDRESS, OFFICE, ZIPCODE, PHONE, FAX, EMAIL, WEBSITE, DISCLOSER, AUDITOR, STMNOTE_AUDIT_CPA, CLO) "
        "VALUES (? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        , results
    )

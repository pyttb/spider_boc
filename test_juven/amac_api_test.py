



# import requests
#
# #?rand=0.1822886326302735&page=0&size=20
# post_data = {'creditInfo':'isLostContractMechanism','rand':'0.12','page':'0','size':'20'}
# return_data=requests.post("http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=0&size=20",data=post_data)
# print return_data.text
#



import json
import requests
import scrapy

url='http://gs.amac.org.cn/amac-infodisc/api/pof/manager?page=0&size=20'
headers={
    'content-type': 'application/json',
    'referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    'Connection': 'keep_alive',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Host': 'gs.amac.org.cn',
    'Content-Length': '0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
payload={}
# payload={'creditInfo':'isLostContactMechanism'}
# r=requests.post(url,headers=headers,data=json.dumps(payload))
# r=requests.post(url,headers=headers,data=json.dumps(payload))
# print json.dumps(payload)
# print type(json.dumps(payload))
r=requests.post(url,headers=headers,data=json.dumps(payload))
print r.text


# print scrapy.Request(url=url)

# print scrapy.FormRequest(url=url,formdata=payload)

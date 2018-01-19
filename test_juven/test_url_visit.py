# -*- coding: utf-8 -*-
#



import urllib2


#不使用代理

import urllib2
response = urllib2.urlopen('http://www.nafmii.org.cn/zlgl/zwrz/xxpl/dxgjfx/')
html = response.read()
print("#不使用代理")
print(html)


# import requests
# import requests.packages.urllib3.util.ssl_
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
#
# # res = requests.get("https://www.cfae.cn/xxpl/dcm.html##")
# res = requests.get('https://www.cfae.cn/connector/selectAllInfoNew')
# print(res.text)


# URL	https://www.cfae.cn/connector/selectAllInfoNew
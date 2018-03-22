# -*- coding: utf-8 -*-
import urllib2

url = 'http://www.wind.com.cn/'
proxy = urllib2.ProxyHandler({'http': '61.160.190.147:8090'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
request = urllib2.Request(url)
response = urllib2.urlopen(request)


r=opener.open(url)
print(r.read())
# print response


# print urllib2.urlopen(url).read()

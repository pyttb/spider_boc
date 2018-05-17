# -*- coding: utf-8 -*-
import urllib2

# url = 'http://plat.chinecredit.com'
url = 'http://ss2.lawxp.com/s.aspx'
proxy = urllib2.ProxyHandler({'http': '114.215.83.184:3128'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
# request = urllib2.Request(url)
# response = urllib2.urlopen(request)

r=opener.open(url)
print(r.read())
# print response


# print urllib2.urlopen(url).read()

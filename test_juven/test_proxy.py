#coding=utf-8

import urllib2


#不使用代理

import urllib2
response = urllib2.urlopen('http://101.201.175.89/dist/#/login')
html = response.read()
print("#不使用代理")
print(html)


#使用代理访问
proxy_handler = urllib2.ProxyHandler({'http': '124.232.163.39:3128'})
opener = urllib2.build_opener(proxy_handler)
r = opener.open('http://101.201.175.89/dist/#/login')
print("#使用代理")
print(r.read())


# read
# urllib2是Python标准库，功能很强大，只是使用起来稍微麻烦一点。在Python 3中，urllib2不再保留，迁移到了urllib模块中。urllib2中通过ProxyHandler来设置使用代理服务器。
#
# proxy_handler = urllib2.ProxyHandler({'http': '121.193.143.249:80'})
# opener = urllib2.build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(r.read())
# 也可以用install_opener将配置好的opener安装到全局环境中，这样所有的urllib2.urlopen都会自动使用代理。
#
# urllib2.install_opener(opener)
# r = urllib2.urlopen('http://httpbin.org/ip')
# print(r.read())
# 在Python 3中，使用urllib。
#
# proxy_handler = urllib.request.ProxyHandler({'http': 'http://121.193.143.249:80/'})
# opener = urllib.request.build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(r.read())
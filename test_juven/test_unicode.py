# -*- coding: utf-8 -*-



# s1 = u"人生苦短"
# s2 = unicode("人生苦短", "utf-8")
# s3 = unicode(s1.encode("gbk"), "utf-8")
#
# print s1
# print s2
# print s3

# -*- coding:utf-8 -*-
s = "人生苦短"
# ： su是一个utf-8格式的字节串

u  = s.decode("utf-8")
# ： s被解码为unicode对象，赋给u

sg = u.encode("gbk")
# ： u被编码为gbk格式的字节串，赋给sg
print sg
# 打印sg
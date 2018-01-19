# -*- coding: utf-8 -*-

import os
# os.system('wget -r --spider http://diameizi.diandian.com 2>|log.txt')


url="http://www.chinamoney.com.cn/fe/CMS5_G20306002Resource?info=43424497;res=1516257745649208267055;download="
filename="盐城.pdf"

print ('wget -c "'+url+ '" -O '+filename)
os.system('wget -c "'+url+ '" -O '+filename)



#公告与提示>债券发行与上市>债券发行-chinamoney#
# URL   http://www.chinamoney.com.cn/fe/Channel/8651
# URL	http://www.chinamoney.com.cn/fe/jsp/CN/chinamoney/notice/beNewDraftByTremList.jsp
# http://www.chinamoney.com.cn/fe/Channel/47916?innerCode=4016126790&bondInfoType=6

#<td width="82%" class="row2-1-1"><a href="javascript:viewDraft('4016126790')" >陕西水务集团有限公司2018年度第一期中期票据申购说明</a></td>
#<td width="18%" class="row2-1">2018-01-18</td>
#实际PDF地址：http://www.chinamoney.com.cn/fe/CMS5_G20306002Resource?info=43426566;res=15162621132461807829843;download=
#落地文件名：2018-01-18_陕西水务集团有限公司2018年度第一期中期票据申购说明.pdf


# wget --post-data="FileName=P020180118343123865581.pdf&DownName=%E4%B8%9C%E8%8E%9E%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B82018%E5%B9%B4%E7%AC%AC003%E6%9C%9F%E5%90%8C%E4%B8%9A%E5%AD%98%E5%8D%95%E5%8F%91%E8%A1%8C%E5%85%AC%E5%91%8A.pdf"  "http://www.shclearing.com/wcm/shch/pages/client/download/download.jsp" -O 东莞银行股份有限公司2018年第003期同业存单发行公告.pdf
# 上海清算所_信息披露
# URL	http://www.shclearing.com/xxpl/fxpl/
# li><a href="./tycd1/201801/t20180118_340560.html" target="_blank">东莞银行股份有限公司2018年第003期同业存单发行公告</a>
# 						<span>2018-01-24</span>
# 					</li>
# javascript:download('./P020180118343123865581.pdf','东莞银行股份有限公司2018年第003期同业存单发行公告.pdf');
#URL	http://www.shclearing.com/wcm/shch/pages/client/download/download.jsp
#FileName	P020180118343123865581.pdf
#DownName	%E4%B8%9C%E8%8E%9E%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B82018%E5%B9%B4%E7%AC%AC003%E6%9C%9F%E5%90%8C%E4%B8%9A%E5%AD%98%E5%8D%95%E5%8F%91%E8%A1%8C%E5%85%AC%E5%91%8A.pdf
#
#



# 北京金融资产交易所
# https://www.cfae.cn/xxpl/dcm.html##
# URL	https://www.cfae.cn/connector/selectAllInfoNew

# title=&pageNumber=1&menuId=17&timeStart=&timeEnd=&bondShortName=&bondCode=&publishOrg=&leadManager=
# title=&menuId=70&pageNumber=1&timeStart=&timeEnd=
# title=&menuId=19&pageNumber=1&timeStart=&timeEnd=

# https://www.cfae.cn/connector/selectOnePortalView?infoId=16351
# https://www.cfae.cn/SFTP/download?fileName=%E6%9D%89%E6%9D%89%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B82018%E5%B9%B4%E5%BA%A6%E7%AC%AC%E4%B8%80%E6%9C%9F%E7%9F%AD%E6%9C%9F%E8%9E%8D%E8%B5%84%E5%88%B8%E6%B3%95%E5%BE%8B%E6%84%8F%E8%A7%81%E4%B9%A6(%E6%9B%B4%E6%AD%A3).pdf&fileAdd=2018/01/18/18/5895156d149c4806ba7cbb013032277b.pdf
# wget 不到,( )  需要替换为 \(   \)
# wget "https://www.cfae.cn/SFTP/download?fileName=%E6%9D%89%E6%9D%89%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B82018%E5%B9%B4%E5%BA%A6%E7%AC%AC%E4%B8%80%E6%9C%9F%E7%9F%AD%E6%9C%9F%E8%9E%8D%E8%B5%84%E5%88%B8%E6%B3%95%E5%BE%8B%E6%84%8F%E8%A7%81%E4%B9%A6\(%E6%9B%B4%E6%AD%A3\).pdf&fileAdd=2018/01/18/18/5895156d149c4806ba7cbb013032277b.pdf"  -O 杉杉集团有限公司2018年度第一期短期融资券法律意见书\(更正\).pdf





# 中国银行间市场交易商协会首页
# http://www.nafmii.org.cn/zlgl/zwrz/xxpl/dxgjfx/

# http://www.nafmii.org.cn/zlgl/zwrz/xxpl/dxgjfx/201606/P020160613389225938000.pdf

#wget "http://www.nafmii.org.cn/zlgl/zwrz/xxpl/dxgjfx/201606/P020160613389225938000.pdf" -O 无锡城东投资有限公司2016年度第一期非公开定向债务融资工具发行情况公告.pdf




















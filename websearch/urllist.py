# -*- coding: UTF-8 -*-
# urllist
# create at 2015/3/15
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
import chardet
from doclex import doclex

collection_urllist = None

urllist = ["http://abelkhan.com",
           "https://www.tmall.com",
           "http://www.tmall.com",
           "http://www.tmall.com?spm=a21bo.7724922.1997523009.3.N9av6u",
           "http://www.jd.com",
           "https://www.douban.com",
           "http://www.readnovel.com",
           "http://www.hongxiu.com",
           "http://www.zhulang.com",
           "http://www.kanshu.com",
           "https://www.hao123.com",
           "http://www.qq.com",
           "http://www.163.com",
           "http://www.tom.com",
           "http://sina.com.cn",
           "http://www.chinaunix.net",
           "http://www.iqiyi.com",
           "http://www.bilibili.com",
           "http://www.acfun.tv",
           "http://www.tudou.com",
           "http://www.youku.com",
           "https://www.tmall.com",
           "https://github.com",
           "http://cn.bing.com",
           "http://www.penbbs.com/forum.php",
           "http://www.zol.com.cn",
           "http://www.17173.com",
           "http://www.cnblogs.com",
           "http://www.csdn.net",
           "http://www.cppblog.com",
           'http://www.jobbole.com',
           "http://www.qidian.com/Default.aspx",
           "http://www.zongheng.com",
           "http://chuangshi.qq.com",
           "http://www.jjwxc.net",
           "https://www.taobao.com",
           "http://www.baidu.com",
           "http://www.google.com",
           "http://www.suning.com",
           "http://jiadian.gome.com.cn",
           'http://www.w3school.com.cn',
           "http://www.xitek.com",
           "http://codingnow.com",
           "http://jj.hbtv.com.cn",
           "http://www.weiqiok.com"]

prefixes = [u'http', u'https', u'www']

postfix = [u'com', u'cn', u'net', u'org', u'edu', u'gov', u'int', u'mil', u'ad', u'ae', u'af', u'ag', u'ai', u'al', u'am', u'an', u'ao', u'aq', u'ar', u'as', u'at', u'au', u'aw', u'az', u'ba', u'bb', u'bd',
           u'be', u'bf', u'bg', u'bh', u'bi', u'bm', u'bj', u'bn', u'bo', u'br', u'bs', u'bt', u'bv', u'bw', u'by', u'bz', u'ca', u'cc', u'cf']

def countweight(url):
    if url.count('/') > 2:
        return 0

    encodingdate = chardet.detect(url)
    if encodingdate['encoding']:
        uurl = unicode(url, encodingdate['encoding'])
        keywords = doclex.simplesplit(uurl)

        removelist = []
        for k in keywords:
            if k in prefixes:
                removelist.append(k)

            if k in postfix:
                removelist.append(k)

        for k in removelist:
            keywords.remove(k)

        if len(keywords) == 1:
            return 500

    return 400

def processurl(url):
    if url.count('/') == 2:
        collection_urllist.update({'url':url}, {'url':url}, True)

def refurllist():
    count = collection_urllist.find().count()
    c = collection_urllist.find()
    for i in c:
        if i['url'] not in urllist:
            urllist.append(i['url'])

    return urllist
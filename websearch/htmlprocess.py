# -*- coding: UTF-8 -*-
# htmlprocess
# create at 2016/2/25
# autor: qianqians

import HTMLParser
import urllist
import chardet
from doclex import doclex

def judged_url(url):
    if url is None or url.find('http') != 0:
        return False
    return True

def ingoreurl(url):
    count = 0
    for ch in url:
        if ch == '/':
            count += 1

    return count > 4

class htmlprocess(HTMLParser.HTMLParser):
    def __init__(self, urlinfo):
        HTMLParser.HTMLParser.__init__(self)

        self.urllist = {}
        self.sub_url = ""

        self.urlinfo = urlinfo
        self.current_url = urlinfo['url']

        if self.current_url == "https://www.tmall.com" or self.current_url == "http://www.tmall.com" or self.current_url.find("tmall") != -1:
            self.urlinfo['profile'].append(u"天猫（英文：Tmall，亦称淘宝商城、天猫商城）原名淘宝商城，是一个综合性购物网站。2012年1月11日上午，淘宝商城正式宣布更名为“天猫”。")

        self.weight = 0
        self.weight = urllist.countweight(self.current_url)

        encodingdate = chardet.detect(self.current_url)
        if self.current_url.count('/') == 2:
            if encodingdate['encoding']:
                uurl = unicode(self.current_url, encodingdate['encoding'])
                keywords = doclex.simplesplit(uurl)
                for k in keywords:
                    if k not in [u'http', u'https', u'www', u'com', u'cn', u'net', u'org', u'edu', u'gov', u'int', u'mil', u'ad', u'ae', u'af', u'ag', u'ai', u'al', u'am', u'an', u'ao', u'aq', u'ar', u'as', u'at', u'au', u'aw', u'az', u'ba', u'bb', u'bd', u'be', u'bf', u'bg', u'bh', u'bi', u'bm', u'bj', u'bn', u'bo', u'br', u'bs', u'bt', u'bv', u'bw', u'by', u'bz', u'ca', u'cc', u'cf']:
                        self.urlinfo['keys']['1'].append(k)

        self.current_tag = ""
        self.style = ""

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.style = 'None'
        self.sub_url = ""

        if tag == 'meta':
            for name,value in attrs:
                if name == 'name':
                    if value == 'keywords' or value == 'metaKeywords':
                        self.style = 'keywords'
                    elif value == 'description' or value == 'metaDescription':
                        self.style = 'profile'

            for name,value in attrs:
                if name == 'content':
                    try:
                        if isinstance(value, str):
                            encodingdate = chardet.detect(value)
                            if encodingdate['encoding']:
                                value = unicode(value, encodingdate['encoding'])

                        if self.style == 'keywords':
                            keywords = doclex.simplesplit(value)
                            if isinstance(keywords, list):
                                for key in keywords:
                                    self.urlinfo['keys']['1'].append(key)

                        elif self.style == 'profile':
                            self.urlinfo['profile'].append(value)

                            keys1 = doclex.lex(value)
                            for key in keys1:
                                self.urlinfo['keys']['2'].append(key)

                            keys1 = doclex.vaguesplit(value)
                            for key in keys1:
                                self.urlinfo['keys']['3'].append(key)

                            tlen = 16
                            if len(value) < 16:
                                tlen = len(value)
                            self.urlinfo['title'].append(value[0:tlen])

                    except:
                        import traceback
                        traceback.print_exc()

        if tag == 'a' or tag == 'A':
            self.sub_url = ""
            for name,value in attrs:
                if name == 'href':
                    if len(value) == 0:
                        return

                    if not judged_url(value):
                        if self.current_url[len(self.current_url) - 1] != '/' and value[0] != '/':
                            value = self.current_url + '/' + value
                        else:
                            value = self.current_url + value

                    if value.find('void') != -1:
                        return

                    if value.find('javascript') != -1:
                        return

                    if value.find('javaScript') != -1:
                        return

                    if self.current_url.find("apple") != -1:
                        if value.find("http://www.apple.com/cn/mac#ac-gn-menustate") !=-1:
                            return

                    if self.current_url.find("cnblogs") != -1:
                        if value.find("http://msg.cnblogs.com/send?recipient=itwriter") != -1:
                            return
                        elif value.find("http://i.cnblogs.com/EditPosts.aspx?opt=1") != -1:
                            return
                        elif value.find("http://i.cnblogs.com/EditPosts.aspx?postid=1935371") != -1:
                            return
                        elif value.find("http://msg.cnblogs.com/send?recipient=itwriter/") != -1:
                            return
                        elif value.find("http://msg.cnblogs.com/send?recipient=itwriter/GetUsername.aspx") != -1:
                            return
                        elif value.find("/EnterMyBlog.aspx?NewArticle=1") != -1:
                            return
                        elif value.find("GetUsername") != -1:
                            return
                        elif value.find("GetMyPassword") != -1:
                            return
                        elif value.find("http://i.cnblogs.com/EditPosts.aspx?postid=") != -1:
                            return
                        elif value[len(value) - 1] == '#':
                            value = value[0:-1]

                    if self.current_url.find(value) != -1:
                        return

                    if value[len(value) - 1] == '#':
                        value = value[0:-1]

                    if value != self.current_url and len(value) < 64 and not ingoreurl(value):
                        self.urllist[value] = {'url':value, 'keys':{'1':[], '2':[], '3':[]}, 'title':[], 'profile':[]}
                        self.sub_url = value

    def handle_data(self, data):
        if self.current_tag == 'title':
            try:
                encodingdate = chardet.detect(data)
                if encodingdate['encoding']:
                    data = unicode(data, encodingdate['encoding'])

                    if not doclex.invialddata(data):
                        if len(data) > 0:
                            self.urlinfo['title'].append(data)

                        keys = doclex.lex(data)
                        if isinstance(keys, list) and len(keys) > 0:
                            for key in keys:
                                self.urlinfo['keys']['2'].append(key)

                        keys = doclex.vaguesplit(data)
                        if isinstance(keys, list) and len(keys) > 0:
                            for key in keys:
                                self.urlinfo['keys']['3'].append(key)
            except:
                import traceback
                traceback.print_exc()

        elif self.current_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            try:
                encodingdate = chardet.detect(data)
                if encodingdate['encoding']:
                    data = unicode(data, encodingdate['encoding'])

                    if not doclex.invialddata(data):
                        if len(data) > 0:
                            self.urlinfo['title'].append(data)

                        keys = doclex.lex(data)
                        if isinstance(keys, list) and len(keys) > 0:
                            for key in keys:
                                self.urlinfo['keys']['2'].append(key)

                        keys = doclex.vaguesplit(data)
                        if isinstance(keys, list) and len(keys) > 0:
                            for key in keys:
                                self.urlinfo['keys']['3'].append(key)
            except:
                import traceback
                traceback.print_exc()

        elif self.current_tag == 'a' or self.current_tag == 'A':
            try:
                if self.sub_url != "":
                    encodingdate = chardet.detect(data)
                    if encodingdate['encoding']:
                        data = unicode(data, encodingdate['encoding'])

                        keys = doclex.simplesplit(data)
                        if isinstance(keys, list) and len(keys) > 0:
                            for key in keys:
                                if key in self.urllist[self.sub_url]['keys']['3']:
                                    self.urllist[self.sub_url]['keys']['3'].remove(key)
                                if key not in self.urllist[self.sub_url]['keys']['1'] and key not in self.urllist[self.sub_url]['keys']['2']:
                                    self.urllist[self.sub_url]['keys']['1'].append(key)

                        keys1 = doclex.lex(data)
                        for key in keys1:
                            self.urllist[self.sub_url]['keys']['2'].append(key)

                        keys1 = doclex.vaguesplit(data)
                        for key in keys1:
                            self.urllist[self.sub_url]['keys']['3'].append(key)

                        tlen = 16
                        if len(data) < 16:
                            tlen = len(data)
                        self.urllist[self.sub_url]['title'].append(data[0:tlen])

                        if len(data) > 32:
                            self.urllist[self.sub_url]['profile'].append(data[0:32])

            except:
                import traceback
                traceback.print_exc()
        else:
            if self.current_tag == 'div' or self.current_tag == 'p':
                try:
                    encodingdate = chardet.detect(data)
                    if encodingdate['encoding']:
                        data = unicode(data, encodingdate['encoding'])

                        if not doclex.invialddata(data):
                            data = doclex.delspace(data)

                            if data[0] == u'<':
                                return

                            if len(data) > 100:
                                tlen = 16
                                if len(data) < 16:
                                    tlen = len(data)
                                self.urlinfo['title'].append(data[0:tlen])

                                if len(data) > 32:
                                    self.urlinfo['profile'].append(data[0:32] + u"...")

                                keys1 = doclex.lex(data)
                                for key in keys1:
                                    self.urlinfo['keys']['2'].append(key)

                                keys1 = doclex.vaguesplit(data)
                                for key in keys1:
                                    self.urlinfo['keys']['3'].append(key)

                                self.weight += 200

                except:
                    import traceback
                    traceback.print_exc()
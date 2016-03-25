# -*- coding: UTF-8 -*-
# webanalysis
# create at 2016/2/25
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import cookielib
import time
import chardet
import urllist
import infosort
from doclex import doclex
from htmlprocess import htmlprocess

collection_url_index = None
collection_url_profile = None

def get_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
                   'Connection':'Keep-Alive',
                   'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
                   'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
                   }

        cookie_jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
        req = urllib2.Request(url = url, headers = headers)
        response = opener.open(req, timeout = 5)
        the_page = response.read()
        headers = response.info()

        return the_page, headers
    except:
        import traceback
        traceback.print_exc()

processed_url_list = []

def process_url(urlinfo):
    url = urlinfo['url']

    if url[len(url) - 1] == '/':
        url = url[0:len(url) - 1]
        urlinfo['url'] = url

    if url in processed_url_list:
        return "url is be processed"

    processed_url_list.append(url)

    print url,"process url"

    info = get_page(url)
    if info is None:
        print "url, error"
        return

    urllist.processurl(url)

    data, headers = info

    try:
        htmlp = htmlprocess(urlinfo)
        htmlp.feed(data)

        try:
            urlinfo = htmlp.urlinfo

            encodingdate = chardet.detect(headers['date'])
            date = unicode(headers['date'], encodingdate['encoding'])

            title = infosort.gettitle(urlinfo['title'])
            if len(title) > 16:
                title = title[0:16] + u'...'
            profile = infosort.getprofile(urlinfo['profile'])
            if title != u"" and profile != u"":
                print "update url", url
                collection_url_profile.update({'key':url} ,
                                              {'$set':{'key':url, 'urlprofile':profile.encode('utf-8', 'ignore'), 'timetmp':time.time(), 'date':date.encode('utf-8', 'ignore'), 'title':title.encode('utf-8', 'ignore')}},
                                              True)

                updatekeywords = []
                weight1 = []
                for key in urlinfo['keys']['1']:
                    if not doclex.inviald_key(key):
                        key = doclex.tolower(key)
                        key = key.encode('utf-8', 'ignore')
                        if key not in weight1:
                            weight1.append(key)
                for key in weight1:
                    if key not in updatekeywords:
                        updatekeywords.append(key)
                        collection_url_index.update({'key':key, 'url':url},
                                                    {'$set':{'url':url, 'key':key, 'weight':htmlp.weight+500}},
                                                    True)

                weight2 = []
                for key in urlinfo['keys']['2']:
                    if not doclex.inviald_key(key):
                        key = doclex.tolower(key)
                        key = key.encode('utf-8', 'ignore')
                        if key not in weight2:
                            weight2.append(key)
                for key in weight2:
                    if key not in updatekeywords:
                        updatekeywords.append(key)
                        collection_url_index.update({'key':key, 'url':url},
                                                    {'$set':{'url':url, 'key':key, 'weight':htmlp.weight+300}},
                                                    True)

                weight3 = []
                for key in urlinfo['keys']['3']:
                    if not doclex.inviald_key(key):
                        key = doclex.tolower(key)
                        key = key.encode('utf-8', 'ignore')
                        if key not in weight3:
                            weight3.append(key)
                for key in weight3:
                    if key not in updatekeywords:
                        updatekeywords.append(key)
                        collection_url_index.update({'key':key, 'url':url},
                                                    {'$set':{'url':url, 'key':key, 'weight':htmlp.weight}},
                                                    True)

        except:
            import traceback
            traceback.print_exc()

        urlinfolist = htmlp.urllist
        return urlinfolist

    except:
        import traceback
        traceback.print_exc()

def process_url_recursion(urlinfo):
    urlinfolist = process_url(urlinfo)

    if isinstance(urlinfolist, dict):
        for key, info in urlinfolist.iteritems():
            urlinfolist1 = process_url(info)
            if isinstance(urlinfolist1, dict):
                for key1, info1 in urlinfolist1.iteritems():
                    process_url(info1)
                    urlinfolist1[key1] = {}
            urlinfolist[key] = {}

def seach(urllist):
    global processed_url_list
    processed_url_list = []

    for url in urllist:
        try:
            print url, "root url"
            process_url_recursion({'url':url, 'keys':{'1':[], '2':[], '3':[]}, 'title':[], 'profile':[]})

        except:
            import traceback
            traceback.print_exc()
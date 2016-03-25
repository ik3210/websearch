# -*- coding: UTF-8 -*-
# webseach
# create at 2015/10/30
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../common/')
sys.path.append('../3part/')

import pymongo
import time
import urllist
import webanalysis
import keywords

if __name__ == '__main__':
    conn = pymongo.Connection('localhost',27017)
    db = conn.webseach

    webanalysis.collection_url_index = db.urlindex
    webanalysis.collection_url_profile = db.urlprofile
    keywords.collection_key = db.keys
    urllist.collection_urllist = db.urllist

    def run():
        t = 0
        while True:
            timetmp = time.time()-t
            if timetmp > 86400:
                keywords.refkeywords()
                t = time.time()
            urllist1 = urllist.refurllist()
            webanalysis.seach(urllist1)

    run()

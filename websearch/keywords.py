# -*- coding: UTF-8 -*-
# keywords
# create at 2016/3/16
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymongo
from doclex import doclex
import chardet

collection_key = None

def refkeywords():
    try:
        c = collection_key.find()
        keywords = []
        for it in c:
            key = it["key"]

            if isinstance(key, str):
                encodingdate = chardet.detect(key)
                key = unicode(key, encodingdate['encoding'])

            if key not in keywords:
                keywords.append(key)
        doclex.keykorks = keywords
    except:
        import traceback
        traceback.print_exc()
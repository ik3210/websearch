# -*- coding: UTF-8 -*-
# infosort
# create at 2016/3/23
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from doclex import doclex

def invaildinfo(str):
    count = 0
    for ch in str:
        if ch in doclex.punctuations or ch in doclex.numlist:
            count += 1
    
    if count > len(str)/2:
        return True
    
    return False

def gettitle(titlelist):
    removelist = []
    for ustr in titlelist:
        if invaildinfo(ustr):
            removelist.append(ustr)

    for ustr in removelist:
        titlelist.remove(ustr)    

    titlelist.sort(key=lambda x: len(x), reverse=True)
    
    if len(titlelist) > 0:
        return titlelist[0]
    else:
        return u''


def getprofile(profilelist):
    removelist = []
    for ustr in profilelist:
        if invaildinfo(ustr):
            removelist.append(ustr)

    for ustr in removelist:
        profilelist.remove(ustr)    

    profilelist.sort(key=lambda x: len(x), reverse=True)

    if len(profilelist) > 0:
        return profilelist[0]
    else:
        return u''
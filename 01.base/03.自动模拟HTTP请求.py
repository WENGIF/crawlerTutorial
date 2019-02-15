# -*- coding: utf-8 -*-
"""以登录CSDN/百度搜索简书为例"""

import urllib.request
import urllib.parse


def postData():
    '''1_POST方式登录CSDN'''
    values={}
    values['username'] = "xxx@qq.com" #账号
    values['password']="xxx" #密码
    info = urllib.parse.urlencode(values).encode("utf-8")
    url = "http://passport.csdn.net/account/login"
    try:
        req = urllib.request.Request(url,info)
        data = urllib.request.urlopen(req).read()
    except Exception as er: 
        print("异常概要：")
        print(er)
    return data


def getData():   
    '''2_GET方式搜索简书'''
    keyword = "简书" #搜索关键词
    keyword = urllib.request.quote(keyword)#编码
    url = "http://www.baidu.com/s?wd="+keyword
    try:
        req = urllib.request.Request(url)
        data = urllib.request.urlopen(req).read()
    except Exception as er: 
        print("异常概要：")
        print(er)
    return data   


if __name__=="__main__":
    print(postData())
    print(getData())
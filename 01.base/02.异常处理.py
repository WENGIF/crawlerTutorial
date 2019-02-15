# -*- coding: utf-8 -*-
"""以CSDN博客为例"""

#--------------------------------------------------
#（1）可捕获所有异常类型
import urllib.request
import urllib.error
import traceback
import sys

try:
    urllib.request.urlopen("http://blog.csdn.net")
except Exception as er1: 
    print("异常概要：")
    print(er1)
    print("---------------------------")
    errorInfo = sys.exc_info()
    print("异常类型："+str(errorInfo[0]))
    print("异常信息或参数："+str(errorInfo[1]))
    print("调用栈信息的对象："+str(errorInfo[2]))
    print("已从堆栈中“辗转开解”的函数有关的信息："+str(traceback.print_exc()))


#--------------------------------------------------
#（2）捕获URLError
import urllib.request
import urllib.error

try:
    urllib.request.urlopen("http://blog.csdn.net")
except urllib.error.URLError as er2: 
    if hasattr(er2,"code"):
        print("URLError异常代码：")
        print(er2.code)
    if hasattr(er2,"reason"):
        print("URLError异常原因：")
        print(er2.reason)


#--------------------------------------------------
#（3）捕获HTTPError
import urllib.request
import urllib.error

try:
    urllib.request.urlopen("http://blog.csdn.net")        
except urllib.error. HTTPError as er3: 
    print("HTTPError异常概要：")
    print(er3)

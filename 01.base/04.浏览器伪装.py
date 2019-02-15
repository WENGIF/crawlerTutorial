# -*- coding: utf-8 -*-
'''以CSDN博客为例'''

import urllib.request


url = "http://blog.csdn.net/"
headers=("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36") 
opener = urllib.request.build_opener() #自定义opener
opener.addheaders = [headers] #添加客户端信息
#urllib.request.install_opener(opener) #如解除注释，则可以使用方法2
try:
    data = opener.open(url,timeout=10).read()  #打开方法1
    #data=urllib.request.urlopen(url).read()  #打开方法2
except Exception as er:
    print("爬取的时候发生错误，具体如下：")
    print(er)
f = open("F:/spider_ret/csdnTest.html","wb") #创建本地HTML文件
f.write(data) #将首页内容写入文件中
f.close()
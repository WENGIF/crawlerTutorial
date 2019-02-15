# -*- coding: utf-8 -*-
"""以百度首页为例"""

import urllib.request


def use_proxy(url,proxy_addr,iHeaders,timeoutSec):
    '''
    功能：伪装成浏览器并使用代理IP防屏蔽
    @url：目标URL
    @proxy_addr：代理IP地址
    @iHeaders：浏览器头信息
    @timeoutSec：超时设置（单位：秒）
    '''
    proxy = urllib.request.ProxyHandler({"http":proxy_addr})
    opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        req = urllib.request.Request(url,headers = iHeaders)  #伪装为浏览器并封装request
        data = urllib.request.urlopen(req).read().decode("utf-8","ignore")  
    except Exception as er:
        print("爬取时发生错误，具体如下：")
        print(er)
    return data


if __name__ == "__name__":
    url = "http://www.baidu.com"
    proxy_addr = "125.94.0.253:8080"
    iHeaders = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0"}
    timeoutSec = 10
    data = use_proxy(url,proxy_addr,iHeaders,timeoutSec)
    print(len(data))
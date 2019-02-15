# -*- coding: utf-8 -*-
"""以豆瓣科幻电影为例"""

import urllib
from multiprocessing.dummy import Pool
import time


def getResponse(url):
    '''获取响应信息'''
    try:
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(req)
    except Exception as er:
        print("爬取时发生错误，具体如下：")
        print(er)
    return res


def getURLs():
    '''获取所需爬取的所有URL'''
    urls = []
    for i in range(0, 101,20):#每翻一页其start值增加20
        keyword = "科幻"
        keyword = urllib.request.quote(keyword)
        newpage = "https://movie.douban.com/tag/"+keyword+"?start="+str(i)+"&type=T"
        urls.append(newpage)
    return urls 


def singleTime(urls):
    '''单进程计时'''
    time1 = time.time()
    for i in urls:
        print(i)
        getResponse(i) 
    time2 = time.time()
    return str(time2 - time1)


def multiTime(urls):
    '''多进程计时'''
    pool = Pool(processes=4) #开启四个进程
    time3 = time.time()
    pool.map(getResponse,urls)
    pool.close()
    pool.join() #等待进程池中的worker进程执行完毕
    time4 = time.time()
    return str(time4 - time3) 


if __name__ == '__main__':
    urls = getURLs()
    singleTimes = singleTime(urls) #单线程计时  
    multiTimes = multiTime(urls) #多线程计时
    print('单线程耗时 : ' + singleTimes + ' s')
    print('多线程耗时 : ' + multiTimes + ' s')
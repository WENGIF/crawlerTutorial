# -*- coding: utf-8 -*-
"""以当当网为例"""

import urllib.request
import chardet


# 爬取网页
data = urllib.request.urlopen("http://www.dangdang.com/").read()

# ---------------------- 编码 ----------------------
# 查看编码格式
import chardet
chardet.detect(data)

# 解码
decodeData = data.decode("gbk")
# 重编码
dataEncode = decodeData.encode("utf-8","ignore")
decodeData2 = decodeData.encode("GB2312","ignore")


# ---------------------- 超时设置 ----------------------
data = urllib.request.urlopen(“http://www.dangdang.com/”,timeout=3).read()

import time
time.sleep(3)

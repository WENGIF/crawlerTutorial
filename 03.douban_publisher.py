# -*- coding: utf-8 -*-
"""豆瓣网出版社名字"""

import urllib
import re
import xlsxwriter
import MySQLdb


#-----------------(1)存储到excel与txt-------------------------#
def gxls_concent(target_url,pat):
    '''
    功能：爬取数据
    @target_url：爬取目标网址
    @pat：数据过滤模式
    '''
    data = urllib.request.urlopen(target_url).read()
    ret_concent = re.compile(pat).findall(str(data,'utf-8'))
    return ret_concent


def wxls_concent(ret_xls,ret_concent):
    '''
    功能：将最终结果写入douban.xls中
    @ret_xls：最终结果存储excel表的路径
    @ret_concent：爬取数据结果列表
    '''
    # 打开最终写入的文件
    wb1 = xlsxwriter.Workbook(ret_xls)
    # 创建一个sheet工作对象
    ws = wb1.add_worksheet()
    try:
        for i in range(len(ret_concent)):
            data = ret_concent[i]
            ws.write(i,0,data)
        wb1.close()
    except Exception as er:
        print('写入“'+ret_xls+'”文件时出现错误')
        print(er)    


def wtxt_concent(ret_txt,ret_concent):
    '''
    功能：将最终结果写入douban.txt中
    @ret_xls：最终结果存储excel表的路径
    @ret_concent：爬取数据结果列表
    '''
    fh = open(ret_txt,"wb")
    try:
        for i in range(len(ret_concent)):
            data = ret_concent[i]
            data = data+"\r\n"
            data = data.encode()
            fh.write(data)
    except Exception as er:
        print('写入“'+ret_txt+'”文件时出现错误')
        print(er)  
    fh.close()


def mainXlsTxt():
    '''
    功能：将数据存储到excel表中
    '''
    target_url = 'https://read.douban.com/provider/all'  # 爬取目标网址
    pat = '<div class="name">(.*?)</div>' # 爬取模式
    ret_xls = "F:/spider_ret/douban.xls"   # excel文件路径
    ret_txt = "F:/spider_ret/douban.txt"   # txt文件路径
    ret_concent = gxls_concent(target_url,pat) # 获取数据
    wxls_concent(ret_xls,ret_concent) # 写入excel表
    wtxt_concent(ret_txt,ret_concent) # 写入txt文件  
#---------------------END(1)--------------------------------#


#-------------------(2)存储到MySQL---------------------------#
def db_con():
    '''
    功能：连接MySQL数据库
    '''
    con = MySQLdb.connect(
        host='localhost',  # port
        user='root',       # usr_name
        passwd='xxxx',     # passname
        db='urllib_data',  # db_name
        charset='utf8',
        local_infile = 1
        )
    return con   


def exeSQL(sql):
    '''
    功能：数据库查询函数 
    @sql：定义SQL语句
    '''
    print("exeSQL: " + sql)
    #连接数据库
    con = db_con()
    con.query(sql)   


def gdb_concent(target_url,pat):
    '''
    功能：转换爬取数据为插入数据库格式:[[value_1],[value_2],...,[value_n]]
    @target_url：爬取目标网址
    @pat：数据过滤模式
    '''
    tmp_concent = gxls_concent(target_url,pat)
    ret_concent = []   
    for i in range(len(tmp_concent)):
        ret_concent.append([tmp_concent[i]])
    return ret_concent


def wdb_concent(tbl_name,ret_concent):
    '''
    功能：将爬取结果写入MySQL数据库中
    @tbl_name：数据表名
    @ret_concent：爬取数据结果列表
    '''
    exeSQL("drop table if exists " + tbl_name)
    exeSQL("create table " + tbl_name + "(pro_name VARCHAR(100));")
    insert_sql = "insert into " + tbl_name + " values(%s);"
    con = db_con()
    cursor = con.cursor()
    try:
        cursor.executemany(insert_sql,ret_concent)
    except Exception as er:
        print('执行MySQL："' + str(insert_sql) + '"时出错')        
        print(er)
    finally:
        cursor.close()        
        con.commit() 
        con.close()


def mainDb():
    '''
    功能：将数据存储到MySQL数据库中
    '''
    target_url = 'https://read.douban.com/provider/all'  # 爬取目标网址
    pat = '<div class="name">(.*?)</div>' # 爬取模式
    tbl_name = "provider" # 数据表名
    # 获取数据
    ret_concent = gdb_concent(target_url,pat)
    # 写入MySQL数据库
    wdb_concent(tbl_name,ret_concent)  
#---------------------END(2)--------------------------------#


if __name__ == '__main__':
    mainXlsTxt()
    mainDb()
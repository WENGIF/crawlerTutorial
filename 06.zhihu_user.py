# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 01:06:12 2017

@author: whenif
"""


####
####1、登录
####
import random
import requests
from bs4 import BeautifulSoup as BS
import time
from PIL import Image  # 打开图片
import re
import json
import os
import sys


def getReqHeaders():
    '''
    功能：随机获取HTTP_User_Agent
    '''
    user_agents=[
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"]
    user_agent = random.choice(user_agents)
    req_headers={
    'User-Agent':user_agent
    }
    return req_headers

def getXsrf(session):
    """
    功能：获取参数_xsrf
    """
    home_url = "https://www.zhihu.com"
    headers = getReqHeaders()
    xsrf = BS(session.get(home_url, headers=headers).text, "lxml").find("input", {"name": "_xsrf"})["value"]
    return xsrf

def showCaptcha(session):
    """
    功能：获取验证码本地显示，返回你输入的验证码
    """
    captcha_url = "http://www.zhihu.com/captcha.gif?r="+str(int(time.time() * 1000))+"&type=login"  #验证码url
    r = session.get(captcha_url, headers=getReqHeaders(), verify=True)
    with open("code.gif", 'wb') as f:
        f.write(r.content)
    #显示验证码
    try:
        print("请查看验证码...")
        img = Image.open("code.gif")
        img.show()
    except:
        print("请打开下载的验证码文件code.gif")


def usrLogin():
    """
    功能：登录
    """
    session = requests.session()
    account = input("请输入账户名:")
    password = input("请输入密码:")
    showCaptcha(session)
    captcha = input("请输入验证码:")
    xsrf = getXsrf(session)
    #确定账户类型
    if re.search(r'^1\d{10}$', account):
        print("使用手机登录中...")
        type="phone_num"
        login_url="https://www.zhihu.com/login/phone_num"      
    elif re.search(r'(.+)@(.+)', account):
        print("使用邮箱登录中...")
        login_url="https://www.zhihu.com/login/email"
        type="email"
    else:
        print("账户格式错误！")
        sys.exit(1)  
    login_data = { '_xsrf':xsrf
                  ,type:account
                  ,'password':password
                  ,'rememberme':'true'
                  ,'captcha':captcha
				  }
    res = session.post(login_url, data=login_data, headers=getReqHeaders(), verify=True)
    content = int((res.json())['r'])
    if content==0:
        print("登录成功")    
        saveCookies()
        os.remove("code.gif")
        session = readCookies()
        return session
    else:
        print("登陆失败！")
        print(res.json())
        
def saveCookies():
    with open("./"+"zhiHuCookies",'w')as f:
        json.dump(session.cookies.get_dict(),f)

def readCookies():
    session = requests.session()
    with open("./"+"zhiHuCookies") as f:
        cookies = json.load(f)
        session.cookies.update(cookies)
    return session

def reUsrLogin():
    """
    功能：若存在cookies文件，则可先清除后重新登录也可直接读取该cookies文件
    """
    print("如想清除cookies文件，请输入1，否则请输入0：")
    check_value = input()
    if check_value=='1':
        os.remove('zhiHuCookies')
        print("重新登录...")
        session = usrLogin()
    else:
        session = readCookies()
    return session    
    
	
def login(): 
    """
    主函数
    """
    if os.path.exists('zhiHuCookies'):
        session = reUsrLogin()
    else:
        session = usrLogin()	
    return session		

####
####2、信息爬取
####

import html
session = login()#获取登录session
usr_id = '/people/kinson-17'

def getUsrInfo(usr_id):
    """
    获取用户信息
    """
    #### （1）获取数据
    home_url = "https://www.zhihu.com"
    usr_url =  home_url+usr_id
    content = session.get(usr_url, headers=getReqHeaders()).text
    soup = BS(content, 'html.parser')
    data =  soup.find('div', attrs={'id': 'data'})
    if data is None:
        data = None
    else:
        data = data['data-state']
    data = html.unescape(data)  # 对转义 html 字符进行处理
    data = BS(data, 'html.parser').text  # 去除夹杂的 html 标签
    #### （2）数据解析
    try:
        # 防止解析到的 JSON 格式错误而引发异常
        json_data = json.loads(data)
    except ValueError:
        print('[error]解析到错误的 json 数据')
    
    entities = json_data['entities']
    # 提取各个用户信息
    users = entities['users']
    user_token = (list(users.keys()))[0]
    user = users[user_token]
    # 提取目标用户的个人信息
    usr_avatarUrlTemplate = None  # 用户头像
    usr_urlToken = None  # 用户标识
    usr_name = None  # 用户名
    usr_headline = None  # 用户自我介绍
    usr_locations = []  # 用户居住地
    usr_business = None  # 用户所在行业
    usr_employments = []  # 用户职业经历
    usr_educations = []  # 用户教育经历
    usr_description = None  # 用户个人描述
    usr_sinaWeiboUrl = None  # 用户新浪微博 URL
    usr_gender = None  # 用户性别
    usr_followingCount = None  # 正在关注用户的数目
    usr_followerCount = None  # 关注者的数目
    usr_answerCount = None  # 该用户回答问题的数目
    usr_questionCount = None  # 用户提问数目
    usr_voteupCount = None  # 用户获得赞同的数目

    if 'avatarUrlTemplate' in user:
        usr_avatarUrlTemplate = user['avatarUrlTemplate']

    if 'urlToken' in user:
        usr_urlToken = user['urlToken']

    if 'name' in user:
        usr_name = user['name']

    if 'headline' in user:
        usr_headline = user['headline']

    if 'locations' in user:
        for location in user['locations']:
            usr_locations.append(location['name'])

    if 'business' in user:
        usr_business = user['business']['name']

    if 'employments' in user:
        for employment in user['employments']:
            elem = {}
            if 'job' in employment:
                job = employment['job']['name']
                elem.update({'job': job})
            if 'company' in employment:
                company = employment['company']['name']
                elem.update({'company': company})
            usr_employments.append(elem)

    if 'educations' in user:
        for education in user['educations']:
            if 'school' in education:
                school = education['school']['name']
                usr_educations.append(school)

    if 'description' in user:
        usr_description = user['description']

    if 'sinaWeiboUrl' in user:
        usr_sinaWeiboUrl = user['sinaWeiboUrl']

    if 'gender' in user:
        usr_gender = user['gender']

    if 'followingCount' in user:
        usr_followingCount = user['followingCount']

    if 'followerCount' in user:
        usr_followerCount = user['followerCount']

    if 'answerCount' in user:
        usr_answerCount = user['answerCount']

    if 'questionCount' in user:
        usr_questionCount = user['questionCount']

    if 'voteupCount' in user:
        usr_voteupCount = user['voteupCount']    
    
    # 构造用户信息实体
    user_info = {'avatarUrlTemplate': usr_avatarUrlTemplate,
                 'urlToken': usr_urlToken,
                 'name': usr_name,
                 'headline': usr_headline,
                 'locations': usr_locations,
                 'business': usr_business,
                 'employments': usr_employments,
                 'educations': usr_educations,
                 'description': usr_description,
                 'sinaWeiboUrl': usr_sinaWeiboUrl,
                 'gender': usr_gender,
                 'followingCount': usr_followingCount,
                 'followerCount': usr_followerCount,
                 'answerCount': usr_answerCount,
                 'questionCount': usr_questionCount,
                 'voteupCount': usr_voteupCount}
    return user_info  

####
####3、爬取关注的人
####
import math
def getFollowingList(usr_info):
    """
    返回用户所关注的用户ID
    """
    usr_id = '/people/'+usr_info['urlToken']
    home_url = "https://www.zhihu.com"
    page_num = "?page=" 
    following = "/following"
    following_count = usr_info['followingCount']
    if following_count<=20:
        max_num = 1
    else:
        max_num = math.ceil(following_count/20)
    usr_id_list = []        
    for num in range(1,max_num+1):
        following_url = home_url+usr_id+following+page_num+str(num)
        res = session.get(following_url, headers=getReqHeaders())
        content = res.text
        soup = BS(content, 'html.parser')
        usr_ids = soup.find_all('h2', {'class': 'ContentItem-title'})
        for usr_id in usr_ids:
            usr_id_list.append((usr_id.div.span.div.div.a["href"])) 
    return usr_id_list
    

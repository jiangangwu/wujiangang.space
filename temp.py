#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests,time
from bs4 import BeautifulSoup
from datetime import datetime

def date2sec(t):
    # transfer date such as "2019/11/03 19:18" to seconds in order to compare
    if '/' in t:
        year = int(t.split("/")[0])
        month = int(t.split("/")[1])
        day = int(t.split("/")[2][0:2])
        hour = int(t.split(" ")[1].split(":")[0])
        minute = int(t.split(" ")[1].split(":")[1])
    if '-' in t:
        year = int(t.split("-")[0])
        month = int(t.split("-")[1])
        day = int(t.split("-")[2][0:2])
        hour = int(t.split(" ")[1].split(":")[0])
        minute = int(t.split(" ")[1].split(":")[1])      
    t = datetime(year, month, day, hour, minute, 0, 0)
    return (t - datetime(1970,1,1)).total_seconds()

def hour2date(t):
    # transfer date such as "8小时前" to "2019/11/03 19:18"
    if "小时前" in t:
        h = int(t.split("小时前")[0])
        t2 = time.localtime()
        t = str(t2.tm_year) + "-" + str(t2.tm_mon) + "-" + str(t2.tm_mday) + " " + str(t2.tm_hour - h) + ":" + str(t2.tm_min)
        if t2.tm_hour - h < 0:
            t = str(t2.tm_year) + "-" + str(t2.tm_mon) + "-" + str(t2.tm_mday -1) + " " + str(t2.tm_hour +24 - h) + ":" + str(t2.tm_min)
    if "分钟前" in t:
        m = int(t.split("分钟前")[0])
        t2 = time.localtime()
        t = str(t2.tm_year) + "-" + str(t2.tm_mon) + "-" + str(t2.tm_mday) + " " + str(t2.tm_hour) + ":" + str(t2.tm_min-m)
        if t2.tm_min - m < 0:
            t = str(t2.tm_year) + "-" + str(t2.tm_mon) + "-" + str(t2.tm_mday) + " " + str(t2.tm_hour - 1) + ":" + str(60 + t2.tm_min - m)
    return t


user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
headers={"User-Agent":user_agent,"Cookie":cookie}

a = []

# 链得得

# http://www.beekuaibao.com/newsflashes
#
#u1 = "http://www.beekuaibao.com"
#s1 = requests.get(u1, headers=headers).text.split('<div class="title" data-v-5b0403f0>')
#for i in range(1,len(s1)-1):
#    topic = s1[i].split('</div>')[0]
#    url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('"')[0]
#    s2 = requests.get(url, headers=headers).text.split('<div class="content">')
#    t = hour2date(s2[0].split('前</span>')[0].split('>')[-1] + '前')
#    body = s2[1].split('声明：')[-1].lstrip() + '\n（<a href="' + url + '">'  + '转自币快报，' + t + '</a>）\n'
#    a.append([date2sec(t),topic,url,t, body, 'toutiao'])



#u1 = "http://www.beekuaibao.com/newsflashes"
#s1 = requests.get(u1,headers=headers).text.split('<div class="title" data-v-5b0403f0>')
#for i in range(1,len(s1)):
#    topic = '快讯：' + s1[i].split('</div>')[0]
#    url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('" ')[0]
#    t = hour2date(s1[i].split('前</span>')[0].split('>')[-1] + '前')
#    body = s1[i].split('<div class="desc-container" data-v-5b0403f0>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自币世界，' + t + '</a>）\n'
#    a.append([date2sec(t),topic,url,t, body,'newsflash'])
  
#u1 = "https://www.bishijie.com/kuaixun/"
#s1 = requests.get(u1,headers=headers).text.split('<ul data-id=')[1:-1]
#date = requests.get(u1,headers=headers).text.split('<div class="live livetop ')[1].split('">')[0]
#for item in s1:
#    topic = '快讯：' + item.split('title="')[1].split('">')[0]
#    url = "https://www.bishijie.com" + item.split('href="')[1].split('" ')[0]
#    t = date + ' ' + item.split('</span>')[0].split('>')[-1]
#    print(t)
#    body = item.split('title="')[2].split('">\n')[1].split('</a>')[0].replace(' ','').lstrip() + '\n（<a href="' + url + '">' + '转自币世界，' + t + '</a>）\n'
#    a.append([date2sec(t),topic,url,t, body,'newsflash'])
# 


#u1 = "https://www.chaindd.com/"
#items = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml').find_all(class_="post_part clearfix")
#for item in items:
#    url = "https://www.chaindd.com" + item.a.get('href')
#    s2 = requests.get(url,headers=headers).text
#    topic = s2.split('</title>')[0].split('<title>')[1]
#    if '涨跌榜' in topic or '交易榜' in topic:
#        continue
#    t1 = s2.split('前<')[0].split('>')[-1] + '前'
#    t = hour2date(t1)
#    body = s2.split('<div class="inner">')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得，' + t + '</a>）\n'
#    a.append([date2sec(t),topic,url,t, body, 'toutiao'])
#



u1 = "http://www.beekuaibao.com"
s1 = requests.get(u1, headers=headers).text.split('<div class="title" data-v-5b0403f0>')
for i in range(1,len(s1)-1):
    topic = s1[i].split('</div>')[0]
    url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('"')[0]
    s2 = requests.get(url, headers=headers).text.split('<div class="content">')
    t = hour2date(s2[0].split('前</span>')[0].split('>')[-1] + '前')
    body = s2[1].split('声明：')[0].lstrip() + '\n（<a href="' + url + '">'  + '转自币快报，' + t + '</a>）\n'
    a.append([date2sec(t),topic,url,t, body, 'toutiao'])


















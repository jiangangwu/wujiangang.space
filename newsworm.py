#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:36:21 2019

@author: jiangang
"""


import requests,socket,time
from datetime import datetime
import datetime as dt
from bs4 import BeautifulSoup
import sqlite3
from markdown import markdown
import bleach
from time import sleep
import random
from dateutil.parser import parse
from jg import date2sec, hour2date, imgsize, body2html, insert3,checkTopic

socket.setdefaulttimeout(30)

user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/61.0.3163.100 Safari/537.36"
cookie="mediav=%7B%22eid%22%3A%22387123...b3574ef2-21b9-11e8-b39c-1bc4029c43b8"
headers={"User-Agent":user_agent,"Cookie":cookie}
socket.setdefaulttimeout(30)


while True:
    print(time.asctime())
    try:
        print()
        print()
        tag  = 'bikuaibao_newsflash'
        print(tag)
        u1 = "http://www.beekuaibao.com/newsflashes"
        s1 = requests.get(u1,headers=headers).text.split('<div class="title" data-v-5b0403f0>')
        a = []
        for i in range(1,len(s1)):
            topic = s1[i].split('</div>')[0]
            if checkTopic(topic) == 1:
                continue
            url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('" ')[0]
            try:
                t = hour2date(s1[i].split('前</span>')[0].split('>')[-1] + '前')
            except Exception as e:
                print("币快报快讯，时间用当前时间 %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s1[i].split('<div class="desc-container" data-v-5b0403f0>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自币快报，' + t + '</a>）\n'
            a.append([date2sec(t), topic, url, t, body, tag, body2html(body),436,'cn'])
        insert3(a)

    except Exception as e:
        print("币快报快讯，下载出出问题 %s" % e)
    
    try:
        print()
        print()
        tag = 'coindesk_news'
        print(tag)
        u1 = "https://www.coindesk.com/tech/"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []
        items = []
        items = s1.find_all(class_='typography__StyledTypography-owin6q-0 jASKws')
        items1 = s1.find_all(class_='typography__StyledTypography-owin6q-0 cyUtww')
        items.extend(items1)
        for item in items:
            url =[]
            url = 'https://coindesk.com' + item.find('a').get('href')
            topic = item.find('a').text
            if checkTopic(topic) == 1:
                continue
            try:
                t = (item.find('a').get('href')).replace('/layer2/','').replace('/tech/','')[:10]
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                print("coindesk 时间使用当前时间： %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            s = requests.get(url,headers=headers).text
            print('coindesk--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s.split('<div class="contentstyle__StyledWrapper-g5cdrh-0 gCDWPA">')[1].split('div class="Box-sc-1hpkeeg-0">')[0] + '\n（<a href="' + url + '">' + 'From: coindesk.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body.replace("&#8820;",'”'),tag, body2html(body),441,'en'])
        insert3(a)

    except Exception as e:
        print("coindex download error: %s" % e)    
    
    try:
        print()
        print()
        tag = 'jinse_news'
        print(tag)
        u1 = "https://www.jinse.com/blockchain/"
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []
        items = []
        items = s1.find_all(class_="font20")
        for item in items:
            url = item.a['href']            
            s = BeautifulSoup(requests.get(url,headers=headers).text,'lxml')
            try:
                topic = item.a['title']
                if checkTopic(topic) == 1:
                    continue
            except:
                continue
            con = 0
            for keyword in ['币','BTC','周报','后市分析','空头','早盘','震荡','行情','实时']:
                if keyword in topic:
                    con = 1
            if con == 1:
                continue
            sleep(1)
            try:
                t = s.find(class_="js-liveDetail__date").text.replace('\n','').replace(' ','').split('，')[0]
                if "前" in t:
                    t = hour2date(t)
                if '月' not in t:                        
                    t = parse(t)
                    t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('jinse_news--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            try:
                s1 = requests.get(url,headers=headers).text                
                body = s1.split('<div class="js-article" data-v-64e3d832>')[1].split('</div>')[0] + '\n（<a href="' + url + '">' + '转自金色财经，' + t + '</a>）\n'
            except:
                continue
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),437,'cn'])
        insert3(a)
        a = []
    except Exception as e:
        print("金色财经新闻下载时出现错误： %s" % e)
    
    try:
        print()
        print()
        tag = 'jinse_newsflash'
        print(tag)
        u1 = "https://www.jinse.com/lives"
        a = []    
        s1 = BeautifulSoup(requests.get(u1).text,'lxml')
        items = s1.find_all(class_="tit font20 font-w")
        for item in items:
            topic = item.a['title']
            if checkTopic(topic) == 1:
                continue
            url = item.a['href']
            s2 = requests.get(url,headers=headers).text
            sleep(1)
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('jinse_newsflash--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2.split('<div class="js-article" data-v-')[1][9:].split('</div>')[0] + '\n（<a href="' + url + '">' + '转自金色财经，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),437,'cn'])
        insert3(a)
        a = []
    except Exception as e:
        print("金色财经快讯下载时出现问题： %s" % e)
    
    try:
        tag = 'cointelegraph_news'
        print()
        print()
        print(tag)
        u1 = "https://cointelegraph.com/press-releases"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []    
        items = s1.find_all(class_="post-card-inline__header")
        for item in items:   
            url = 'https://cointelegraph.com' + item.find('a').get('href')
            topic = item.find(class_="post-card-inline__title").text
            if checkTopic(topic) == 1:
                continue
            s = requests.get(url,headers=headers).text
            try:
                t = s.split('<time datetime="')[1].split('"')[0]
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                print("cointelegraph: use current time, for: %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('cointelegraph--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s.split('<div class="post-content" data-v-2a0745c6>')[1].split("</div>")[0] + '\n（<a href="' + url + '">' + 'From: cointelegraph.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),440,'en'])
        insert3(a)
        a = []
    except Exception as e:
        print('cointelegraph dowload error: %s' % e)

    try:
        print()
        print()
        tag = 'chaindd_newsflash'
        print(tag)
        u1 = "http://www-test.liandede.com/nictation?t1654657347983"
        a = []
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        for item in s1.find_all(class_="w_tit"):
            topic = item.a.string
            if checkTopic(topic) == 1:
                continue
            url = item.a['href']
            s2 = requests.get(url,headers=headers).text
            sleep(1)
            try:
                t = s2.split('<span class="color-unclickable">')[1].split('</span>')[0]
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")                    
            except Exception as e:
                print("链得得，使用当前时间，因为： %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('链得得--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            try:
                body = s2.split('ChainDD）')[1].split('/>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得快讯，' + t + '</a>）\n'
            except Exception as e:
                print("8. %s" % e)
                body = s2.split('【链得得播报】')[1].split('</p>')[0].lstrip() + '\n（<a href="' + url + '">' + '转自链得得快讯，' + t + '</a>）\n'        
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),435,'cn'])
        insert3(a)
        a = []
    except Exception as e:
        print("9. %s" % e)
    
    try:    
        tag = 'cryptopotato_news'
        print()
        print()
        print(tag)
        u1 = "https://cryptopotato.com/"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []    
        items = s1.find_all(class_="media-heading entry-title")
        for item in items:   
            url = item.find('a').get('href')
            topic = item.find('a').text
            if checkTopic(topic) == 1:
                continue
            s = requests.get(url,headers=headers).text.split('<span class="breadcrumb_last" aria-current="page">')[1].split('<div class="rp4wp-related-posts rp4wp-related-post">')[0]
            try:
                t = s.split('<span class="last-modified-timestamp">')[1].split('</span>')[0]
                t = parse(t.replace('@',''))
                t = time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                print("11. %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s.split('<div class="coincodex-content">')[1].split('<div class="rp4wp-related-posts rp4wp-related-post">')[0].lstrip().replace("&#8217;","") + '\n（<a href="' + url + '">' + 'From: cryptopotato.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),439,'en'])
        insert3(a)
        a = []
    except Exception as e:
        print('cryptopotato download error: %s' % e)

    try:
        print()
        print()
        tag = 'babite_newsflash'
        print(tag)
        u1 = "https://www.8btc.com/news"    
        a = []
        s1 = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml')
        for item in s1.find_all(class_="flash-item"):
            try:
                topic = item.find(class_='flash-item__title link-dark-major').text.replace("\n",'').strip()
                if checkTopic(topic) == 1:
                    continue
            except Exception as e:
                print("topic class is not find: %s" % e)
                continue
            url = "https://www.8btc.com" + item.a['href']
            s2 = requests.get(url,headers=headers).text
            sleep(1)
            try:
                t = hour2date(s2.find(class_="time").text)
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t)
                t = time.strftime("%Y-%m-%d %H:%M")  
            except Exception as e:
                print("8比特快讯，使用当前时间，因为： %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2.split('<div class="bbt-html" data-v-7f057cc4>')[1] + '\n（<a href="' + url + '">'  + '转自巴比特快讯，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),433,'cn'])
        insert3(a)
        a = []
    except Exception as e:
        print("8比特快讯下载时出现问题： %s" % e)
    
    try:
        print()
        print()
        tag = 'babite_news'
        print(tag)
        u1 = "https://www.8btc.com/news"    
        a = []
        s1 = BeautifulSoup(requests.get(u1, headers=headers).text,'lxml')
        for item in s1.find_all(class_="article-info"):
            try:
                topic = item.h3.text.replace("\n",'').strip()
                if checkTopic(topic) == 1:
                    continue
            except Exception as e:
                print("topic class is not find: %s" % e)
                continue
            url = "https://www.8btc.com" + item.a['href']
            s2 = requests.get(url,headers=headers).text
            sleep(1)
            try:
                t = s2.find(class_="time").text
                if "前" in t:
                    t = hour2date(t)                        
                t = parse(t.replace('@',''))
                t = time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                print("8比特新闻，使用当前时间，因为： %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2.split('<div class="bbt-html" data-v-7f057cc4>')[1] + '\n（<a href="' + url + '">'  + '转自巴比特新闻，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t,body.replace("'",'"'),tag,body2html(body.replace("'",'"')),433,'cn'])
        insert3(a)
        a = []
    except Exception as e:
        print("8比特新闻下载时出现问题： %s" % e)

    try:
        print()
        print()
        tag = 'bikuaibao_news'
        print(tag)
        u1 = "http://www.beekuaibao.com"
        a = []
        s1 = requests.get(u1, headers=headers).text.split('<div class="title" data-v-5b0403f0>')
        for i in range(1,len(s1)-1):
            topic = s1[i].split('</div>')[0]
            if checkTopic(topic) == 1:
                continue
            url = "http://www.beekuaibao.com" + s1[i-1].split('href="')[-1].split('"')[0]
            s2 = requests.get(url, headers=headers).text.split('<article class="content">')
            sleep(1)
            try:
                t = hour2date(s2[0].split('前</span>')[0].split('>')[-1] + '前')
            except Exception as e:
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            body = s2[1].split('</article>')[0].lstrip() + '\n（<a href="' + url + '">'  + '转自币快报，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body, tag, body2html(body),436,'cn'])
        insert3(a)
        a = []
    except Exception as e:
        print("币快报下载时出现问题： %s" % e)

    try:    
        print()
        print()
        tag = 'thebitcoinnews_news'
        print(tag)
        u1 = "https://thebitcoinnews.com/category/bitcoin-news/"    
        s1 = BeautifulSoup(requests.get(u1,headers=headers).text,'lxml')
        a = []    
        items = s1.find_all(class_="td-module-thumb")
        for item in items:   
            url = item.find('a').get('href')
            topic = item.find('a').get('title') #s.split('<title>')[1].split('</title>')[0].replace('&#039;','').replace('&amp;','&').replace('&quot;',"'")
            if checkTopic(topic) == 1:
                continue
            s = requests.get(url,headers=headers).text
            try:
                t = s.split('<time class="entry-date updated td-module-date" datetime="')[1].split('">')[0]
                t = parse(t.replace('@',''))
                t = time.strftime("%Y-%m-%d %H:%M")
            except Exception as e:
                print("thebitcoinnews, use current time, for: %s" % e)
                t = time.strftime("%Y-%m-%d %H:%M:%S")
            print('bikuaibao--' + time.strftime("%Y-%m-%d %H:%M") + '--' + "%s--%s" % (t,topic))
            if len(s.split('td-adspot-title')[1].replace('<div></div>','').split('</div>')[1])<500:
                body = s.split('td-adspot-title')[1].replace('<div></div>','').split('</div>')[2].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + 'From: thebitcoinnews.com，' + t + '</a>）\n'
            else:
                body = s.split('td-adspot-title')[1].replace('<div></div>','').split('</div>')[1].split('</div>')[0].lstrip() + '\n（<a href="' + url + '">' + 'From: thebitcoinnews.com，' + t + '</a>）\n'
            a.append([date2sec(t),topic,url,t, body,tag, body2html(body),438,'en'])
        insert3(a)
        a = []
    except Exception as e:
        print('thebitcoinnews dowload error: %s' % e)

    sleep(random.randint(3600,4800))

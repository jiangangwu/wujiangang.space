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
        t = str(t2.tm_year) + "/" + str(t2.tm_mon) + "/" + str(t2.tm_mday) + " " + str(t2.tm_hour - h) + ":" + str(t2.tm_min)
        if t2.tm_hour - h < 0:
            t = str(t2.tm_year) + "/" + str(t2.tm_mon) + "/" + str(t2.tm_mday -1) + " " + str(t2.tm_hour +24 - h) + ":" + str(t2.tm_min)
    return t



# 金色财经
u1 = "https://www.jinse.com/news/blockchain/"
s1 = BeautifulSoup(requests.get(u1).text,'lxml')
items = s1.find_all(class_="col right")
a = []
for item in items:
    topic = "转载：" + item.a.string
    url = item.a['href']
    s = requests.get(url).text
    t = hour2date(s.split('class="time">')[1].split('</div>')[0])
    body = "\n原文地址：" + url + "\n" + s.split('js-article-detail">')[1].split('</div>')[0] 
    a.append([date2sec(t),topic,url,t, body])
# 巴比特
u1 = "https://www.8btc.com/news"
s1 = BeautifulSoup(requests.get(u1).text,'lxml')
for item in s1.find_all(class_="article-item-warp"):
    topic = item.img['alt']
    url = "https://www.8btc.com" + item.a['href']
    s2 = requests.get(url).text
    t = hour2date(s2.split('datatime')[1].split('>')[1].split('<')[0])
    body = "\n原文地址：" + url + "\n" + s2.split('class="bbt-html" data-v-76ec936b>')[1].split('</div>')[0]
    a.append([date2sec(t),topic,url,t, body])
# 按时间排序
ndx = list(range(len(a)))
swapped = True
while swapped:
    swapped = False
    for i in range(len(a)-1):
        if a[i][0] > a[i+1][0]:
            ndx[i], ndx[i+1] = ndx[i+1], ndx[i]
            swapped = True










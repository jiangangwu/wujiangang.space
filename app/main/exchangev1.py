# nohup python3 -u exchangev1.py > exchange.log 2>&1 &
import requests,socket
import hashlib
import json
import time
import numpy as np
import random

#############
## 相关参数 ##
#############

socket.setdefaulttimeout(30)

u = "https://spotapi.bijieex.com"
url_order = "/spot/v1/order/place"

apiKey = "6a940fb3-285b-4ff4-bce4-3074470971b3"
ts = int(time.time())
apiSecret = "cfa1f742-4ae0-46e8-9103-d08fc8068817"


key  = "ts=" + str(ts) + ",apiKey=" + apiKey + ",apiSecret=" + apiSecret
key_hash = hashlib.md5()
key_hash.update(key.encode(encoding='utf-8'))
key_md = key_hash.hexdigest().upper()

pj = "?" + "apiKey=" + apiKey + "&sign=" + key_md + "&ts=" + str(ts)

##############
## 循环操作 ##
#############

count = 0

while True:
    
    print()

    ## 睡眠
    
    if time.localtime(time.time()).tm_hour >= 0 and time.localtime(time.time()).tm_hour < 7:
        t = random.randint(10,120)
        print("Sleep for %d seconds ..." % t)
        time.sleep(t)
    elif time.localtime(time.time()).tm_hour >= 7 and time.localtime(time.time()).tm_hour < 9:
        t = random.randint(3,30)
        print("Sleep for %d seconds ..." % t)
        time.sleep(t)
    elif time.localtime(time.time()).tm_hour >= 9 and time.localtime(time.time()).tm_hour < 20:
        t = random.randint(3,20)
        print("Sleep for %d seconds ..." % t)
        time.sleep(t)
    elif time.localtime(time.time()).tm_hour >= 20 and time.localtime(time.time()).tm_hour < 22:
        t = random.randint(3,30)
        print("Sleep for %d seconds ..." % t)
        time.sleep(t)
    else:
        t = random.randint(5,40)
        print("Sleep for %d seconds ..." % t)
        time.sleep(t)

    ## 获取深度

    url_depth = u + "/spotMarket/v1/market/spot/depth/CNT-USDT/100"
    try:
        depth = requests.get(url_depth).text
    except Exception as e:
        print(e)
        continue
    depth = json.loads(depth)

    buys = depth["data"]["bid"]
    sells = depth["data"]["ask"]

    all_buys_p = []
    all_buys_q = []
    for buy in buys:
        all_buys_p.append(buy["price"])
        all_buys_q.append(buy["amount"])

    all_sells_p = []
    all_sells_q = []
    for sell in sells:
        all_sells_p.append(sell["price"])
        all_sells_q.append(sell["amount"])

    print("Total sells:%d" % sum(all_sells_q))
    print("Total buys:%d" % sum(all_buys_q))
    print("Total tickers of sells:%d" % len(all_sells_q))
    print("Total tickers of buys:%d" % len(all_buys_q))

    ## 24小时最高、最低价

    url_ticker = u + '/spotMarket/data/api/ticker/SPOT/CNT-USDT'
    try:
        tks = requests.get(url_ticker).text
    except Exception as e:
        print(e)
        continue
    tks_json = json.loads(tks)


    high = float(tks_json["data"]["high"]) * 1.05
    low = float(tks_json["data"]["low"]) * 0.95
    #current_price = round(random.uniform(low,high),4)

    print("24h high: %s" % tks_json["data"]["high"])
    print("24h low: %s" % tks_json["data"]["low"])
    print("24h change: %s" % tks_json["data"]["change"])
    print("24h turnover: %s" % tks_json["data"]["turnover"])
    
    ## 我的所有委托

    url_current_orders = "/spot/v1/order/query/openOrders"

    data_current_orders = {
        "pageNo":1,
        "pageSize":100,
        "symbol":"CNT/USDT",
        "apiKey": apiKey,
        "ts": ts,
        "sign": key_md
    }
    try:
        r_current_orders =requests.post(u + url_current_orders,data=json.dumps(data_current_orders),headers = {'Content-Type': 'application/json'})
    except Exception as e:
        print(e)
        continue
    
    r_current_orders_json = json.loads(r_current_orders.text)

    current_orders = []
    current_sells_id = []
    current_buys_id = []
    current_buys_p = []
    current_sells_p = []
    current_buys_q = []
    current_sells_q = []
    for order in r_current_orders_json["data"]["list"]:
        current_orders.append([order["orderId"],order["side"],order["price"],order["orderQty"]])
        if order["side"] ==1:
            current_sells_p.append(order["price"])
            current_sells_q.append(order["orderQty"])
            current_sells_id.append(order["orderId"])
        else:
            current_buys_p.append(order["price"])
            current_buys_q.append(order["orderQty"])                
            current_buys_id.append(order["orderId"])

    print("My sells: %d" % sum(current_sells_q))
    print("My buys: %d" % sum(current_buys_q))
    print("Other sells: %d" % (sum(all_sells_q) - sum(current_sells_q)))
    print("Other buys: %d" % (sum(all_buys_q) - sum(current_buys_q)))

        
    ## 撤单重挂
    
    if count > 1500 or count == 0:
        
        ## 撤销所有委托

        url_cancel = "/spot/v1/order/batchcancel"
        if len(current_buys_id) < 60:
            data_cancel = {
                "orderIds": current_buys_id[:5],
                "symbol":"CNT/USDT",
                "apiKey": apiKey,
                "ts": ts,
                "sign": key_md    
            }
            try:
                r_cancel =requests.post(u + url_cancel,data=json.dumps(data_cancel),headers = {'Content-Type': 'application/json'})
                print("Cancel all orders: %s" % r_cancel.text)
            except Exception as e:
                print(e)
                continue
        else:
            data_cancel = {
                "orderIds": current_buys_id[:5],
                "symbol":"CNT/USDT",
                "apiKey": apiKey,
                "ts": ts,
                "sign": key_md    
            }
            try:
                r_cancel =requests.post(u + url_cancel,data=json.dumps(data_cancel),headers = {'Content-Type': 'application/json'})
                print("Cancel all orders: %s" % r_cancel.text)
            except Exception as e:
                print(e)
                continue
            
        if len(current_sells_id) < 60:
            data_cancel1 = {
                "orderIds": current_sells_id[:5],
                "symbol":"CNT/USDT",
                "apiKey": apiKey,
                "ts": ts,
                "sign": key_md    
            }
            try:
                r_cancel1 =requests.post(u + url_cancel,data=json.dumps(data_cancel1),headers = {'Content-Type': 'application/json'})
                print("Cancel all orders: %s" % r_cancel1.text)
            except Exception as e:
                print(e)
                continue
        else:
            data_cancel = {
                "orderIds": current_sells_id[:5],
                "symbol":"CNT/USDT",
                "apiKey": apiKey,
                "ts": ts,
                "sign": key_md    
            }
            try:
                r_cancel =requests.post(u + url_cancel,data=json.dumps(data_cancel),headers = {'Content-Type': 'application/json'})
                print("Cancel all orders: %s" % r_cancel.text)
            except Exception as e:
                print(e)
                continue
        
        ## 产生挂单

        # day_range = round(random.uniform(101,124)/10000,4)

        current_price = round(random.uniform(0.105,0.12),4)

        p_buys = []
        q_buys = []

        q_buy_min = 2000000
        q_buy_max = 60000000

        for i in range(5):
            q_buys.append(round(random.uniform(q_buy_min,q_buy_max)/10000,4))
            p_buys.append(round(random.uniform(current_price*10000*0.3,current_price*10000)/10000,4))

        p_sells = []
        q_sells = []

        q_sell_min = 2000000
        q_sell_max = 4000000

        for i in range(5):
            q_sells.append(round(random.uniform(q_sell_min,q_sell_max)/10000,4))
            p_sells.append(round(random.uniform(current_price,current_price*10000*1.5)/10000,4))

        orders_sell = []
        for i in range(len(p_sells)):
            data_sell = {
                "orderQty":q_sells[i],
                "price":p_sells[i],
                "priceType":1, # 0市价，1限价
                "side": 1,     # 0买，  1卖
                "symbol": "CNT/USDT",
                "apiKey": apiKey,
                "ts": ts,
                "sign": key_md
            }
            try:
                r_sell =requests.post(u + url_order,data=json.dumps(data_sell),headers = {'Content-Type': 'application/json'})
                r_sell_json = json.loads(r_sell.text)
                if r_sell_json["code"] == 200:
                    orders_sell.append([i,p_sells[i],q_sells[i],r_sell_json["data"]["orderId"]])
            except:
                try:
                    r_sell =requests.post(u + url_order,data=json.dumps(data_sell),headers = {'Content-Type': 'application/json'})
                    r_sell_json = json.loads(r_sell.text)
                    if r_sell_json["code"] == 200:
                        orders_sell.append([i,p_sells[i],q_sells[i],r_sell_json["data"]["orderId"]])
                except:
                    try:
                        r_sell =requests.post(u + url_order,data=json.dumps(data_sell),headers = {'Content-Type': 'application/json'})
                        r_sell_json = json.loads(r_sell.text)
                        if r_sell_json["code"] == 200:
                            orders_sell.append([i,p_sells[i],q_sells[i],r_sell_json["data"]["orderId"]])
                    except Exception as e:
                        print(e)

        print("Put sell orders: %d" % len(orders_sell))                

        orders_buy = []
        for i in range(len(q_buys)):
            data_buy = { 
                "orderQty":q_buys[i],
                "price":p_buys[i],
               "priceType":1, # 0市价，1限价
                "side": 0,     # 0买，  1卖
                "symbol": "CNT/USDT",
                "apiKey": apiKey,
                "ts": ts,
                "sign": key_md
            }
            try:
                r_buy =requests.post(u + url_order,data=json.dumps(data_buy),headers = {'Content-Type': 'application/json'})
                r_buy_json = json.loads(r_buy.text)
                if r_buy_json["code"] == 200:
                    orders_buy.append([i,p_buys[i],q_buys[i],r_buy_json["data"]["orderId"]])
            except:
                try:
                    r_buy =requests.post(u + url_order,data=json.dumps(data_buy),headers = {'Content-Type': 'application/json'})
                    r_buy_json = json.loads(r_buy.text)
                    if r_buy_json["code"] == 200:
                        orders_buy.append([i,p_buys[i],q_buys[i],r_buy_json["data"]["orderId"]])
                except:
                    try:
                        r_buy =requests.post(u + url_order,data=json.dumps(data_buy),headers = {'Content-Type': 'application/json'})
                        r_buy_json = json.loads(r_buy.text)
                        if r_buy_json["code"] == 200:
                            orders_buy.append([i,p_buys[i],q_buys[i],r_buy_json["data"]["orderId"]])
                    except Exception as e:
                        print(e)
        print("Put buy orders: %d" % len(orders_buy))                
        count = 1


    ## 在交易量均值与0.5倍均值之间取随机数作为交易量

    url_depth = u + "/spotMarket/v1/market/spot/depth/CNT-USDT/1"

    try:
        depth0 = requests.get(url_depth).text
    except Exception as e:
        print(e)
        continue

    depth = json.loads(depth0)

    buy = depth["data"]["bid"]
    sell = depth["data"]["ask"]

    p_buy = buy[0]["price"]
    q_buy = buy[0]["amount"]
    p_sell = sell[0]["price"]
    q_sell = sell[0]["amount"]

    # if (p_sell-p_buy)/p_sell > 0.03:

    print("Current difference: %f " % round((p_sell-p_buy)/p_sell*100,2))
    rint = random.randint(1,60)
    print("@%s" % time.asctime(time.localtime(time.time())))
    
    if rint >= 1 and rint < 10:
        q0 = round(random.uniform((q_sell + q_buy)/4, (q_sell + q_buy)/2),4)
    elif rint >= 20 and rint < 30:
        q0 = round(random.uniform((q_sell + q_buy)/4, (q_sell + q_buy)/2),3)
    elif rint >= 30 and rint < 40:
        q0 = round(random.uniform((q_sell + q_buy)/4, (q_sell + q_buy)/2),2)
    elif rint >= 40 and rint < 50:
        q0 = round(random.uniform((q_sell + q_buy)/4, (q_sell + q_buy)/2),1)
    else:
        q0 = round(random.uniform((q_sell + q_buy)/4, (q_sell + q_buy)/2),0)

    p0 = round(random.uniform((p_sell + p_buy)/2*0.997, (p_sell + p_buy)/2*1.003),4)
    if count == 100:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 200:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 300:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 400:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 500:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 600:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 700:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 800:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 900:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 1000:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 1100:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 1200:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 1300:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if count == 1400:
        p0 = round(random.uniform((p_sell + p_buy)/2*0.99, (p_sell + p_buy)/2*1.01),4)
    if p0 < 0.1:
        p0 = round(random.uniform(0.101,0.105),4)

    if p0 > 0.12:
        p0 = round(random.uniform(0.115,0.12),4)
        
    if q0 < 100:
        q0 = random.randint(1000000,8000000)/10000
        
    if q0 > 400:
        q1 = q0 + random.randint(-200,200)
    else:
        q1 = q0

    data_sell = {
        "orderQty":q0,
        "price":p0,
        "priceType":1, # 0市价，1限价
        "side": 1,     # 0买，  1卖
        "symbol": "CNT/USDT",
        "apiKey": apiKey,
        "ts": ts,
        "sign": key_md
    }
    
        
    data_buy = { 
        "orderQty":q1,
        "price":p0,
        "priceType":1, # 0市价，1限价
        "side": 0,     # 0买，  1卖
        "symbol": "CNT/USDT",
        "apiKey": apiKey,
        "ts": ts,
        "sign": key_md
    }
    
    try:
        if random.randint(30,60) > 45:
            r_sell =requests.post(u + url_order,data=json.dumps(data_sell),headers = {'Content-Type': 'application/json'})
            time.sleep(random.randint(2,10))
            r_buy =requests.post(u + url_order,data=json.dumps(data_buy),headers = {'Content-Type': 'application/json'})
        else:
            r_buy =requests.post(u + url_order,data=json.dumps(data_buy),headers = {'Content-Type': 'application/json'})
            time.sleep(random.randint(2,10))
            r_sell =requests.post(u + url_order,data=json.dumps(data_sell),headers = {'Content-Type': 'application/json'})
        print(time.asctime( time.localtime(time.time())))
        print("Price %f, buy %f, sell %f" % (p0, q0, q1))
    except Exception as e:
        print(e)
        print("failed @%s" % time.asctime( time.localtime(time.time())))
    count = count + 1
    print("Count: %d" % count)

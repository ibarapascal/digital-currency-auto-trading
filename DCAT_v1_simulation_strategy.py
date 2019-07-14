'''
Created on Feb 28, 2018

@author: Pascal JING
'''

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests
import time
from mongoengine import *
from math import pow

MARKET_URL = "https://api.huobi.pro"


#'Timestamp': '2017-06-02T06:13:49'

def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)

    try:
        response = requests.get(url, postdata, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        #print("httpGet failed, detail is:%s,%s" %(response.text,e))
        print("httpGet failed, detail is:%s,%s" + str(e))
        return


# �ｿｽ�ｿｽﾈ｡KLine
def get_kline(symbol, period, size):
    """
    :param symbol
    :param period: �ｿｽ�ｿｽﾑ｡ﾖｵ�ｿｽ�ｿｽ{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: �ｿｽ�ｿｽﾑ｡ﾖｵ�ｿｽ�ｿｽ [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


class btcusdt1min(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False)
class btcusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False)
class bchusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 
class ethusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 
class etcusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 
class ltcusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 
class eosusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 
class xrpusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 
class htusdt(Document):
    time = IntField(required=True, unique=True)
    open = FloatField(required=True, unique=False)
    close = FloatField(required=True, unique=False)
    low = FloatField(required=True, unique=False)
    high = FloatField(required=True, unique=False)
    amount = FloatField(required=True, unique=False)
    vol = FloatField(required=True, unique=False)
    count = FloatField(required=True, unique=False) 


def read_DB(COLLECTIONS, time_min, time_max):
    
    result = []
    
    try:
        for data in COLLECTIONS.objects(time__gte = time_min, time__lte = time_max):
                
            result.append({'time': data.time, 'price':data.close})
                
        result.sort(key = lambda x:x['time'], reverse = True)   

    except Exception as e:
        pass
   
    return result


def mov_avg(data, row_length, method):

    result = 0
    
    if method == 0:
        for i in range(row_length):
            result += data[i]
        result = result / row_length
        
    if method == 1:
        for i in range(row_length):
            weight = row_length - i
            result += data[i] * weight
        weight_sum = (row_length + 1) * row_length / 2
        result = result / weight_sum
        
    return result


# only used for 1min data.
def check_data_continuous(data):#, method):
    
#     if '1min' in method:
#         period = 60
#     elif '5min' in method:
#         period = 300
#     elif '15min' in method:
#         period = 900
#     elif '60min' in method:
#         period = 3600
    period = 60    
    
    num = len(data) - 1
    t_start = data[num]['time']
    t_end = data[0]['time']
    t_delta = t_end - t_start
    
    Flag = False
    
    if t_delta == num * period:
        
        Flag = True
        print('Data check Success!')
        print('Data  numbers: ' + str(len(data)))
        print('Data start at: ' + str(t_start))
        print('Data  Stop at: ' + str(t_end))
        
        return Flag
    
    else:
        
        print('Data check failed! Unsatisfied data.')
        input('Paused here.')
        
        return Flag

# --------------------------------------------------------------------------------
# For main

TRADE_FEE = (1 - 0.002)# * 0.25)
SLIP_RATE = 1#0.998


CAL_STEP_LEN = 500


# For process

IC_USDT = 10000
IC_DC = 0

CAL_STEP_DELTA = 3

# -----------------------------------------------------------------------------------


def initialize_account(data):
    
    num = len(data) - 1 - CAL_STEP_LEN
    
    time = data[num]['time']
    price = data[num]['price']
    
    value_u = price * IC_DC + IC_USDT
    value_d = IC_DC + IC_USDT / price
    
    result = {'time': time, 'price': price, 'usdt': IC_USDT, 'dc': IC_DC, 'value_u': value_u, 'value_d': value_d, 'rate_a': 100,'rate_r': 100, 'd_rate_r': 100, 'd_rate_a': 100, 'rate_delta': 0} 

    return result


def trade(data_current, data_calculate, data_first):
    
#     0 to 1 : buy DC
#     -1 to 0 : sale DC
    
    time = data_calculate['time']
    price = data_calculate['p1']
    
    scale = data_calculate['p2']
    
    flag = False
    dc = 0
    usdt = 0
    
    if scale > 0:
        if data_current['usdt'] != 0:
            usdt = data_current['usdt'] * ( 1 - scale )
            dc = data_current['dc'] + data_current['usdt'] * scale / price * TRADE_FEE * SLIP_RATE
            flag = True
    
    if scale < 0:
        if data_current['dc'] != 0:
            dc = data_current['dc'] * ( 1 + scale)
            usdt = data_current['usdt'] + data_current['dc'] * ( - scale) * price * TRADE_FEE * SLIP_RATE
            flag = True
          
    value_u = price * dc + usdt
    value_d = dc + usdt / price
    
    rate_absolute = value_u / IC_USDT * 100
    rate_relative = rate_absolute * data_first['p1'] / data_calculate['p1'] 

    d_rate_r = ( rate_relative / data_current['rate_r'] - 1 ) * 100
    d_rate_a = ( rate_absolute / data_current['rate_a'] - 1 ) * 100
    
    rate_delta = d_rate_r + d_rate_a
    
#     rate_relative = round(rate_relative, 4)
#     rate_absolute = round(rate_absolute, 4)
#     d_rate_r = round(d_rate_r, 4)
#     d_rate_a = round(d_rate_a, 4)
#     rate_delta = round(rate_delta, 4)
    
    result = {'time': time, 'price': price, 'usdt': usdt, 'dc': dc, 'value_u': value_u, 'value_d': value_d, 'rate_a': rate_absolute, 'rate_r': rate_relative,'d_rate_a': d_rate_a, 'd_rate_r': d_rate_r, 'rate_delta': rate_delta}
    
    return flag, result


def calculate(data, flag):
    
    scale = 0
    p3 = []
    p4 = []
    p5 = []
    p7 = []
    p6 = []
    p8 = []
    p9 = []
    p10 = []
    
    for i in range(CAL_STEP_DELTA):
        temp = data[i : i + CAL_STEP_LEN - CAL_STEP_DELTA + 1]
        
        d = []
        for j in range(len(temp)):
            d.append(temp[j]['price'])

        p3.append(mov_avg(d, 6, 1))
        p4.append(mov_avg(d, 18, 1))
        p5.append(mov_avg(d, 36, 1))
        p6.append(mov_avg(d, 72, 1))
        p7.append(mov_avg(d, 216, 1))
        p8.append(mov_avg(d, 36, 1) - mov_avg(d, 216, 1)) #DEFAULT V1.0
#         p8.append(mov_avg(d, 36, 1) - mov_avg(d, 108, 1))
#         p8.append(mov_avg(d, 48, 1) - mov_avg(d, 216, 1))
#         p8.append(mov_avg(d, 18, 1) - mov_avg(d, 72, 1))
    
        e = []
        for k in range(int(CAL_STEP_LEN / 2)):
            temp2 = d[k : k + int(CAL_STEP_LEN / 2) - 1]
            e.append(pow(mov_avg(temp2, 36, 1) - mov_avg(temp2, 216, 1),2)) #DEFAULT V1.0
#             e.append(pow(mov_avg(temp2, 36, 1) - mov_avg(temp2, 72, 1),2))
        
#         p9.append(mov_avg(d, 216, 1) - 2 * pow(mov_avg(e, 216, 1),0.5)) #DEFAULT V1.0
#         p10.append(mov_avg(d, 216, 1) + 2 * pow(mov_avg(e, 216, 1),0.5)) #DEFAULT V1.0
        p9.append(mov_avg(d, 216, 1) - 2.4 * pow(mov_avg(e, 216, 1),0.5))
        p10.append(mov_avg(d, 216, 1) + 2.4 * pow(mov_avg(e, 216, 1),0.5))
#         p9.append(mov_avg(d, 72, 1) - 2 * pow(mov_avg(e, 72, 1),0.5))
#         p10.append(mov_avg(d, 72, 1) + 2 * pow(mov_avg(e, 72, 1),0.5))
    '''
#     V1
#     fee = 0.002
#     scale_c = 0.8
#     DB1: rr:114.221% ra:108.861% rrm:-9.711% ram:-3.496%
#     DB2: rr:104.270% ra:101.044% rrm:-4.191% ram:-5.421%
    
#     Compare group:
#     BP: 2   101.890% 98.303%
#     BP: 2.5 101.704% 98.325%
#     analysis: in V1.0 BOLL just used as flag, so BP value not important
    
    scale_c = 0.8
#     scale_c = 1
    
    if p3[0] < p9[0] and p3[1] > p9[1]: flag['BOLL'] = 'BELLOW'
    if p3[0] > p10[0] and p3[1] < p10[1]: flag['BOLL'] = 'ABOVE'
    
    if p3[0] < p3[1] and p4[0] < p4[1] and p5[0] < p5[1] and p6[0] < p6[1]:
        if flag['BOLL'] == 'BELLOW':
            if p8[0] > p8[1] and p8[1] < p8[2]:
                scale = scale_c #buy
                flag['BOLL'] = 'DEFAULT'
        if p8[0] > 0:
            if p8[0] < p8[1] and p8[1] > p8[2]: 
                scale = - scale_c #sale
                
    if p3[0] > p3[1] and p4[0] > p4[1] and p5[0] > p5[1] and p6[0] > p6[1]:
        if flag['BOLL'] == 'ABOVE':
            if p8[0] < p8[1] and p8[1] > p8[2]:
                scale = - scale_c #sale
                flag['BOLL'] = 'DEFAULT'
        if p8[0] < 0:
            if p8[0] > p8[1] and p8[1] < p8[2]:
                scale = scale_c #buy
    '''
    
#     TEST3 BOLL strict with different scale
#     TEMP1 101.607% 98.331%

#     default 36,216 trade time:11
#     if 18,72 trade time:19 , while income rate down
#     if 72,216 no trade time:0
#     if 48,216 trade time:7 , while max income rate lower and total rate down.

#     default boll param 2 trade time:11
#     if 3 trade time:0
#     if 2.5 trade time:3 , while max income rate lower but increase the total performance!!
#     TEMP1 102.322% 100.263%
#     if 2.3 trade time:7
#     TEMP1 101.996% 99.516%

#     change boll param to 2.5
#     default scale_c: 1
#     if scale_c: 0.8 , trade time up to 40 , while increase the total performance.
#     TEMP1 104.179% 100.221%
#     TEMP1 103.704% 100.221%
#     if scale_c: 0.1
#     TEMP1 103.555% 100.060%

#     >>>Need more test with DB
#     1, 2.5
#     1, 2.3
#     0.8, 2.5
#     0.2, 2.5
#     maybe different method with different BP value
#     BTC, BCH better (2.4, 2.2)

#     >>>Maybe find some other method bellow
#     for example change scale with other strategy part

    scale_c = 1

    if p3[0] < p9[0] or p3[1] < p9[1] or p3[2] < p9[2]:
        if p8[0] > p8[1] and p8[1] < p8[2]:
            scale = scale_c
            flag['BOLL'] = 'BELLOW'    
    if p3[0] > p9[0] or p3[1] > p9[1] or p3[2] > p9[2]:
        if p8[0] < p8[1] and p8[1] > p8[2]:    
            scale = - scale_c
            flag['BOLL'] = 'ABOVE'
       
#     if add this part, trade time up to 55. 
#     Not useful
#
#     scale_d = 0.2
#          
#     if flag['BOLL'] == 'BELLOW':
#         if p8[0] > 0:
#             if p8[0] < p8[1] and p8[1] > p8[2]:
#                 scale = - scale_d
#                 flag['BOLL'] = 'DEFAULT'
#     if flag['BOLL'] == 'ABOVE':
#         if p8[0] < 0:
#             if p8[0] > p8[1] and p8[1] < p8[2]: 
#                 scale = scale_d
#                 flag['BOLL'] = 'DEFAULT'
    
                
    result = {'time':data[0]['time'], 'p1':data[0]['price'], 'p2':scale}
          
    return result, flag

# ------------------------------------------------------------------
# 20180301



# ----------------------------------------------------------------
# 20180228

    '''
#    TEST2 CHANGE if 
    scale_c = 0.8
    
    if p3[0] < p9[0] and p3[1] > p9[1]: flag['BOLL'] = 'BELLOW'
    if p3[0] > p10[0] and p3[1] < p10[1]: flag['BOLL'] = 'ABOVE'
    
    if p4[0] < p5[0] < p6[0] and p4[0] < p4[1] and p5[0] < p5[1] and p6[0] < p6[1]:
        if flag['BOLL'] == 'BELLOW':
            if p8[0] > p8[1] and p8[1] < p8[2]:
                scale = scale_c #buy
                flag['BOLL'] = 'DEFAULT'
        if p8[0] > 0:
            if p8[0] < p8[1] and p8[1] > p8[2]: 
                scale = - scale_c #sale
                
    if p4[0] > p5[0] > p6[0] and p4[0] > p4[1] and p5[0] > p5[1] and p6[0] > p6[1]:
        if flag['BOLL'] == 'ABOVE':
            if p8[0] < p8[1] and p8[1] > p8[2]:
                scale = - scale_c #sale
                flag['BOLL'] = 'DEFAULT'
        if p8[0] < 0:
            if p8[0] > p8[1] and p8[1] < p8[2]:
                scale = scale_c #buy
    '''

    '''
#     TEST1 BOLL
    scale_c = 1
    if flag['BOLL'] == 'DONE-SELL' and p3[0] < p9[0]:flag['TF1'] = 'BOTTOM'
    if flag['BOLL'] == 'DONE-BUY' and p3[0] > p9[0]:flag['TF1'] = 'TOP'
        
    if flag['TF1'] == 'BOTTOM' and p8[0] > p8[1] and p8[1] < p8[2]:
        scale = scale_c
        flag['BOLL'] = 'DONE-BUY'
    if flag['TF1'] == 'TOP' and p8[0] < p8[1] and p8[1] > p8[2]:
        scale =  - scale_c
        flag['BOLL'] = 'DONE-SELL'
    '''
                

def main():
    
#     for DCAT_beta_historydata
#     and DCAT_beta_historydata2
#     use METHOD = btcusdt1min
#     
#     for DCAT_beta_historydata3
#     use METHOD = btcusdt, ethusdt and so on.

# --------------------------------------------------------------------------------
    '''  
    MONGO_DB = 'DCAT_beta_historydata'
#    MONGO_DB = 'DCAT_beta_historydata2'
    connect(MONGO_DB, host='localhost', port=27017)
    METHOD = btcusdt1min
    r = read_DB(METHOD, 0, int(get_timestamp()['data']/1000))
    '''
    F_continue = True
    while(F_continue):
        a = get_kline('btcusdt', '1min', '2000')['data']
        if len(a) == 2000:
            F_continue = False
    r = []
    for i in range(len(a)):
        r.append({'time': a[i]['id'], 'price': a[i]['open']})
    r.sort(key = lambda x:x['time'], reverse = True)
            
#  -----------------------------------------------------------------------------------

    if check_data_continuous(r):
        
        cd = []
        
#         V1
#         flag = {'BOLL':'DEFAULT'}#, 'DIRECTION': 'DEFAULT'}
        
#         TEST BOLL
#         flag = {'BOLL': 'DONE-SELL', 'TF1': 'DEFAULT'}

        flag = {'BOLL':'DEFAULT'}
        
        for i in range(len(r) - CAL_STEP_LEN + 1):

            rd = r[len(r) - 1 - CAL_STEP_LEN - i : len(r) - 1 - i]
            if rd != []:
                result = calculate(rd, flag)
                cd.append(result[0])
                flag = result[1]
            else:
                break
            print(str(i))
            
        cd.sort(key = lambda x:x['time'], reverse = True)

        ad = []
        ad.append(initialize_account(r))
        
        for i in range(len(cd)):
            
            ad_current = ad[len(ad) - 1]
            n = len(cd) - 1 - i
            m = len(cd) - 1
            
            result = trade(ad_current, cd[n], cd[m])
            
            if result[0]:     
                ad.append(result[1])
            
        ad.sort(key = lambda x:x['time'], reverse = True)
        
        for i in range(len(ad)):
            j = len(ad) - 1 - i
# print('%10.1f'%r)
            print(ad[j]['time'], '%5.4f'%ad[j]['rate_r'], '%5.4f'%ad[j]['rate_a'], '%5.4f'%ad[j]['d_rate_r'], '%5.4f'%ad[j]['d_rate_a'], '%5.4f'%ad[j]['rate_delta'], '%5.4f'%ad[j]['price'])
#             print(str(ad[j]['time'])+'%5.4f'%ad[j]['rate_r']+'%5.4f'%ad[j]['rate_a']+'%5.4f'%ad[j]['d_rate_r']+'%5.4f'%ad[j]['d_rate_a']+'%5.4f'%ad[j]['rate_delta']+'%5.4f'%ad[j]['price'])
        print('total trade times: ' + str(len(ad)))
        
    return

main()


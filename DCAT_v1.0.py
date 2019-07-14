'''
Created on Feb 22, 2018

@author: Pascal JING
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import xlwt
import xlrd
import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests
from math import pow
from xlutils.copy import copy

# For huobi_api_utils

# 髞溷価霎ｾ諡ｷ髞滓巳諡ｷ蜀僊PIKEY

ACCESS_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# API 髞滓巳諡ｷ髞滓巳諡ｷ髞溯｡暦ｿｽ
MARKET_URL = "https://api.huobi.pro"
TRADE_URL = "https://api.huobi.pro"
# MARKET_URL = "https://api.huobi.pro.com"
# TRADE_URL = "https://api.huobi.pro.com"
# 尽量用api.huobi.pro.com. by:奶总

# 髞滄亳霎ｾ諡ｷ髞滓巳諡ｷ髞溷将蛹｡諡ｷ騾夐函譁､諡ｷget_accounts()髞滓巳諡ｷ蜿紡cct_id,辟ｶ髞滓巳諡ｷ逶ｴ髞滓磁髱ｩ諡ｷ蛟ｼ,髞滓巳諡ｷ髞滓巳諡ｷ髞滓穐髱ｩ諡ｷ髞滓巳諡ｷ蜿夜函譁､諡ｷ
ACCOUNT_ID = 99999999

# For main

TRADE_FEE = (1 - 0.002)# * 0.25)
SLIP_RATE = 1#0.998

# For process

FILE_PATH = 'C:\\Users\\Pascal JING\\Desktop\\tradelog.xls'
# FILE_PATH = 'C:\\Users\\Administrator\\Desktop\\tradelog.xls'

#'Timestamp': '2017-06-02T06:13:49'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.FileHandler('tradelog.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)

    try:
        response = requests.get(url, postdata, headers=headers, timeout=100)

        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        #print("httpGet failed, detail is:%s,%s" %(response.text,e))
        print("httpGet failed, detail is:%s,%s" + str(e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)

    try:
        response = requests.post(url, postdata, headers=headers, timeout=100)
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        #print("httpPost failed, detail is:%s,%s" %(response.text,e))
        print("httpPost failed, detail is:%s,%s" + str(e))
        return


def api_key_get(params, request_path):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)

    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature

# ��ȡKLine
def get_kline(symbol, period, size):
    """
    :param symbol
    :param period: ��ѡֵ��{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size: ��ѡֵ�� [1,2000]
    :return:
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return http_get_request(url, params)


# ��ȡ  ֧�ֵĽ��׶�
def get_symbols(long_polling=None):
    """
    """
    params = {}
    if long_polling:
        params['long-polling'] = long_polling
    path = '/v1/common/symbols'
    return api_key_get(params, path)


def get_timestamp():
    params = {}
    path = '/v1/common/timestamp'
    return api_key_get(params, path)


def get_accounts():
    """
    :return: 
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)


# ��ȡ��ǰ�˻��ʲ�
def get_balance(acct_id=None):
    """
    :param acct_id
    :return:
    """

    if not acct_id:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id'];

    url = "/v1/account/accounts/{0}/balance".format(acct_id)
    params = {"account-id": acct_id}
    return api_key_get(params, url)


# ������ִ�ж���
def send_order(amount, source, symbol, _type, price=0):
    """
    :param amount: 
    :param source: ���ʹ�ý���ʲ����ף������µ��ӿ�,�������source����д'margin-api'
    :param symbol: 
    :param _type: ��ѡֵ {buy-market���м���, sell-market���м���, buy-limit���޼���, sell-limit���޼���}
    :param price: 
    :return: 
    """
    try:
        accounts = get_accounts()
        acct_id = accounts['data'][0]['id']
    except BaseException as e:
        print ('get acct_id error.%s' % e)
        acct_id = ACCOUNT_ID

    params = {"account-id": acct_id,
              "amount": amount,
              "symbol": symbol,
              "type": _type,
              "source": source}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)


# ��ѯĳ������
def order_info(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}".format(order_id)
    return api_key_get(params, url)


# ��ѯĳ�������ĳɽ���ϸ
def order_matchresults(order_id):
    """
    
    :param order_id: 
    :return: 
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(order_id)
    return api_key_get(params, url)


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


def _check_symbols(data):
    
    result = {}
    d_g_symbols = get_symbols()
    if d_g_symbols['status'] != 'ok':
        print('ERROR get symbols.')
        input('BREAK')
    else:
        d_symbols = d_g_symbols['data']
        for i in range(len(d_symbols)):
            for j in range(len(data)):
                
                if d_symbols[i]['base-currency'] == data[j][0] and d_symbols[i]['quote-currency'] == data[j][1]:
                    
                    result[data[j][0]] = d_symbols[i]['amount-precision']
                    result[data[j][1]] = d_symbols[i]['price-precision']
                    
    return result
# data = [['btc', 'usdt']]
# print(_check_symbols(data))
# {'btc': 2, 'usdt': 4}
# temp = 4.24523523
# print(round(temp,2))
# print(round(temp,4))


def _check_balance(data, method):
    result = {}
    d_g_balance = get_balance()
    if d_g_balance['status'] != 'ok' and d_g_balance['data']['state'] != 'working':
        print('ERROR get balance.')
        input('BREAK')
    else:
        d_balance = d_g_balance['data']['list']
        for i in range(len(d_balance)):
            for j in range(len(data)):
                
                if d_balance[i]['currency'] == data[j] and d_balance[i]['type'] == method:
                    
                    result[data[j]] = float(d_balance[i]['balance']) # Notice that it returns string.
                    
    return result 
# data = ['btc', 'usdt']
# method = 'trade'
# print(_check_balance(data, method))
# {'btc': '0.000121313823020400', 'usdt': '390.322503210000006998'}


def _check_order_info(id_order):
    result = []
    for i in range(len(id_order)):
        d_g_order_info = order_info(id_order[i])
        if d_g_order_info['status'] != 'ok':
            print('ERROR get order info.')
            input('BREAK')
        else:
            d_order = d_g_order_info['data']
            
            result.append(d_order)
            
    return result
# id_order = [1813664847, 1875241243]
# print(_check_order_info(id_order))
# [{'id': 1813664847, 'symbol': 'btcusdt', 'account-id': 913998, 'amount': '1.000000000000000000', 'price': '0.0', 'created-at': 1519526360003, 'type': 'buy-market', 'field-amount': '0.000103309413760400', 'field-cash-amount': '0.999999999999993464', 'field-fees': '0.000000206618827520', 'finished-at': 1519526360139, 'source': 'api', 'state': 'filled', 'canceled-at': 0}]


def _check_order_matchresults(id_order):
    result = []
    for i in range(len(id_order)):
        d_g_order_matchresults = order_matchresults(id_order[i])
        if d_g_order_matchresults['status'] != 'ok':
            print('ERROR get order match results.')
            input('BREAK')
        else:
            d_order = d_g_order_matchresults['data']
            
            result.append(d_order)
            
    return result
# id_order = [1813664847]
# print(_check_order_matchresults(id_order))
# [[{'id': 1029235468, 'order-id': 1813664847, 'match-id': 2977812687, 'symbol': 'btcusdt', 'type': 'buy-market', 'source': 'api', 'price': '9679.660000000000000000', 'filled-amount': '0.000103309413760400', 'filled-fees': '0.0', 'filled-points': '0.001999999999992244', 'created-at': 1519526360148}]]


def _check_if_refresh(F_first_startup, d_time):
    
    flag = False
    F_while = True
    warncode = {}
    while(F_while):
        n_time = get_kline('btcusdt', '1min', '1')
        if n_time:
            if n_time['status'] == 'ok':
                if n_time['data'] != []:
#             TypeError: 'NoneType' object is not subscriptable.
                    n_time = n_time['data'][0]['id']
#             break
                    F_while = False
                    
                else:
                    warncode = {'err-code': 'No data recieved', 'err-msg': 'while status ok'}
            else:
                warncode = {'err-code' :n_time['err-code'], 'err-msg': n_time['err-msg']}
        else:
            warncode = {'err-code': 'No data recieved', 'err-msg': 'while status null'}
            time.sleep(1)
            pass
        
    if n_time != d_time:
        if n_time > d_time:
            flag = True
        elif F_first_startup:
            pass
        else:
            warncode = 2
    return flag, n_time, warncode


def record(d_first, d_balance, d_calculate, d_order, d_record):
    
    F_ROOT_ABORT = False
    
    f_time = d_first['time']
    f_price = d_first['price']
    f_btc = d_first['btc']
    f_usdt = d_first['usdt']
    
    r_btc = d_balance['btc']
    r_usdt = d_balance['usdt']
    
    time = d_calculate[0]['time']
    i_price = d_calculate[0]['price']
    scale = d_calculate[0]['scale']
    
    temp = 0
    field_amount = 0
    for i in range(len(d_order)):
        temp = float(d_order[i]['price']) * float(d_order[i]['filled-amount'])
        field_amount += float(d_order[i]['filled-amount'])
    r_price = temp / field_amount
    slip_rate = (r_price / i_price - 1) * 100
    
    i_btc = d_record['i_btc']
    i_usdt = d_record['i_usdt']
    
    r_rate_absolute = (r_btc * r_price + r_usdt) / (f_btc * f_price + f_usdt) * 100
    r_rate_relative = r_rate_absolute * f_price / r_price
    
    direction = ''
    
    if scale > 0:
        i_btc += i_usdt / i_price * scale * TRADE_FEE * SLIP_RATE
        i_usdt -= i_usdt * scale
        direction = 'BUY'
    if scale < 0:
        scale = - scale
#         ERROR! NOTICE!
#         i_btc -= i_btc * scale
#         i_usdt += i_btc * scale * i_price * TRADE_FEE * SLIP_RATE
        i_usdt += i_btc * scale * i_price * TRADE_FEE * SLIP_RATE
        i_btc -= i_btc * scale
        direction = 'SELL'
    i_rate_absolute = (i_btc * i_price + i_usdt) / (f_btc * f_price + f_usdt) * 100
    i_rate_relative = i_rate_absolute * f_price / i_price
    
    import time as myTime
    time_now = myTime.time()
    time_local = myTime.localtime(time_now) 
    n_time = myTime.strftime("%Y-%m-%d %H:%M:%S", time_local)
    
    if r_rate_absolute < 95 and r_rate_relative < 95:
        F_ROOT_ABORT = True
    if r_rate_absolute < 80 or r_rate_relative < 80:
        F_ROOT_ABORT = True
        
    result = {'n_time': n_time,\
              'time': time,\
              'f_time': f_time,\
              'f_btc': f_btc,\
              'f_usdt': f_usdt,\
              'f_price': f_price,\
              'r_price': r_price,\
              'i_price': i_price,\
              'slip_rate': slip_rate,\
              'direction': direction,\
              'scale': scale,\
              'r_btc': r_btc,\
              'r_usdt': r_usdt,\
              'r_rate_r': r_rate_relative,\
              'r_rate_a': r_rate_absolute,\
              'i_btc': i_btc,\
              'i_usdt': i_usdt,\
              'i_rate_r': i_rate_relative,\
              'i_rate_a': i_rate_absolute,\
              'abort_flag': F_ROOT_ABORT } 
    
    return result


#     only used for btc/usdt trade now
def trade(d_balance, d_calculate):
    
    errorcode = {}
    infocode = {}
    
    flag = False
    id_order = 0
    
    account_btc = float(d_balance['btc'])
    account_usdt = float(d_balance['usdt'])
    
#     time = d_calculate[0]['time']
    price = d_calculate[0]['price']
    scale = d_calculate[0]['scale']
    
    precision = _check_symbols([['btc', 'usdt']])
    p_btc = precision['btc']
    p_usdt = precision['usdt']    
    
#     minimum trade amount calculate processing.
#     p_safe_params for the change of price during software running.
#     numbers include check done. 
    p_safe_params = 1.01
    
    if price * pow(0.1, p_btc) > pow(0.1, p_usdt):
        pmin_btc = pow(0.1, p_btc)
        pmin_usdt = round(price * pow(0.1, p_btc) * p_safe_params, p_usdt) + pow(0.1, p_usdt)
    else:
        pmin_btc = round(pow(0.1, p_usdt) / price / p_safe_params, p_btc) + pow(0.1, p_btc)
        pmin_usdt = pow(0.1, p_usdt)
    
#     core trade processing.
#     return order id and ideal trade result for further usage.
    if scale > 0:
#         buy btc
        trade_amount = round(account_usdt * scale - pow(0.1, p_usdt), p_usdt) 
        if trade_amount > pmin_usdt:
            
            r_order = send_order(trade_amount, 'api', 'btcusdt', 'buy-market') #buy check done.
#             '''
#             r_order = {'status': 'ok', 'data': 1}
# #             print('  ' +str(trade_amount))
#             '''
            if r_order['status'] == 'ok':

                flag = True
                id_order = r_order['data']
            else:
                errorcode = {'err-code' :r_order['err-code'], 'err-msg': r_order['err-msg']}
        else:
            infocode = {'info-code': 'Trade not done', 'info-msg': 'min account btc'}\
                           
    elif scale < 0:
#         sale btc
        scale = - scale
        trade_amount = round(account_btc * scale - pow(0.1, p_btc), p_btc) 
        if trade_amount > pmin_btc:
            
            r_order = send_order(trade_amount, 'api', 'btcusdt', 'sell-market') #sale check done.
#             '''
#             r_order = {'status': 'ok', 'data': 1}
# #             print('  ' +str(trade_amount))
#             '''
            if r_order['status'] == 'ok':
                              
                flag = True
                id_order = r_order['data']
            else:
                errorcode = {'err-code': r_order['err-code'], 'err-msg': r_order['err-msg']}
        else:
            infocode = {'info-code': 'Trade not done', 'info-msg': 'min account btc'}
                
    return flag, id_order, errorcode, infocode



def calculate(data, flag):
    
    scale = 0
    CAL_STEP_LEN = 500
    CAL_STEP_DELTA = 3
    
    p3 = []
    p4 = []
    p5 = []
    p6 = []
    p7 = []
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
        
        p8.append(mov_avg(d, 36, 1) - mov_avg(d, 216, 1)) 
        
        e = []
        for k in range(int(CAL_STEP_LEN / 2)):
            temp2 = d[k : k + int(CAL_STEP_LEN / 2) - 1]
#             need review , not accurate
            
            e.append(pow(mov_avg(temp2, 36, 1) - mov_avg(temp2, 216, 1), 2))
        
        p9.append(mov_avg(d, 216, 1) - 2 * pow(mov_avg(e, 216, 1), 0.5))
        p10.append(mov_avg(d, 216, 1) + 2 * pow(mov_avg(e, 216, 1), 0.5))
        
    scale_c = 0.8
    
    if p3[0] < p9[0] and p3[1] > p9[1]: flag['BOLL'] = 'BELLOW'
    if p3[0] > p10[0] and p3[1] < p10[1]: flag['BOLL'] = 'ABOVE'
    
    if p3[0] < p3[1] and p5[0] < p5[1] and p4[0] < p4[1] and p6[0] < p6[1]:
        if flag['BOLL'] == 'BELLOW':
            if p8[0] > p8[1] and p8[1] < p8[2]:
                scale = scale_c #buy
                flag['BOLL'] = 'DEFAULT'
        if p8[0] > 0:
            if p8[0] < p8[1] and p8[1] > p8[2]: 
                scale = - scale_c #sale
                
    if p3[0] > p3[1] and p5[0] > p5[1] and p4[0] > p4[1] and p6[0] > p6[1]:
        if flag['BOLL'] == 'ABOVE':
            if p8[0] < p8[1] and p8[1] > p8[2]:
                scale = - scale_c #sale
                flag['BOLL'] = 'DEFAULT'
        if p8[0] < 0:
            if p8[0] > p8[1] and p8[1] < p8[2]:
                scale = scale_c #buy
    
#     scale = -0.1
#     scale = 0.1
    
    result = {'time':data[0]['time'], 'price':data[0]['price'], 'scale':scale}
    
    return result, flag


def write_excel(F_first_startup, F_write_log, data):
    
    sheetname = 'tradelog'
    filename = FILE_PATH
    temp = ['n_time', 'time', 'r_price', 'i_price', 'slip_rate', 'direction', 'scale', 'r_btc', 'r_usdt', 'r_rate_r', 'i_rate_r', 'r_rate_a', 'i_rate_a']
    
    if F_first_startup:
        file = xlwt.Workbook()
        sheet = file.add_sheet(sheetname, cell_overwrite_ok = True)
        
        for j in range(len(temp)):
            sheet.write(0, j, temp[j])
        
        file.save(filename)
        
    if F_write_log:
        file = copy(xlrd.open_workbook(filename)) #Notice that it's necessary
        sheet = file.get_sheet(sheetname)

        for j in range(len(temp)):
            sheet.write(len(data) - 1 + 1, j, data[len(data) - 1][temp[j]])
                    
        file.save(filename)
    
    return


def trigger():
    
    d_time = 0
    
    F_while = True
    F_calculate = {'BOLL': 'DEFAULT'}#, 'DIRECTION': 'DEFAULT'}
    F_first_startup = True
    D_first = {}
    D_record = {}
    D_records = []
    
    logger.info('System start!')   
    
    while(F_while):
        check_result = _check_if_refresh(F_first_startup, d_time)
        if check_result[2]:
            logging.warn('API-kline check refresh unsatisfied.')
            logging.error(check_result[2]['err-code'] + '. ' + check_result[2]['err-msg'])

        if check_result[0] == False:
            time.sleep(1)
        else:
            d_time = check_result[1]
# main process            
            result_main = main(F_calculate, F_first_startup, D_first, D_record)
            
            D_first = result_main[2]
            
            if F_first_startup:
                D_record = result_main[3]
            if D_record != result_main[3]:
                D_record = result_main[3]
                D_records.append(D_record)
                
            F_write_log = result_main[4]

            write_excel(F_first_startup, F_write_log, D_records)
                
            if D_record['abort_flag']:
                F_while = False
                logger.error('Loss afford line passed. Aborting.') 
                input('BREAK.')
                        
            F_calculate = result_main[0]
            F_first_startup = result_main[1]
                
    return


def main(F_calculate, F_first_startup, d_first, d_record):
    
    F_write_log = False
    F_delaying = False
    
    F_while = True
    while(F_while):
        d_kline = get_kline('btcusdt', '1min', '521')
        if d_kline:
            if d_kline['status'] == 'ok':
                if d_kline['data'] != [] and len(d_kline['data']) == 521:
            
                    import time as myTime
                    time_now = int(myTime.time())
                    time_delay = time_now - d_kline['data'][0]['id']

                    d_kline = d_kline['data']
                    F_while = False
                    
                    if time_delay > 10 and not F_first_startup:
                        logging.warn('API-kline check data delaying.')
                        logging.warn('Delay ' + str(time_delay) + ' seconds now.')
                        F_delaying = True
                 
                else:
                    logging.warn('API-kline check data unsatisfied.')
                    logging.warn('Return length error. Need: 521. Actual: ' + str(len(d_kline['data'])))   
            else:
                logging.warn('API-kline check data unsatisfied.')
                logging.error(d_kline['err-code'] + '. ' + d_kline['err-msg'])    
        else:
            logging.warn('API-kline check data unsatisfied.')
            logging.warn('No data received.')
            pass
        
    d_main = []
    for i in range(len(d_kline)):
        d_main.append({'time': d_kline[i]['id'], 'price': d_kline[i]['open']})
    d_main.sort(key = lambda x:x['time'], reverse = True)

    if F_first_startup:
        d_balance = _check_balance(['btc', 'usdt'], 'trade')
        d_first = {'time': d_main[0]['time'], 'price': d_main[0]['price'], 'btc': d_balance['btc'], 'usdt': d_balance['usdt']}
        d_record = {'i_btc': d_balance['btc'], 'i_usdt': d_balance['usdt'], 'i_rate_relative': 100, 'i_rate_absolute': 100, 'abort_flag': False}
    
        logger.info(d_first)
# calculate        
    d_calculate = calculate(d_main, F_calculate)
    
    logger.info(str(d_calculate[0]['time'])+' '+\
                str(d_calculate[0]['price'])+' '+\
#                 str(d_calculate[1]['DIRECTION'])+' '+\
                str(d_calculate[1]['BOLL'])+' '+\
                str(d_calculate[0]['scale'])) 
        
    if d_calculate[0]['scale'] != 0 and not F_first_startup and not F_delaying:
# balance
        d_balance = _check_balance(['btc', 'usdt'], 'trade')
# trade        
        r_trade = trade(d_balance, d_calculate)
        
        if r_trade[2]:
            logging.error('API-trade status error!')
            logging.error(r_trade[2]['err-code'] + '. ' + r_trade[2]['err-msg'])
        
        if r_trade[3]:
            logging.error(r_trade[3]['info-code'] + '. ' + r_trade[3]['info-msg'])
        
        if r_trade[0]:
            
            logger.info(str('Trade success!'))
            
            id_order = [r_trade[1]]
            F_while = True
            while(F_while):
# check  
                if _check_order_info(id_order)[0]['state'] == 'filled':
                    d_order = _check_order_matchresults(id_order)[0]
                    d_balance = _check_balance(['btc', 'usdt'], 'trade')
# record                    
                    d_record = record(d_first, d_balance, d_calculate, d_order, d_record)
                    
                    F_write_log = True
                    F_while = False
                else:
                    logger.warn('API-trade unfinished order processing.')
                    time.sleep(10)
                    pass
#                 '''
#                 if id_order[0] == 1:
#                     d_order = [{'id': 1029235468, 'order-id': 1813664847, 'match-id': 2977812687, 'symbol': 'btcusdt', 'type': 'buy-market', 'source': 'api', 'price': '9679.660000000000000000', 'filled-amount': '0.000103309413760400', 'filled-fees': '0.0', 'filled-points': '0.001999999999992244', 'created-at': 1519526360148}]
#                     d_record = record(d_first, d_balance, d_calculate, d_order, d_record)
#                     F_write_log = True
#                     F_while = False
#                 '''
            logger.info(str(d_record))
            
    F_first_startup = False    
        
    return d_calculate[1], F_first_startup, d_first, d_record, F_write_log

        
trigger()


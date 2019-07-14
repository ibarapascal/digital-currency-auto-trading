'''
Created on Jan 31, 2018

@author: Pascal JING
'''

import urllib.parse
import requests
import logging
import time

from mongoengine import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
handler = logging.FileHandler('historydata.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


MARKET_URL = "https://api.huobi.pro"


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
        print("httpGet failed, detail is:%s,%s" %(response.text,e))
        return


def get_kline(symbol, period, size):
    """
    :symbol
    :period: {1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :size: [1,2000]
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
    
    
def process():
    
    MONGO_DB = 'DCAT_beta_historydata3'
    connect(MONGO_DB, host='localhost', port=27017)
    
    method = [btcusdt, bchusdt, ethusdt, etcusdt, ltcusdt, eosusdt, xrpusdt, htusdt]
    method_str = {btcusdt: 'btcusdt',\
                  bchusdt: 'bchusdt',\
                  ethusdt: 'ethusdt',\
                  etcusdt: 'etcusdt',\
                  ltcusdt: 'ltcusdt',\
                  eosusdt: 'eosusdt',\
                  xrpusdt: 'xrpusdt',\
                  htusdt:  'htusdt'}
    
    while(1):
        
        logging.info('Start data collection.')
        
        for i in range(len(method)):
            
            methodstep = method[i]
            
            F_while = True
            while(F_while):
                
                d_kline = get_kline(method_str[methodstep], '1min', '2000')
                
                if d_kline:
                    if d_kline['status'] == 'ok':
                        if d_kline['data'] != [] and len(d_kline['data']) == 2000:
                            
                            d_kline = d_kline['data']
                            F_while = False
                            
                        else:
                            logging.warn(method_str[methodstep] + ' check data unsatisfied.')
                            logging.warn('Return length error. Need: 2000. Actual: ' + str(len(d_kline['data'])))
                            time.sleep(10)     
                    else:
                        logging.warn(method_str[methodstep] + ' check data unsatisfied.')
                        logging.error(d_kline['err-code'] + '. ' + d_kline['err-msg'])
                        time.sleep(300)    
                else:
                    logging.warn(method_str[methodstep] + ' check data unsatisfied.')
                    logging.warn('No data received.')
                    time.sleep(300)
                
            
            num = len(d_kline)
            k = 0
            for i in range(1, num):
                j = num - i
                post = methodstep(
                    time = d_kline[j]['id'] ,
                    open = d_kline[j]['open'] ,
                    close = d_kline[j]['close'] ,
                    low = d_kline[j]['low'] ,
                    high = d_kline[j]['high'] ,
                    amount = d_kline[j]['amount'] ,
                    vol = d_kline[j]['vol'] ,
                    count = d_kline[j]['count']
                    )
                try:
                    post.save()
#                 print('Save ' + str(i) + '/' + str(num) + ' ' + str(d_kline[j]['id']))
                except:
                    pass
#                 k += 1
#                 print('Find ' + str(i) + '/' + str(num) + ' ' + str(d_kline[j]['id']))   
#             print('Jump ' + str(i + 1) + '/' + str(num) + ' ' + str(d_kline[j - 1]['id']))
#                 
#             print('\nSuccessful synchronous data from api.huobi.pro')
# 
#             if k == 0:
#                 print('\nAlert! Data discontinuous. Check DB to confirm.\n')
            logging.info(method_str[methodstep] + ' data synchronous done.') 
        
        logging.info('End of this time collection.')    
        time.sleep(3600)
    
    return

process()




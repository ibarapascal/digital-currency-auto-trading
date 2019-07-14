'''
Created on 2018/03/01

@author: Administrator
'''
import json
import urllib
import urllib.parse
import urllib.request
import requests
import re

URL = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E4%BA%BA%E6%B0%91%E5%B8%81&co=&resource_id=4278&t=1519864941631&cardId=4278&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110209215706583088863_1519864932323&_=1519864932325'
'''
GET /8aQDcjqpAAV3otqbppnN2DJv/api.php?query=1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E4%BA%BA%E6%B0%91%E5%B8%81&co=&resource_id=4278&t=1519864941631&cardId=4278&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110209215706583088863_1519864932323&_=1519864932325 HTTP/1.1
Host: sp0.baidu.com
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
Accept: */*
Referer: https://www.baidu.com/s?wd=%E7%BE%8E%E5%85%83%E6%B1%87%E7%8E%87&rsv_spt=1&rsv_iqid=0xef46477e00035529&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&oq=bat%2520%25E6%2596%2587%25E4%25BB%25B6%2520%25E8%25BF%2590%25E8%25A1%258C%25E5%25AE%258C%25E4%25B8%258D%25E8%2587%25AA%25E5%258A%25A8%25E5%2585%25B3%25E9%2597%25AD&rsv_t=69baPs0AYJDq82KxyzEzgtAqRfRjuTNMhNjMpSDvlAa8ZqwdkDTx3Y9fdnvssyRAf%2BGw&inputT=1951&rsv_pq=c2ad0c250003f65b&rsv_sug3=20&rsv_sug1=19&rsv_sug7=100&rsv_sug2=0&rsv_sug4=1952
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: BAIDUID=7EA11D0580BE1E0487170F94F4E5FC3C:FG=1; BIDUPSID=7EA11D0580BE1E0487170F94F4E5FC3C; PSTM=1508725829; H_PS_PSSID=1463_21097_20718; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; PSINO=2
'''

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

#         if response.status_code == 200:
#             return response.json()
#         else:
#             return

        print(response.text)
        print(response.text[42:len(response.text) -1])
        return response.json()
    
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" + str(e))
        return
    
def get_exchange_data():
    
#     params = {}
    params = {'query':'1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E4%BA%BA%E6%B0%91%E5%B8%81',
              'resource_id': '4278',
              't': '1519864941631',
              'cardId': '4278',
              'ie': 'utf8',
              'oe': 'gbk',
              'cb': 'op_aladdin_callback',
              'format': 'json',
              'tn': 'baidu',
              'cb': 'jQuery110209215706583088863_1519864932323',
              '_': '1519864932325'
              }
#     url = 'https://sp0.baidu.com' + '/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=1%E7%BE%8E%E5%85%83%E7%AD%89%E4%BA%8E%E5%A4%9A%E5%B0%91%E4%BA%BA%E6%B0%91%E5%B8%81&co=&resource_id=4278&t=1519864941631&cardId=4278&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110209215706583088863_1519864932323&_=1519864932325'
    url = 'https://sp0.baidu.com' + '/8aQDcjqpAAV3otqbppnN2DJv/api.php'
    
    return http_get_request(url, params)


print(get_exchange_data())


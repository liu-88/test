# -*-coding:utf-8-*-
# @FileName :requests_testt.py
# @Time     :2022-07-25 14:53
# @Author   :Digua
import json

import requests
import ddddocr
from common.get_tooken_image_guide import *
from hyper.contrib import HTTP20Adapter

def redirect(headers):
    headers_res = {}
    for h in headers:
        if(h[0:1] == ": "):
            single = h[1:].split(": ")
            headers_res[single[0]] = single[1]
            headers_res = dict(headers_res, **h)
        else:
            single = h.split(": ")
            if(len(single) != 1):
                if h == "\n":
                    continue
                else:
                    headers_res[single[0]] = single[1]
    return headers_res

rq = requests.session()
data = {"clientId":"erp-client","clientSecret":"","grantType":"password","password":"L6D5K6","userName":"pp"}
# rq.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"})
rq.get("https://beta-wms.zhican.com/child/wms/")
rp = rq.get("https://beta-wms.zhican.com/api/v1/users/captcha/img")
ocr = ddddocr.DdddOcr(old=True)
base64image = get_wms_image_base4(rp.json()["data"]["codeImgBase64"])
code = ocr.classification(base64image)
randomstr = rp.json()['data']['randomStr']
R_Headers = f'''User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'''
headers_1 = R_Headers.strip().split('\n')
headers_1 = redirect(headers_1)
# headers_1 = {"Content-type": "application/json;charset=UTF-8",
#              "randomStr": randomstr,"code":code,
#              "Accept": "application/json, text/plain, */*"}
# data = json.dumps(data)
# headers =  {
# "code": code,
# 'randomstr': randomstr,
# }
# rq.mount("https://beta-wms.zhican.com", HTTP20Adapter(headers_1))
temp_headers = {
"randomStr": randomstr,
"code": "1234"
}
rq.headers.update(headers_1)
# rq.mount("https://beta-wms.zhican.com/api/v1/users/auth/token", contrib.HTTP20Adapter())
rp2 = rq.post("https://beta-wms.zhican.com/api/v1/users/auth/token", json=data, headers=temp_headers)
print(rp2.json())
print(rq.headers,"登录信息头")
print(rp2.json())
jwt = rp2.json()["data"]["jwt"]
print(1)
# print(jwt)
data2 = {"pageSize":10,"pageIndex":1,"warehouseName":"","code":"","name":""}

headers_3 = """Client-id: erp-client
current-warehouse-id: 233
system-type: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"""
headers_4 = headers_3.strip().split('\n')
headers_5 = redirect(headers_4)
rq.headers.update(headers_5)
rq.headers.update(
    {
        "Authorization": jwt
    }
)

rp3 = rq.post("https://beta-wms.zhican.com/api/v1/warehouse/warehouseArea/list/page", json=data2)
print(rp3.json())
print(rq.headers)
# print(rq.headers)
# print(rp2.url)
# print(rp2.json())
# print(rq.headers)
# print(rp.headers)
# print(rp.text)

import os
import requests
import json
f = open("710033.log")
lines = f.readlines()
dic = {}
def findsku(line):
    lists = line.split("&")
    for tmp in lists:
        res = tmp.split("=")
        if res[0] == "sku":
            return res[1]

def findcid1(tmpres):
    pass
cou = 0
for line in lines:
    sku = findsku(line)
    url = "http://172.28.175.132:5080/api/dbproxy?method=get&db=iteminfo-detail&result=thrift&type=com.jd.si.clerk.SKUData&key=" + sku
    res = requests.get(url)
    res = res.json()
    try:
        cid1 = res["data"][0]["details"]["categoryLevel1"]
        dic[cid1] = dic.get(cid1, 0) + 1
    except:
        print(res)
    
for k,v in dic.items():
    print(k, v)

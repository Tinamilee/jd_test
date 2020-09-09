#coding=UTF-8
import json
import hashlib
import commands
import requests
import time
import sys
from optparse import OptionParser

def get_sign(str):
    my_md5 = hashlib.md5()
    my_md5.update(str)
    my_md5_Digest = my_md5.hexdigest()
    return my_md5_Digest

def get_response(url):
    APP_ID = "test"
    APP_SECRET = "eeadaa94-deaa-4b09-b01e-939d7db22da6"
    TIMESTAMP = str(int(time.time())*1000)
    ERP = "weizhenli2"
    SIGN = get_sign(APP_ID+TIMESTAMP+APP_SECRET)
    headers = {"Content-Type":"application/json","appId":APP_ID,"optErp":ERP,"timestamp":TIMESTAMP,"signature":SIGN}
    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        print e
    return res

def post_requests(url, data):
    APP_ID= "test"
    APP_SECRET= "eeadaa94-deaa-4b09-b01e-939d7db22da6"
    TIMESTAMP = str(int(time.time())*1000)
    ERP = "weizhenli2"
    SIGN = get_sign(APP_ID+TIMESTAMP+APP_SECRET)
    headers = {"Content-Type":"application/json","appId":APP_ID,"optErp":ERP,"timestamp":TIMESTAMP,"signature":SIGN}
    #print "type of data:", type(data)
    try:
        res = requests.put(url, data=data, headers=headers)
    except Exception as e:
        print e
    print "res:", res.content
 

def get_card_id(cardcode):
    url = "http://api-gateway.jd.com/jacp/api/rest/space/card/code/%s" % cardcode
    card_info = get_response(url).content
    #print"card_info:", card_info
    #print type(card_info)
    return card_info

def runcmd(cmd):
    try:
        ret, res = commands.getstatusoutput(cmd)
    except Exception, e:
        raise Exception('[ERROR]: run cmd failed "%s": %s' % (cmd, e))
    return ret, res

# 获取新commit的数据并返回
def findnewcommit():
    parser = OptionParser()
    parser.add_option('--git-dir', default='.git', help='the .git path of project')
    parser.add_option('-l', '--last', default='d8d8c668', help='last commit sha1.')
    parser.add_option('-n', '--new', default='5caa5f51', help='new commit sha1.')
    options, args = parser.parse_args()
    try:
        ret, res = runcmd('git --git-dir=%s log --no-merges --format=%%s %s..%s' % (options.git_dir, options.last, options.new))
        # print ret, res
        return ret, res
    except Exception, e:
        print e

def changestatus(cardid, spaceid):
    url = "http://api-gateway.jd.com/jacp/api/rest/space/%s/card/%s/status" % (spaceid, cardid)
    data = {"id":cardid, "statusId":7, "spaceId":spaceid, "cardId":cardid}
    #data = {"statusId":7}
    data_json = json.dumps(data)
    #print "type of cardid:", type(cardid)
    try:
        res = post_requests(url, data_json)
    except Exception as e:
        print e

if __name__ == '__main__':
    #  1.1获取不同版本中，新提交的信息
    ret, cardcodes = findnewcommit() 
    ccs = cardcodes.split("\n")
    cardcodeslist = []
    # 2 处理返回数据格式，获得C开头的cardcode
    for ca in ccs:
        if "#" in ca:
            tmp = ca.split("#")
            cardcodeslist.append(tmp[1])
    #print "cardcodelist:", cardcodeslist
    cou = 0
    for cc in cardcodeslist:
        print "cc every cardcode: ", cc
        # 3 根据cardcode 获得card id
        card_info = get_card_id(cc)
        print "card_info:", card_info
        #card_dic = eval(card_info)
        # 3.1 字符串解析为字典格式
        card_dic = json.loads(card_info)
        if card_dic["message"] != "SUCCESS":
            continue
        print "card_dic:", card_dic
        data_dic = card_dic["data"]
        #print data_dic["id"], data_dic["spaceId"]
        # 3.2 字典格式获取cardid和spaceid
        cardid = data_dic["id"]
        spaceid = data_dic["spaceId"]
        # 4 更改状态
        changestatus(cardid, spaceid)
        cou += 1
        #changestatus(569497, 3574)
    print "change %s card status , and total is %s" % (cou, len(cardcodeslist))

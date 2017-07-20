#!/usr/bin/env python
# coding=utf-8
# python version:2.7.4
# system:windows xp
import re,urllib,random
import json,datetime
import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def yhq_str_parse(data):
    '''
    对用户群列表字符串进行解析获取用户群name列表
    :param data: table列表字符串
    :return: array
    '''
    ww = re.split("\n", data)
    array = []
    for item in ww:
        array.append(re.split(' ', item)[-1])
    return array

def http_request(url, req):
    req = urllib.urlencode(req)
    request = urllib2.Request(url, req)
    response = urllib2.urlopen(request)
    result = response.read()
    json_data = json.loads(result)
    return json_data

def delay_several_day(several):
    date = datetime.datetime.now() + datetime.timedelta(days= several)
    return date.strftime('%Y-%m-%d %H:%M:%S')

def login(ip_port):
    login_path = ip_port + "/api/web/permission/login"
    req = {"username":"admin","password":"123456"}
    rsp =http_request(login_path, req)
    return rsp

def get_userTemplate(token,ip_port):
    '''
    获取用户设置模板默认一个
    :param token: 登录token
    :param ip_port: http://ip:port
    :return: 返回报文
    '''
    userTemplate_path = ip_port + "/api/userTemplate/getListData"
    req = {"currPage": 1,"pageSize": 3,"token":token}
    rsp = http_request(userTemplate_path, req)
    return rsp

def add_preset_msg(ip_port, type):
    '''
    添加预设用户推送
    :param ip_port: http://ip:port
    :param type: 推送类型jpush sms sys
    :return: 返回报文
    '''
    preset_path = ip_port + "/api/messageTask/insertPreSetMesTask"
    log = login(ip_port)
    template = get_userTemplate(log["data"]["token"],ip_port)
    jump_url = ''
    if type == 'jpush':
        jump_url = "http://baidu.com"
    req = {"token": log["data"]["token"],
            "messageDesc": "autopre" + str(random.randint(1000,999999)),
            "userTemplateId": template["data"]["resultList"][0]["id"],
            "userTemplateName": template["data"]["resultList"][0]["templateName"],
            "pushType": type,
            "jumpUrl": jump_url,
            "sendTimeStart": delay_several_day(1),
            "sendTimeEnd": delay_several_day(3),
            "messageTempNid": 'succLoanInviteSms',
            "userReferPercent": '',
          }
    rsp = http_request(preset_path, req)
    return rsp


def save_taskData(service,type):
    '''
    保存实时推送；
    :param service: http://ip:port
    :param type: 推送方式
    :return: 
    '''
    log = login(service)
    template = get_userTemplate(log["data"]["token"], service)
    jump_url = ''
    if type == 'jpush':
        jump_url = "http://baidu.com"
    url = service + "/api/messageInfo/saveTaskData"
    req = {"token": log["data"]["token"],
            "messageDesc": "autoreal" + str(random.randint(1000,9999)),
            "userTemplateId": template["data"]["resultList"][1]["id"],
            "pushType": type,
            "jumpUrl": jump_url,
            "sendTimeStart": delay_several_day(1),
            "sendTimeEnd": delay_several_day(3),
            "messageTempNid": 'succLoanInviteSms',
         }
    rsp = http_request(url, req)
    return rsp

def upload_file(service,file_path):
    '''
    文件上传；
    :param service: 服务ip和port
    :param path: 文件路径
    :return: 接口返回报文
    '''
    url = service + "/api/messageTask/uploadFile"
    body_value = {"fileType": "xlsx",
                  "file": open(file_path, 'rb'),
    }
    rsp = request_with_file(url, body_value)
    return rsp['data']

def insert_import_list(service,type,file_path='../../resource/autotest.xlsx'):
    '''
    名单导入推送（jpush,sms,sys）;
    :param service: http://ip:port
    :param type: 推送方式
    :return: 
    '''
    fr = upload_file(service,file_path)
    log = login(service)
    template = get_userTemplate(log["data"]["token"], service)
    jump_url = ''
    if type == 'jpush':
        jump_url = "http://www.sina.com"
    url = service + "/api/messageTask/insertImportListMesTask"
    req = {"uploadFileName": fr['fileName'],
           "uploadFileId": fr['id'],
           "token": log["data"]["token"],
           "messageDesc": "autoins" + str(random.randint(1000, 9999)),
           "userTemplateId": template["data"]["resultList"][1]["id"],
           "pushType": type,
           "jumpUrl": jump_url,
           "sendTimeStart": delay_several_day(1),
           "sendTimeEnd": delay_several_day(3),
           "messageTempNid": 'succLoanInviteSms',
           "userReferPercent": 10,
           }
    rsp = request_with_file(url, req)
    return rsp

def request_with_file(url, req):
    register_openers()
    datagen, re_headers = multipart_encode(req)
    request = urllib2.Request(url, datagen, re_headers)
    # 如果有请求头数据，则添加请求头
    result = urllib2.urlopen(request).read()
    json_data = json.loads(result)
    return json_data


# insert_import_list('http://192.168.1.93:8082', 'sms',"F:\\autotest_project\\ruby_data\\llbxInterface\\autotest.xlsx")
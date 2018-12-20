# coding=utf-8
import os,sys
import requests,json

# fir 参数
type = 'android'
url = 'http://api.fir.im/apps'
api_token = '2f50dde233766cd8be05f9cdf8312fa9'

# global fir 信息
iconDict = ''
binaryDict = ''

# 获取应用信息
def get_fir_apps(type,bundle_id,api_token):
    print('---开始获取应用信息---')
    try:
        params = {'type': type, 'bundle_id': bundle_id, 'api_token': api_token}
        resp = requests.post(url, data = params)
        json = resp.json()
        if resp.ok:
            global iconDict
            global binaryDict
            iconDict = json['cert']['icon']
            binaryDict = json['cert']['binary']
            print("---应用信息获取成功---")
            return True
        else:
            print("---应用信息获取失败---")
            print(json)
            return False
    except:
        print('Exception:',sys.exc_info())


# 上传应用图片
def upload_icon(upload_url,key,token,icon_path):
    print('---开始上传应用图片---')
    try:
        files = {'file' : open(icon_path,'rb')}
        params = {
            'key': key,                      # 'key'
            'token': token                   # 'token'
        }
        resp = requests.post(upload_url, data = params,files = files )
        json = resp.json()
        if resp.ok:
            print('---上传应用图片成功---')
        else:
            print('---开始上传应用失败---')
            print(json)
    except:
         print('Exception:',sys.exc_info())


# 上传应用apk
def upload_apk(upload_url,key,token,app_name,version_name,version_code,apk_path,change_log):
    print('---开始上传应用apk---')
    try:
        files = {'file' : open(apk_path,'rb')}
        params = {
            'key': key,                      # 'key'
            'token': token,                  # 'token'
            'x:name' : app_name,             # 'App的name'
            'x:version' : version_name,      # '1.0.0'
            'x:build' : version_code,        # '100'
            'x:changelog' : change_log       # '更新日志'
        }
        resp = requests.post(upload_url, data = params,files = files )
        json = resp.json()
        if resp.ok:
            print('---上传应用apk成功---')
        else:
            print('---上传应用apk失败---')
            print(json)
    except:
         print('Exception:',sys.exc_info())

# 获取参数，顺序执行上传至Fir任务
def start_fir_upload():
    try:
        app_name     = sys.argv[1]
        bundle_id    = sys.argv[2]
        version_name = sys.argv[3]
        version_code = sys.argv[4]
        icon_path    = sys.argv[5]
        apk_path     = sys.argv[6]
        change_log   = sys.argv[7]

        ret = get_fir_apps(type,bundle_id,api_token)
        if ret:
            upload_icon(iconDict['upload_url'],iconDict['key'],iconDict['token'],icon_path)
            upload_apk(binaryDict['upload_url'],binaryDict['key'],binaryDict['token'],app_name,version_name,version_code,apk_path,change_log)
        else:
            print ret
    except:
         print('Exception:',sys.exc_info())

start_fir_upload()
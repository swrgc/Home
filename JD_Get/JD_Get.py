# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:21:44 2020

@author: swrgc
"""

#京东商品价格监控

#iPhone


import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from fake_useragent import UserAgent

def GetMiddleStr(content,startStr,endStr):#取中间字段
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    if len(endStr)>0:
        endIndex = content[startIndex:].index(endStr)+startIndex
        return content[startIndex:endIndex]
    else:
        return content[startIndex:]

def get_name(sid):#获取sku-id的商品名称
    url =  'https://item.jd.com/{}.html'.format(sid)
    response = requests.get(url,stream=True)
#    response.encoding = 'utf8'
#    if response.status_code == 200:
    content = BeautifulSoup(response.text,'html.parser')
    if str(content.select('div[class="sku-name"]')) != '[]':
        sku_name = GetMiddleStr(str(content.select('div[class="sku-name"]')),'sku-name">','</div>').strip()
    else:
        sku_name = ''
    if '"/>' in sku_name:
        sku_name = GetMiddleStr(sku_name,'"/>','').strip()
    sku_name = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]|\\<.*?>", "", sku_name).strip()
    return sku_name
    

def get_price(sid):#获取sku_id的价格
    url = 'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(sid)
    response = requests.get(url,stream=True)
    content = response.text
    sku_price = re.findall(r'"p":"(.*?)"',content)
    return sku_price

def get_serach_list(skus):#基于商品名称获取搜索网页链接
    url_list = []
    for sku in skus:
        url_list.append('https://search.jd.com/Search?keyword={}&enc=utf-8&wq={}&pvid=ab331ca4b13a487bbf4621aa7dde78e2'.format(sku,sku))
    return url_list

def get_sku_id(serach_list):#基于搜索网页获取所有sku_id
    id_list = []
    headers = {'User-Agent':str(UserAgent().random)}
    for url in serach_list:
        response = requests.get(url,headers = headers,stream=True)
        response.encoding = 'utf8'
        content = BeautifulSoup(response.text,'html.parser')
        li_all =content.find_all('li',class_= "gl-item")
        for i in li_all:
            sid = GetMiddleStr(i.a['href'],'//','')
            sid = GetMiddleStr(sid,'/','.html')
            id_list.append(sid)
    return id_list

def get_sku_list(id_list):#获取最新价格
    result = pd.DataFrame(columns = ['sid','name','price','time'])
    time = str(datetime.datetime.now())[:16]
    for sid in id_list:
        print(sid)
        name = get_name(sid)
        print(name)
        price = float(get_price(sid)[0])
        print(price)
        row = result.shape[0]
        result.loc[row] = [sid,name,price,time]
    return result

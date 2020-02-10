# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 04:00:10 2020

@author: swrgc
"""

import pandas as pd
import JD_Get as JD_Get
from python_email import send_email
import numpy as np
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

#设置商品关键词
skus = ['YSL','Tom Ford','香奈儿','阿玛尼','索尼笔记本','SK-II','兰蔻','电饭煲','realme手机']

serach_list = JD_Get.get_serach_list(skus)

id_list = JD_Get.get_sku_id(serach_list)

while True:
    try:
        price_list
    except NameError:
        price_list = pd.DataFrame(columns = ['name','id','price','time'])
    
    headers= {'User-Agent':str(UserAgent().random)}

    new_price_list = JD_Get.get_sku_list(id_list)

    price_list = pd.concat([price_list,new_price_list])
    
    summary = pd.pivot_table(price_list,values = 'price',index = ['id'],columns = 'time',aggfunc = np.max)
    
    test = pd.merge(summary.iloc[:,[-1]],pd.DataFrame(summary.mean(axis = 1)),left_index = True,right_index = True)
    test['discount'] = 1-test.iloc[:,-2]/test.iloc[:,-2]
    albert = [test.index[i] for i in range(0,len(test.index)) if test['discount'][1]>=0.2]#上报7折以下商品
    for sku_id in albert:
    #    print(sku_id)
        name = price_list[price_list['id'] == sku_id]['name'].iloc[0]
        new_price = test[0][sku_id]
        old_price = test.iloc[:,[0]].loc[sku_id].values[0]
        text = '发现商品大降价，\n商品名称:{}，\n价格从原来的{}下降到了{}，\n链接是\nhttps://item.jd.com/{}.html。'.format(name,new_price,old_price,sku_id)
        print(text)
        send_email(text,'747608403@qq.com')
    send_email('1号跟踪了一遍','747608403@qq.com')
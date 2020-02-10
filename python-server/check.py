# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 00:08:04 2020

@author: Administrator
"""


from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import re
#准备数据库
JD_database = dict({'database':'JD_Price',
                    'user':'postgres',
                    'password':'SMALLwhite5875',
                    'host':'127.0.0.1',
                    'port':"5432"})

connDB = JD_database
engine = create_engine('postgresql+psycopg2://' + 
                       connDB['user'] + ':' + 
                       connDB['password'] + '@' + 
                       connDB['host'] + ':' + 
                       str(connDB['port']) + '/' + 
                       connDB['database'])


table = 'jd_price_2'
#读入原始数据
query_sql = "select * from {}".format(table)
df = pd.read_sql(query_sql,engine)

summary = pd.pivot_table(df,values = 'price',index = ['name'],columns = 'time',aggfunc = np.max)
summary2 = pd.pivot_table(df,values = 'price',index = ['sid'],columns = 'time',aggfunc = np.max)

r = []
for x in summary.index:
    print(x)
    y = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]|\\<.*?>", "", x)
    r.append(y.strip())

print(r[10])

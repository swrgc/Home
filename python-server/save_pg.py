# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 20:51:27 2020

@author: Administrator
"""

import psycopg2
from sqlalchemy import create_engine
import pandas as pd

JD_database = dict({'database':'JD_Price',
                    'user':'postgres',
                    'password':'SMALLwhite5875',
                    'host':'127.0.0.1',
                    'port':"5432"})

connDB = JD_database
conn = psycopg2.connect(database = connDB['database'],
                        user = connDB['user'],
                        password = connDB['password'],
                        host = connDB['host'],
                        port = connDB['port'])

engine = create_engine('postgresql+psycopg2://' + 
                       connDB['user'] + ':' + 
                       connDB['password'] + '@' + 
                       connDB['host'] + ':' + 
                       str(connDB['port']) + '/' + 
                       connDB['database'])


table = 'jd_price_1'
query_sql = "select * from {}".format(table)

df = pd.read_sql(query_sql,engine) # 配合pandas的方法读取数据库值

df.to_sql(table, engine, if_exists='append', index=False) 

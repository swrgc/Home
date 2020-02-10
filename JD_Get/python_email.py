# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 23:51:03 2020

@author: swrgc
"""

from email.mime.text import MIMEText
import smtplib


text = 'nihao,woshi zitong fasong'

def send_email(text,to,subject = '京东价格监测'):
    
    msg = MIMEText(text)
    
    msg['Subject'] = subject

    msg['From'] ='价格捕捉'

    msg['To'] = '快点买'#收件人名称

    from_address = '747608403@qq.com'
    pwd = 'jjkqjcrgvyssbcdj'#smtp password

    smtp_server = 'smtp.qq.com'

    to_address = [to]#地址

    try:
        server = smtplib.SMTP(smtp_server,587,timeout =5)

        server.login(from_address,pwd)

        server.sendmail(from_address,to_address,msg.as_string())
        server.quit()
        print('success')

    except Exception as e:
        print('failed! reason:{}'.format(e))





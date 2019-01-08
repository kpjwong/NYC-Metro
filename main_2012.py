# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 00:28:02 2018

@author: jerem
"""

import pandas as pd

def parser(txtfile):
    raw_data = open(txtfile,'r')
    CA_list, UNIT_list, SCP_list, DATE_list, TIME_list, DES_list, ENTRIES_list, EXITS_list = [], [], [], [], [], [], [], []
    for row in raw_data:
        L = row.split(',')
        try:
            CA_list.append(L.pop(0))
            UNIT_list.append(L.pop(0))
            SCP_list.append(L.pop(0))
            DATE_list.append(L.pop(0))
            TIME_list.append(L.pop(0))
            DES_list.append(L.pop(0))
            ENTRIES_list.append(L.pop(0))
            EXITS_list.append(L.pop(0))
        except:
            continue
    data = pd.DataFrame({'CA': CA_list, 
                         'UNIT': UNIT_list, 
                         'SCP': SCP_list, 
                         'DATE': DATE_list, 
                         'TIME': TIME_list,
                         'DES': DES_list,
                         'ENTRIES': ENTRIES_list,
                         'EXITS': EXITS_list})
    return data


data = parser('turnstile_120526.txt')
data = data[data.DATE >= '05-31-2012']
data = data.append(
       parser('turnstile_120602.txt')).append(
       parser('turnstile_120609.txt')).append(
       parser('turnstile_120616.txt')).append(
       parser('turnstile_120623.txt')).append(
       parser('turnstile_120630.txt'))
data = data[data.DATE <= '06-30-2012']

data = data.sort_values(by=['CA','UNIT','SCP','DATE','TIME'])
data.to_csv('turnstile_2012.csv')
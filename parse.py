# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 16:24:10 2018

@author: jerem
"""

import pandas as pd

raw_data = pd.read_csv("mta_2016.csv", sep=",")
date_list = []
ca_list = []
unit_list = []
t_list = []
z_list = []
entry_list = []
exit_list = []

est_dates = ['06/03/2016', '06/06/2016', '06/26/2016', '06/27/2016']
for idx, row in raw_data.iterrows():
    if not pd.isna(row['date']) and row['date'] in est_dates and not pd.isna(row['hour_diff']):
        print(idx)
        N = 6*int(row['hour_diff'])
        t = 6*row['hour']+1
        i = 0
        while i < N:
            date_list.append(row['date'])
            ca_list.append(row['ca'])
            unit_list.append(row['unit'])
            t_list.append(t)
            z_list.append(row['pickup_zone_gid'])
            entry_list.append(row['station_entry_ph']/6)
            exit_list.append(row['station_exit_ph']/6)
            t = t + 1 - 144*(t+1>144)
            i += 1

data = pd.DataFrame({'date': date_list,
                     'ca': ca_list,
                     'unit': unit_list,
                     't': t_list,
                     'zone_gid': z_list,
                     'entry': entry_list,
                     'exit': exit_list})
    
data.to_csv('2016_est_mta_data.csv')    
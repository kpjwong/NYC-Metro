# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 18:43:46 2018

@author: jerem
"""

import pandas
import functools
# get walking time to MTA
def get_walking_time(i):
    walking_t_list = []
    for j in range(i+1,262):
        data = globals()['result_'+str(i)+'_'+str(j)]
        if data:
            trip = data[0].get('legs')[0]
            walking_t, do_flag = 0, True
            for step in trip.get('steps'):
                if do_flag:
                    if step.get('travel_mode')=='WALKING':
                        walking_t += step.get('duration').get('value')/60
                    elif step.get('travel_mode')=='TRANSIT':
                        do_flag = False
            walking_t_list.append(walking_t)
            del data
    return functools.reduce(lambda x, y: x+y, walking_t_list)/len(walking_t_list) if walking_t_list else float('nan')


i_list, z_list, t_list = [], [], []
for i in range(1,262):
    i_list.append(i)
    z_list.append(zone[i])
    t_list.append(get_walking_time(i))

df = pandas.DataFrame({'zone_ID':i_list,
                       'zone':z_list,
                       'walking_time':t_list})
    
df.to_csv('walking_time.csv')
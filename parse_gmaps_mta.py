# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 09:09:24 2018

@author: jerem
"""

import pandas
zone = pandas.read_csv('zones.csv').zone

def parse(i,j):
    if i < j:
        data = globals()['result_'+str(i)+'_'+str(j)]
        if data:
            trip = data[0].get('legs')[0]
            trip_t = trip.get('duration').get('value')/60
            walking_t, transit_t = 0, 0
            for step in trip.get('steps'):
                if step.get('travel_mode')=='WALKING':
                    walking_t += step.get('duration').get('value')/60
                elif step.get('travel_mode')=='TRANSIT':
                    transit_t += step.get('duration').get('value')/60
            del data
            return trip_t, walking_t, transit_t
        else:
            return float('nan'), float('nan'), float('nan')
    elif i > j:
        return parse(j,i)
    

i_list, j_list, trip_t_list, transit_t_list, walking_t_list = [], [], [], [], []
for i in range(1,262):
    for j in range(1,262):
        if i != j:
            i_list.append(i+1)
            j_list.append(j+1)
            trip_t, transit_t, walking_t = parse(i,j)
            trip_t_list.append(trip_t)
            transit_t_list.append(transit_t)
            walking_t_list.append(walking_t)

DATA = pandas.DataFrame({'origin': i_list, 
                         'destination': j_list, 
                         'trip duration': trip_t_list, 
                         'transit duration': transit_t_list, 
                         'walking duration': walking_t_list})

DATA.to_csv('zone_travel_time.csv')
'''
import json, urllib
from urllib.parse import urlencode

start = "Chrysler Building, Manhattan"
finish = "Barclay Center, Brooklyn"

url = 'https://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
            ('origin', start),
            ('destination', finish),
            ('key', 'AIzaSyBcwp9sgR6vgXwk5Qx6QyKvfwX0qOiFqhk'),
            ('mode', 'transit')
 ))

i = 0
ur = urllib.request.urlopen(url)
result = json.load(ur)


transit_route_data=result.get('routes')[0].get('legs')[0]
trip_time = transit_route_data.get('duration').get('value')/60
walking_time, transit_time = 0, 0
for step in transit_route_data.get('steps'):
    if step.get('travel_mode')=='WALKING':
        walking_time += step.get('duration').get('value')/60
    elif step.get('travel_mode')=='TRANSIT':
        transit_time += step.get('duration').get('value')/60
waiting_time = trip_time-walking_time-transit_time
'''
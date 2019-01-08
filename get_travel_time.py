# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 18:29:35 2018

@author: jerem
"""

from datetime import datetime
import googlemaps
import pandas
import time as t
import numpy as np

zone = pandas.read_csv('zones.csv').zone
time = datetime(2018,9,4,9,0,0)
API_key = 'AIzaSyBcwp9sgR6vgXwk5Qx6QyKvfwX0qOiFqhk'
gmaps = googlemaps.Client(key=API_key)

col_26 = np.zeros([263,1])
col_156 = np.zeros([263,1])
i = 24
for j in range(262):
    result = gmaps.directions(zone[24], zone[j], mode="transit", departure_time=time)
    if result:
        steps = result[0]['legs'][0]['steps']
        transit_time = 0
        for step in steps:
            if step['travel_mode']=='TRANSIT':
                transit_time += step['duration']['value']/60
        col_26[j+1] = transit_time
        print('1:', j)
    result2 = gmaps.directions(zone[154], zone[j], mode="transit", departure_time=time) 
    if result2:
        steps2 = result2[0]['legs'][0]['steps']
        transit_time2 = 0
        for step2 in steps2:
            if step2['travel_mode']=='TRANSIT':
                transit_time2 += step2['duration']['value']/60
        col_156[j+1] = transit_time2
        print('2:', j)
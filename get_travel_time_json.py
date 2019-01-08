# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 20:36:38 2018

@author: jerem
"""

import json, urllib
import numpy as np
from urllib.parse import urlencode
import pandas
zone = pandas.read_csv('zones.csv').zone
for i in range(len(zone)):
    zone[i] = zone[i].replace(', ',',').replace(' ','+')

row_list = []
bad_list = []
dist_mat = np.zeros([263,263])
for i in range(262):
    start = zone[i]
    for j in range(i+1,262):
        finish = zone[j]
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?%s' % urlencode((
             ('origins', start.replace(' ','+')),
             ('destinations', finish.replace(' ','+')),
             ('key', 'AIzaSyBcwp9sgR6vgXwk5Qx6QyKvfwX0qOiFqhk'),
             ('mode', 'drive')))
        ur = urllib.request.urlopen(url)
        try:
            result = json.load(ur)
            dist = result['rows'][0]['elements'][0]['distance']['value']/1609.344
            row_list.append((i+1,j+1,dist))
            dist_mat[i+1][j+1] = dist
            dist_mat[j+1][i+1] = dist
            print(i+1,j+1,'done: dist =',dist)
        except:
            bad_list.append((i,j))
            print(i+1,j+1,'bad')
        
'''
for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
    j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
    print(j)
'''
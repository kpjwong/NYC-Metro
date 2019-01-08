# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

data = pd.read_csv("turnstile_160604.txt", sep=",")
data = data[data.DATE >= '05/31/2016']
data = data.append(
       pd.read_csv("turnstile_160611.txt", sep=",")).append(
       pd.read_csv("turnstile_160618.txt", sep=",")).append(
       pd.read_csv("turnstile_160625.txt", sep=","))
data2 = pd.read_csv("turnstile_160702.txt", sep=",")
data2 = data2[data2.DATE <= '06/30/2016']
data = data.append(data2)
del data2

data = data.sort_values(by=['STATION','SCP','DATE','TIME'])
data.to_csv('turnstile.csv')
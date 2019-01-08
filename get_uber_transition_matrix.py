# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 23:00:25 2018

Transition of MTA passengers:
let z1, z2 be TLC taxi zones
let zz1, zz2 be model zones
let b1, b1 be boros
let t \in {0,1,2} be peaks
let P^M, P^T be transition estimated from MTA and Taxis

If b1 = b2 = Manhattan:
P^M(z1,z2|t) = P^M(b1,b2|t)*P^M(zz1,zz2)*P^T(z1,z2|zz1,zz2,t)
(=PM_BBt*PM_zzzz_MM*PT_zz_zzzzt)

Format: PT_zz_zzzzt = PT_zz{t}
call: PT(z1,z2|zz1,zz2,t) = PT_zz_zzzzt[(zz1,zz2,t)]

Else:
P^M(z1,z2|t) = P^M(b1,b2|t)*P^M(z2|b1)
(=PM_BBt*PM_zB)


"""
import numpy as np
import pandas as pd
data_2013 = pd.read_csv('D:\\Data\\june_2013.csv')
data_2016 = pd.read_csv('D:\\Data\\june_2016.csv')

tr_2013 = pd.crosstab(data_2013.pickup_zone_gid, data_2013.dropoff_zone_gid)
tr_2016 = pd.crosstab(data_2016.pickup_zone_gid, data_2016.dropoff_zone_gid)

tr_2013 = tr_2013.div(tr_2013.sum(axis=1),axis=0)
tr_2016 = tr_2016.div(tr_2016.sum(axis=1),axis=0)

mta_2008 = pd.read_csv('mta_trips_2008_cleaned.csv')
PM_BB = {}
for t in range(3):
    PM_BB[t] = pd.crosstab(mta_2008.loc[mta_2008.peak==t].o_boro, mta_2008.loc[mta_2008.peak==t].d_boro)
    PM_BB[t] = PM_BB[t].div(PM_BB[t].sum(axis=1),axis=0)

PM_zzzz_MM = pd.crosstab(mta_2008.loc[(mta_2008.o_boro=='Manhattan') & (mta_2008.d_boro=='Manhattan')].o_zz, mta_2008.loc[(mta_2008.o_boro=='Manhattan') & (mta_2008.d_boro=='Manhattan')].d_zz)
PM_zzzz_MM = PM_zzzz_MM.div(PM_zzzz_MM.sum(axis=1),axis=0)

M_subdata = data_2013.loc[(data_2013.pickup_boro=="Manhattan") & (data_2013.dropoff_boro=="Manhattan")]
PT_zz_zzzzt = {}
for h in range(24):
    M_subdata_h = M_subdata.loc[(data_2013.pickup_t-1)//6==h]
    for zz1 in range(1,20):
        subdata_zz = M_subdata_h.loc[data_2013.pickup_zz==zz1]
        for zz2 in range(1,20):
            print(zz1,zz2,h)
            subdata = subdata_zz.loc[data_2013.dropoff_zz==zz2]
            PT_zz_zzzzt[(zz1,zz2,h)] = pd.crosstab(subdata.pickup_zone_gid, subdata.dropoff_zone_gid)
            PT_zz_zzzzt[(zz1,zz2,h)] = PT_zz_zzzzt[(zz1,zz2,h)].div(PT_zz_zzzzt[(zz1,zz2,h)].sum(axis=1),axis=0)

PM_zB = pd.crosstab(mta_2008.d_boro, mta_2008.d_zone_gid)
PM_zB = PM_zB.div(PM_zB.sum(axis=1), axis=0)




taxi_zones = pd.read_csv('taxi_zones.csv')
PM = np.zeros([263,263,144])
peak_t_dict = {}
for h in range(24):
    if h >= 6 and h <= 11:
        peak_t_dict[h] = 1
    elif h >= 16 and h <= 19:
        peak_t_dict[h] = 2
    else:
        peak_t_dict[h] = 0

PM = np.zeros([263,263,24])
for h in range(24):
    t_peak = peak_t_dict[h]
    for z1_idx in range(262):
        z1 = z1_idx + 1
        zz1 =  taxi_zones.zz[z1_idx]
        b1 = taxi_zones.boro[z1_idx]
        for z2_idx in range(262):
            print(z1_idx,z2_idx,h)
            z2 = z2_idx + 1
            zz2 = taxi_zones.zz[z2_idx]
            b2 = taxi_zones.boro[z2_idx]
            if b1=='Manhattan' and b2=='Manhattan':
                try:
                    PM[z1][z2][h] = PM_BB[t_peak][b2][b1]*\
                                    PM_zzzz_MM[zz2][zz1]*\
                                    PT_zz_zzzzt[(zz1,zz2,h)][z2+1][z1+1]
                except:
                    continue
            else:
                try:
                    PM[z1][z2][h] = PM_BB[t_peak][b2][b1]*\
                                PM_zB[z2+1][b2]
                except:
                    continue
                

uber_tr_mat = np.zeros([263,263,144])
for t in range(144):
    print(t)
    subdata = data_2013.loc[data_2013.pickup_t==t+1]
    uber_tr_t = pd.crosstab(subdata.pickup_zone_gid, subdata.dropoff_zone_gid)
    uber_tr_t = uber_tr_t.div(uber_tr_t.sum(axis=1),axis=0)
    for z1 in range(263):
        try:
            uber_tr_mat[z1,[i for i in range(263) if i+1 in uber_tr_t.columns],t] = uber_tr_t.loc[uber_tr_t.index==z1+1]
        except:
            continue
        
uber_tr_mat_h = np.zeros([263,263,24])
for h in range(24):
    print(h)
    subdata = data_2013.loc[(data_2013.pickup_t-1)//6==h]
    uber_tr_h = pd.crosstab(subdata.pickup_zone_gid, subdata.dropoff_zone_gid)
    uber_tr_h = uber_tr_h.div(uber_tr_h.sum(axis=1),axis=0)
    for z1 in range(263):
        try:
            uber_tr_mat_h[z1,[i for i in range(263) if i+1 in uber_tr_h.columns],h] = uber_tr_h.loc[uber_tr_h.index==z1+1]
        except:
            continue

uber_tr_mat_tinvariant = np.zeros([263,263])
for z1 in range(263):
    try:
        uber_tr_mat_tinvariant[z1,[i for i in range(263) if i+1 in tr_2013.columns]] = tr_2013.loc[tr_2013.index==z1+1]
    except:
        continue
    

mta_tr = pd.crosstab(mta_2008.o_zone_gid, mta_2008.d_zone_gid)
mta_tr = mta_tr.div(mta_tr.sum(axis=1),axis=0)
mta_tr_zz = pd.crosstab(mta_2008.o_zz, mta_2008.d_zz)
mta_tr_zz = mta_tr_zz.div(mta_tr_zz.sum(axis=1),axis=0)
mta_tr_mat_tinvariant = np.zeros([263,263])
mta_tr_mat_zz_tinvariant = np.zeros([20,20])

for z1 in range(263):
    if z1+1 in mta_tr.index:
        mta_tr_mat_tinvariant[z1,[i for i in range(263) if i+1 in mta_tr.columns]] = mta_tr.loc[mta_tr.index==z1+1]
        
        
for zz1 in range(20):
    if zz1+1 in mta_tr_zz.index:
        mta_tr_mat_zz_tinvariant[zz1,[i for i in range(20) if i+1 in mta_tr_zz.columns]] = mta_tr_zz.loc[mta_tr_zz.index==zz1+1]        
        
        
        
        
        

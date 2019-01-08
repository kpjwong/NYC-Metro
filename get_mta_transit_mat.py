# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 22:36:20 2018

@author: jerem
"""

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
            uber_tr_mat_h[z1,[i for i in range(263) if i+1 in uber_tr_h.columns],h] = uber_tr_t.loc[uber_tr_h.index==z1+1]
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









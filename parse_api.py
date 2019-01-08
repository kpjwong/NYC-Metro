# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 17:03:58 2018

"""

import pandas as pd
import numpy as np

api_data = pd.read_csv('api_data.csv')
sm_data_mat = np.zeros([4,144,263])
w_data_mat = np.zeros([4,144,263])

for idx, row in api_data.iterrows():
    d = row['est_date']
    t = row['t']
    z = row['pickup_zone_gid']
    sm_data_mat[d-1][t-1][z-1] = row['mean_surge_multiplier']
    w_data_mat[d-1][t-1][z-1] = row['waiting_time']

mean_by_hour_data = pd.read_excel('mean_sm_w.xlsx',sheet_name='mean_by_hour')
mean_by_zz_data = pd.read_excel('mean_sm_w.xlsx',sheet_name='mean_by_zz')
mean_by_z_t_data = pd.read_excel('mean_sm_w.xlsx',sheet_name='mean_by_z_t')
mean_by_s_data = pd.read_excel('mean_sm_w.xlsx',sheet_name='mean_by_s')

z_to_zz = pd.read_csv('z_to_zz.csv')

for d in range(1,5):
    for t in range(1,145):
        for z in range(1,264):
            if sm_data_mat[d-1][t-1][z-1] == 0 or sm_data_mat[d-1][t-1][z-1] == 1:
                print(d,t,z)
                try:
                    sm_data_mat[d-1][t-1][z-1] = mean_by_z_t_data.loc[
                                                (mean_by_z_t_data.pickup_zone_gid==z) &
                                                (mean_by_z_t_data.t==t)].mean_surge_multiplier
                except:
                    s = 20*(t-1) + z_to_zz.zz[z-1]
                    sm_data_mat[d-1][t-1][z-1] = mean_by_s_data.mean_surge_by_s[s-1]
            if w_data_mat[d-1][t-1][z-1] == 0:
                print(d,t,z)
                try:
                    w_data_mat[d-1][t-1][z-1] = mean_by_zz_data.loc[
                                               (mean_by_zz_data.est_date==d) &
                                               (mean_by_zz_data.zz==z_to_zz.zz[z-1]) &
                                               (mean_by_zz_data.t==t)].mean_wait_by_zz
                except:
                    try:
                        h = (t-1)//6
                        w_data_mat[d-1][t-1][z-1] = mean_by_hour_data.loc[
                                                   (mean_by_hour_data.est_date==d)
                                                   (mean_by_hour_data.hour==h) &
                                                   (mean_by_hour_data.pickup_zone_gid==z)].mean_wait_by_hour
                    except:
                        try:
                            w_data_mat[d-1][t-1][z-1] = mean_by_z_t_data.loc[
                                                       (mean_by_z_t_data.t==t) &
                                                       (mean_by_z_t_data.pickup_zone_gid==z)].mean_wait_by_z_t
                        except:
                            s = 20*(t-1) + z_to_zz.zz[z-1]
                            w_data_mat[d-1][t-1][z-1] = mean_by_s_data.mean_wait_by_s[s-1]


            
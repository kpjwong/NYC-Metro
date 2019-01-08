# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 00:03:29 2018

@author: jerem
"""

import pandas as pd
import numpy as np

est_mta_data = pd.read_csv('est_mta.csv')
est_mta_data.sort_values(['unit', 'scp', 'date', 'time'])
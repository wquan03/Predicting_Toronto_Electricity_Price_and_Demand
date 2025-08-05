import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
import warnings
import re
import openpyxl

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var


def combine_csvs(file_prefix, start_year, source_file_path, header):
    df_lst = []
    for year in range(start_year, var.cur_year + 1):
        df = pd.read_csv(source_file_path + file_prefix + str(year) + '.csv', header = header)
        df_lst.append(df)
        
    df_final = pd.concat(df_lst)
    return df_final


def cal_outlier_df(df, target_col):
    spike_col = target_col + ' is spike'
    df[spike_col] = 0
    df['z_score'] = np.abs(stats.zscore(df[target_col]))
    df[spike_col] = df['z_score'].apply(lambda x: 1 if x >= 3 else 0)
    df = df.drop(columns=[target_col, 'z_score'])

    # print(df.loc[df[spike_col] == 1].head())
    return df, spike_col
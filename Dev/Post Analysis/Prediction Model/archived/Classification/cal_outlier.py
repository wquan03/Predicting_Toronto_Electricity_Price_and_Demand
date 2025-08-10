import pandas as pd
import numpy as np
from scipy import stats



def cal_outlier_df(df, target_col):
    spike_col = target_col + ' is spike'
    df[spike_col] = 0
    df['z_score'] = np.abs(stats.zscore(df[target_col]))
    df[spike_col] = df['z_score'].apply(lambda x: 1 if x >= 3 else 0)
    df = df.drop(columns=[target_col, 'z_score'])

    # print(df.loc[df[spike_col] == 1].head())
    return df



# all_field_data_daily
daily_file_nm = 'all_field_data_daily'
df_daily = pd.read_excel(daily_file_nm + '.xlsx', sheet_name = 'All Data Fields')
df_daily = df_daily.drop('Ontario Demand', axis = 1)

df_daily = cal_outlier_df(df_daily, 'Toronto Demand')
df_daily = cal_outlier_df(df_daily, 'Price')

# all_field_data_monthly
monthly_file_nm = 'all_field_data_monthly'
df_monthly = pd.read_excel(monthly_file_nm + '.xlsx', sheet_name = 'All Data Fields')
df_monthly = df_monthly.drop('Ontario Demand', axis = 1)

df_monthly = cal_outlier_df(df_monthly, 'Toronto Demand')
df_monthly = cal_outlier_df(df_monthly, 'Price')

# output
df_daily.to_csv(daily_file_nm + '_with_outlier.csv', index = False)
df_monthly.to_csv(monthly_file_nm + '_with_outlier.csv', index = False)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var


df_weather = pd.read_csv(var.weather_input + 'weatherstats_toronto_daily.csv')
df_hdd_cdd = pd.read_csv(var.weather_input + 'CYYZ Heating Cooling Combined.csv')
df_weather = df_weather.rename(columns = {
    'date': 'Date',
    'heatdegdays': 'HDD 18',
    'cooldegdays': 'CDD 18'
})

df_all_weather = df_weather.merge(df_hdd_cdd, how = 'left', on = 'Date')
df_all_weather = df_all_weather.iloc[::-1]

df_all_weather['Date'] = pd.to_datetime(df_all_weather['Date'])

group_lst = ['avg_hourly_temperature', 'avg_hourly_relative_humidity', 'avg_hourly_dew_point', 'avg_hourly_wind_speed', 'avg_hourly_pressure_sea', 'daylight', 'HDD 15.5', 'CDD 15.5', 'HDD 18', 'CDD 18']
# Monthly
df_all_weather_monthly_avg = df_all_weather.groupby(pd.Grouper(key='Date', freq='ME'))[group_lst].mean().reset_index()
df_all_weather_monthly_avg['Date'] = df_all_weather_monthly_avg['Date'].dt.strftime('%Y-%m')
df_precipitation_monthly_sum = df_all_weather.groupby(pd.Grouper(key='Date', freq='ME'))['precipitation'].sum().reset_index()
df_precipitation_monthly_sum['Date'] = df_precipitation_monthly_sum['Date'].dt.strftime('%Y-%m')

# Yearly
df_all_weather_yearly_avg = df_all_weather.groupby(pd.Grouper(key='Date', freq='YE'))[group_lst].mean().reset_index()
df_all_weather_yearly_avg['Date'] = df_all_weather_yearly_avg['Date'].dt.strftime('%Y')
df_precipitation_yearly_sum = df_all_weather.groupby(pd.Grouper(key='Date', freq='YE'))['precipitation'].sum().reset_index()
df_precipitation_yearly_sum['Date'] = df_precipitation_yearly_sum['Date'].dt.strftime('%Y')

# Combine the sum and mean columns
df_all_weather_monthly = df_all_weather_monthly_avg.merge(df_precipitation_monthly_sum, how = 'left', on = 'Date')
df_all_weather_yearly = df_all_weather_yearly_avg.merge(df_precipitation_yearly_sum, how = 'left', on = 'Date')

# Reoder the df
order_lst = ['Date'] + group_lst + ['precipitation']
df_all_weather = df_all_weather[order_lst]

# Output to excel
with pd.ExcelWriter(var.weather_output + 'weather_time_series_data.xlsx') as writer:
    df_all_weather.to_excel(writer, sheet_name='daily average', index=False)

    df_all_weather_monthly.to_excel(writer, sheet_name='monthly average', index=False)
    df_all_weather_yearly.to_excel(writer, sheet_name='yearly average', index=False)
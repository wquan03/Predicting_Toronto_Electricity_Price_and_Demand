import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import reduce
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var

# read in all data fields
demand_dict = pd.read_excel(var.demand_output + 'toronto_demand_time_series_data.xlsx', sheet_name = None)
supply_dict = pd.read_excel(var.supply_output + 'ontario_supply_time_series_data.xlsx', sheet_name = None)
price_dict = pd.read_excel(var.market_price_output + 'toronto_price_time_series_data.xlsx', sheet_name = None)
gas_price_dict = pd.read_excel(var.market_price_output + 'natural_gas_price_time_series_data.xlsx', sheet_name = None)
weather_dict = pd.read_excel(var.weather_output + 'weather_time_series_data.xlsx', sheet_name = None)
df_data_dictionary = pd.read_csv(var.anaylsis_input + 'data_dictionary.csv')
df_population = pd.read_excel(var.population_input + 'toronto_yearly_population.xlsx')



lst_of_dict = [demand_dict, supply_dict, price_dict, gas_price_dict, weather_dict]

# extract daily and monthly average
lst_of_daily_df = []
lst_of_monthly_df = []
for dict in lst_of_dict:
    df_daily = dict.get('daily average')
    df_daily['Date'] = pd.to_datetime(df_daily['Date'])
    df_monthly = dict.get('monthly average')
    df_monthly['Date'] = pd.to_datetime(df_monthly['Date'])
    lst_of_daily_df.append(df_daily)
    lst_of_monthly_df.append(df_monthly)

# merge the list of dfs from all the dictionaries
def merge_dfs(left, right):
    return pd.merge(left, right, on = 'Date', how='left') 

df_all_field_daily = reduce(merge_dfs, lst_of_daily_df)
df_all_field_monthly = reduce(merge_dfs, lst_of_monthly_df)

# Define start and end dates
start_date = '2003-05-01'
end_date = '2025-4-30'
df_all_field_daily = df_all_field_daily[(df_all_field_daily['Date'] >= start_date) & (df_all_field_daily['Date'] <= end_date)]
df_all_field_monthly = df_all_field_monthly[(df_all_field_monthly['Date'] >= start_date) & (df_all_field_monthly['Date'] <= end_date)]


# rename columns for better understanding
rename_dict = {
    'avg_hourly_temperature': 'Temperature', 
    'avg_hourly_relative_humidity': 'Relative Humidity',
    'avg_hourly_dew_point': 'Dew Point',
    'avg_hourly_wind_speed': 'Wind Speed', 
    'avg_hourly_pressure_sea': 'Sea Level Pressure',
    'precipitation': 'Precipitation (mm)'
}
df_all_field_daily = df_all_field_daily.rename(columns = rename_dict)
df_all_field_monthly = df_all_field_monthly.rename(columns = rename_dict)

# enrich the dataset
def enrich_dataset(df, level = 'day'):
    df['Date'] = pd.to_datetime(df['Date'])
    if level == 'day':
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['DayOfWeek'] = df['Date'].dt.dayofweek

        df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
        # df['IsWeekend'] = 1 if df['DayOfWeek'] >= 5 else 0
    elif level == 'month':
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        
    else:
        df['Year'] = df['Date'].dt.year
    df['TempSquared'] = df[var.toronto_temp] ** 2
    df['PrevDayDemand'] = df[var.toront_demand].shift(1)
    return df

df_all_field_daily = enrich_dataset(df_all_field_daily)
df_all_field_monthly = enrich_dataset(df_all_field_monthly, 'month')

# Merge population data based on column year - since population is yearly data
df_all_field_daily = df_all_field_daily.merge(df_population, how = 'left', on = 'Year')
df_all_field_monthly = df_all_field_monthly.merge(df_population, how = 'left', on = 'Year')

# Drop unwantted fields
df_all_field_daily = df_all_field_daily.drop('daylight', axis = 1)
df_all_field_monthly = df_all_field_monthly.drop('daylight', axis = 1)

# fill na as 0
df_all_field_daily = df_all_field_daily.fillna(0)
df_all_field_monthly = df_all_field_monthly.fillna(0)

# Drop non-numeric columns like 'Date'
# df_pct_change_daily = df_all_field_daily.drop(columns=['Date']).pct_change(fill_method=None)
# df_pct_change_monthly = df_all_field_monthly.drop(columns=['Date']).pct_change(fill_method=None)

# Optionally reattach the Date column
# df_pct_change_daily.insert(0, 'Date', df_all_field_daily['Date'])
# df_pct_change_monthly.insert(0, 'Date', df_all_field_monthly['Date'])

# Drop the first row if you don't want NaNs
# df_pct_change = df_pct_change.dropna()

# Output to excel
with pd.ExcelWriter(var.anaylsis_output + 'all_field_data_daily.xlsx') as writer:
    df_data_dictionary.to_excel(writer, sheet_name = 'Data Dictionary', index=False)

    df_all_field_daily.to_excel(writer, sheet_name='All Data Fields', index=False)
    # df_pct_change_daily.to_excel(writer, sheet_name='All Data Fields % Change', index=False)

with pd.ExcelWriter(var.anaylsis_output + 'all_field_data_monthly.xlsx') as writer:
    df_data_dictionary.to_excel(writer, sheet_name = 'Data Dictionary', index=False)

    df_all_field_monthly.to_excel(writer, sheet_name='All Data Fields', index=False)
    # df_pct_change_monthly.to_excel(writer, sheet_name='All Data Fields % Change', index=False)
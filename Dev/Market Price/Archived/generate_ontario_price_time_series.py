import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import re
import openpyxl
from difflib import SequenceMatcher  # SequenceMatcher(None, a, b).ratio()

import os
import sys

# base_root = 'C:\\Users\\CGOD\\Desktop\\University\\ROP\\IESO MRP Data\\'
# sys.path.append(base_root)

# from utilities import variables as var

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utilities import variables as var


df_price = pd.read_excel(var.market_price_input + 'Ontario HOEP Predis OR\\PUB_PriceHOEPPredispOR_merged.xlsx')



# Combining date with hour
df_price['Date'] = pd.to_datetime(df_price['Date'])
df_price['Date'] = df_price['Date'] + pd.to_timedelta(df_price['Hour'], unit='h')
df_price = df_price.drop('Hour', axis = 1)

# Remove unwanted columns
df_price = df_price.drop(['Hour 1 Predispatch', 'Hour 2 Predispatch', 'Hour 3 Predispatch'], axis = 1)

# Pre-process the data
df_price['HOEP'] = df_price['HOEP'].fillna('0')
df_price['OR 10 Min Sync'] = df_price['OR 10 Min Sync'].fillna('0')
df_price['OR 10 Min non-sync'] = df_price['OR 10 Min non-sync'].fillna('0')
df_price['OR 30 Min'] = df_price['OR 30 Min'].fillna('0')

df_price['HOEP'] = df_price['HOEP'].astype(str).str.replace(',', '').astype(float)
df_price['OR 10 Min Sync'] = df_price['OR 10 Min Sync'].astype(str).str.replace(',', '').astype(float)
df_price['OR 10 Min non-sync'] = df_price['OR 10 Min non-sync'].astype(str).str.replace(',', '').astype(float)
df_price['OR 30 Min'] = df_price['OR 30 Min'].astype(str).str.replace(',', '').astype(float)


# Daily average
df_price_daily = df_price.groupby(pd.Grouper(key='Date', freq='D'))[['HOEP', 'OR 10 Min Sync', 'OR 10 Min non-sync', 'OR 30 Min']].mean()
df_price_daily.index = df_price_daily.index.strftime('%Y-%m-%d')

# Monthly average
df_price_monthly = df_price.groupby(pd.Grouper(key='Date', freq='ME'))[['HOEP', 'OR 10 Min Sync', 'OR 10 Min non-sync', 'OR 30 Min']].mean()
df_price_monthly.index = df_price_monthly.index.strftime('%Y-%m')

# Output to excel
with pd.ExcelWriter(var.market_price_output + 'ontario_price_time_series_data.xlsx') as writer:
    df_price.to_excel(writer, sheet_name='raw data', index = False)
    df_price_daily.to_excel(writer, sheet_name='daily average')
    df_price_monthly.to_excel(writer, sheet_name='monthly average')
# print(df_price)

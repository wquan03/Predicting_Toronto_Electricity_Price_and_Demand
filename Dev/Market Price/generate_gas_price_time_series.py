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

df_gas_price = pd.read_excel(var.gas_price_input + 'EIA Natural Gas.xls', sheet_name = 'Data 1', header = 2)
df_gas_price.columns = ['Date', 'Gas Price']

# Convert to datetime with time
df_gas_price['Date'] = pd.to_datetime(df_gas_price['Date'])

# Reset index to include skipped days
df_gas_price.set_index('Date', inplace=True)
full_idx = pd.date_range(start=df_gas_price.index.min(), end=df_gas_price.index.max(), freq='D')
df_gas_price = df_gas_price.reindex(full_idx)
# Fill the missing days
df_gas_price['Gas Price'] = df_gas_price['Gas Price'].ffill()

# Reset index and rename
df_gas_price = df_gas_price.reset_index().rename(columns={'index': 'Date'})

# Daily average
df_gas_price_daily = df_gas_price.groupby(pd.Grouper(key='Date', freq='D'))['Gas Price'].mean()
df_gas_price_daily.index = df_gas_price_daily.index.strftime('%Y-%m-%d')

# Monthly average
df_gas_price_monthly = df_gas_price.groupby(pd.Grouper(key='Date', freq='ME'))['Gas Price'].mean()
df_gas_price_monthly.index = df_gas_price_monthly.index.strftime('%Y-%m')

# Output to excel
with pd.ExcelWriter(var.market_price_output + 'natural_gas_price_time_series_data.xlsx') as writer:
    df_gas_price.to_excel(writer, sheet_name='raw data', index = False)
    df_gas_price_daily.to_excel(writer, sheet_name='daily average')
    df_gas_price_monthly.to_excel(writer, sheet_name='monthly average')
# print(df_gas_price)

